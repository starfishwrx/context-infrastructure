#!/usr/bin/env python3
"""
L2 Reflector runner.

Codex backend:
- Python reads OBSERVATIONS.md and candidate rules files locally.
- Codex returns a structured rewrite plan as JSON.
- Python applies the approved file writes deterministically.

OpenCode backend:
- Preserves the original prompt-driven behavior for compatibility.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from agent_runner import get_workspace_root, normalize_backend, run_agent_task
from heartbeat_runtime import compact_line, load_text, now_label, run_codex_json_task, write_automation_memory


WORKSPACE_ROOT = get_workspace_root()
KNOWLEDGE_BASE = WORKSPACE_ROOT / "periodic_jobs" / "ai_heartbeat" / "docs" / "KNOWLEDGE_BASE.md"
OBSERVATIONS_PATH = WORKSPACE_ROOT / "contexts" / "memory" / "OBSERVATIONS.md"
PROMPT_TEMPLATE_PATH = (
    WORKSPACE_ROOT / "periodic_jobs" / "ai_heartbeat" / "prompts" / "codex_reflector.md"
)
DEFAULT_REFLECTOR_MEMORY = Path(
    "C:/Users/Administrator/.codex/automations/ai-heartbeat-reflector/memory.md"
)
REFLECTOR_OUTPUT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["decision", "observations_content", "rule_updates", "walkthrough"],
    "properties": {
        "decision": {"type": "string", "enum": ["write", "skip"]},
        "observations_content": {"type": "string"},
        "rule_updates": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["path", "content", "reason"],
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                    "reason": {"type": "string"},
                },
            },
        },
        "walkthrough": {"type": "string"},
    },
}
CORE_RULE_FILES = [
    WORKSPACE_ROOT / "rules" / "SOUL.md",
    WORKSPACE_ROOT / "rules" / "USER.md",
    WORKSPACE_ROOT / "rules" / "COMMUNICATION.md",
    WORKSPACE_ROOT / "rules" / "WORKSPACE.md",
    WORKSPACE_ROOT / "rules" / "skills" / "INDEX.md",
]


def build_legacy_prompt() -> str:
    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    return (
        template.replace("{{WORKSPACE_ROOT}}", WORKSPACE_ROOT.as_posix())
        .replace("{{KNOWLEDGE_BASE_PATH}}", KNOWLEDGE_BASE.as_posix())
        .replace("{{OBSERVATIONS_PATH}}", OBSERVATIONS_PATH.as_posix())
    )


def reflector_write_allowed(relative_path: str) -> bool:
    normalized = relative_path.replace("\\", "/").lstrip("/")
    if normalized in {
        "rules/SOUL.md",
        "rules/USER.md",
        "rules/COMMUNICATION.md",
        "rules/WORKSPACE.md",
        "rules/skills/INDEX.md",
        "contexts/memory/OBSERVATIONS.md",
    }:
        return True
    return normalized.startswith("rules/skills/") or normalized.startswith("rules/axioms/")


def build_codex_prompt() -> str:
    context_payload = {
        "observations_path": "contexts/memory/OBSERVATIONS.md",
        "observations_content": load_text(OBSERVATIONS_PATH),
        "candidate_rule_files": {
            path.relative_to(WORKSPACE_ROOT).as_posix(): load_text(path)
            for path in CORE_RULE_FILES
            if path.exists()
        },
        "allowed_update_prefixes": [
            "rules/SOUL.md",
            "rules/USER.md",
            "rules/COMMUNICATION.md",
            "rules/WORKSPACE.md",
            "rules/skills/",
            "rules/axioms/",
            "contexts/memory/OBSERVATIONS.md",
        ],
    }
    context_json = json.dumps(context_payload, ensure_ascii=False, indent=2)
    return f"""
你是一个长期 context infrastructure workspace 的每周 L2 Reflector。
你会收到当前记忆文件，以及候选规则文件的快照。
你的任务是晋升稳定知识、清理过期噪音，并保持文件职责边界清晰。

只返回原始 JSON，不要使用 Markdown 代码块，不要输出额外解释。

输出结构：
{{
  "decision": "write" | "skip",
  "observations_content": "contexts/memory/OBSERVATIONS.md 的完整替换内容",
  "rule_updates": [
    {{
      "path": "允许前缀下的相对仓库路径",
      "content": "完整替换内容",
      "reason": "简短理由"
    }}
  ],
  "walkthrough": "简短总结"
}}

规则：
- 只能使用给定的文件内容和允许更新的路径前缀。
- 更新要保守。只晋升稳定、可复用、值得长期保留的知识。
- 必须保持每个文件的职责边界。
- 不要发明允许前缀之外的路径。
- 如果没有足够明确的晋升或清理理由，返回 `skip`。
- `observations_content` 必须始终返回完整文件内容，即使你认为它无需变化。
- `walkthrough` 用中文说明晋升了什么、清理了什么、为什么。

Context JSON：
{context_json}
""".strip()


def apply_reflector_writes(
    observations_content: str,
    rule_updates: list[dict[str, str]],
    *,
    dry_run: bool,
) -> list[str]:
    changed_paths: list[str] = []

    current_observations = OBSERVATIONS_PATH.read_text(encoding="utf-8")
    if observations_content and observations_content != current_observations:
        if not dry_run:
            OBSERVATIONS_PATH.write_text(observations_content, encoding="utf-8")
        changed_paths.append("contexts/memory/OBSERVATIONS.md")

    for update in rule_updates:
        relative_path = str(update.get("path") or "").replace("\\", "/").lstrip("/")
        content = update.get("content") or ""
        if not reflector_write_allowed(relative_path):
            raise RuntimeError(f"Reflector attempted to update disallowed path: {relative_path}")

        path = WORKSPACE_ROOT / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if content != current:
            if not dry_run:
                path.write_text(content, encoding="utf-8")
            changed_paths.append(relative_path)

    return changed_paths


def run_codex_reflector(
    *,
    model_id: str | None,
    memory_path: Path | None,
    dry_run: bool,
) -> str:
    payload, raw_output = run_codex_json_task(
        build_codex_prompt(),
        schema=REFLECTOR_OUTPUT_SCHEMA,
        model_id=model_id,
    )
    if not isinstance(payload, dict):
        raise RuntimeError(f"Reflector returned non-object JSON: {raw_output}")

    decision = str(payload.get("decision") or "skip").strip().lower()
    observations_content = str(payload.get("observations_content") or "")
    rule_updates = payload.get("rule_updates") or []
    walkthrough = compact_line(payload.get("walkthrough") or "")

    if not isinstance(rule_updates, list):
        raise RuntimeError(f"Reflector returned invalid rule_updates payload: {raw_output}")

    changed_paths: list[str] = []
    if decision == "write":
        changed_paths = apply_reflector_writes(
            observations_content,
            rule_updates,
            dry_run=dry_run,
        )
        if not changed_paths:
            decision = "skip"

    summary = (
        walkthrough
        or (
            f"Reflector updated {len(changed_paths)} files."
            if decision == "write"
            else "Reflector skipped: no durable promotion or cleanup was justified."
        )
    )

    write_automation_memory(
        memory_path,
        title="AI Heartbeat Reflector Memory",
        lines=[
            f"Last run: {now_label()}",
            "Backend: codex",
            f"Decision: {'dry-run ' if dry_run else ''}{decision}",
            f"Updated files: {', '.join(changed_paths) if changed_paths else '(none)'}",
            f"Notes: {summary}",
        ],
    )
    return summary


def run_legacy_reflector(
    *,
    backend: str,
    model_id: str | None,
    delete_after: bool,
) -> str:
    prompt = build_legacy_prompt()
    target_date = datetime.now().strftime("%Y-%m-%d")
    print(
        f"Triggering reflector with backend={backend} model={model_id or '(default)'}..."
    )
    result = run_agent_task(
        prompt,
        backend=backend,
        model_id=model_id,
        session_title=f"Heartbeat L2 Reflector - {target_date}",
        workdir=WORKSPACE_ROOT,
        delete_after=delete_after,
        sandbox="workspace-write",
    )
    if result.resolved_model:
        print(f"Resolved model: {result.resolved_model}")
    if result.session_id:
        print(f"Session: {result.session_id}")
    if result.final_message:
        print(result.final_message)
    print("Task complete.")
    return compact_line(result.final_message or "Task complete.")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="L2 Reflector Agent")
    parser.add_argument(
        "--backend",
        default=os.getenv("AI_HEARTBEAT_BACKEND", "codex"),
        choices=["codex", "opencode"],
        help="Agent backend to use",
    )
    parser.add_argument("--model", default=None, help="Model ID to use")
    parser.add_argument(
        "--no-delete",
        action="store_true",
        help="Keep OpenCode session after completion (ignored for Codex)",
    )
    parser.add_argument(
        "--memory-file",
        default=None,
        help="Optional automation memory file path",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the full flow but skip workspace writes",
    )
    args = parser.parse_args()

    backend = normalize_backend(args.backend)
    model_id = args.model
    delete_after = not args.no_delete
    memory_path = Path(args.memory_file) if args.memory_file else (
        DEFAULT_REFLECTOR_MEMORY if backend == "codex" else None
    )

    if backend == "codex":
        summary = run_codex_reflector(
            model_id=model_id,
            memory_path=memory_path,
            dry_run=args.dry_run,
        )
        print(summary)
        return

    run_legacy_reflector(
        backend=backend,
        model_id=model_id,
        delete_after=delete_after,
    )


if __name__ == "__main__":
    main()
