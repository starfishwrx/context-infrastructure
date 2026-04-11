#!/usr/bin/env python3
"""
L1 Observer runner.

Codex backend:
- Python collects local workspace context.
- Codex only returns structured observation JSON.
- Python writes OBSERVATIONS.md and automation memory.

OpenCode backend:
- Preserves the original prompt-driven behavior for compatibility.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from agent_runner import get_workspace_root, normalize_backend, run_agent_task
from heartbeat_runtime import (
    collect_recent_file_context,
    collect_root_file_context,
    compact_line,
    now_label,
    run_codex_json_task,
    write_automation_memory,
)


WORKSPACE_ROOT = get_workspace_root()
KNOWLEDGE_BASE = WORKSPACE_ROOT / "periodic_jobs" / "ai_heartbeat" / "docs" / "KNOWLEDGE_BASE.md"
OBSERVATIONS_PATH = WORKSPACE_ROOT / "contexts" / "memory" / "OBSERVATIONS.md"
PROMPT_TEMPLATE_PATH = (
    WORKSPACE_ROOT / "periodic_jobs" / "ai_heartbeat" / "prompts" / "codex_observer.md"
)
DEFAULT_OBSERVER_MEMORY = Path(
    "C:/Users/Administrator/.codex/automations/ai-heartbeat-observer/memory.md"
)

PRIORITY_EMOJI = {
    "high": "🔶",
    "medium": "🟡",
    "low": "🟢",
}
OBSERVER_OUTPUT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["decision", "entries", "walkthrough"],
    "properties": {
        "decision": {"type": "string", "enum": ["write", "skip"]},
        "entries": {
            "type": "array",
            "maxItems": 6,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["priority", "tag", "observation"],
                "properties": {
                    "priority": {
                        "type": "string",
                        "enum": ["high", "medium", "low"],
                    },
                    "tag": {"type": "string"},
                    "observation": {"type": "string"},
                },
            },
        },
        "walkthrough": {"type": "string"},
    },
}


def build_legacy_prompt(target_date: str) -> str:
    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    return (
        template.replace("{{TARGET_DATE}}", target_date)
        .replace("{{WORKSPACE_ROOT}}", WORKSPACE_ROOT.as_posix())
        .replace("{{KNOWLEDGE_BASE_PATH}}", KNOWLEDGE_BASE.as_posix())
        .replace("{{OBSERVATIONS_PATH}}", OBSERVATIONS_PATH.as_posix())
    )


def collect_observer_context() -> dict[str, object]:
    roots = [
        WORKSPACE_ROOT / "adhoc_jobs",
        WORKSPACE_ROOT / "periodic_jobs",
        WORKSPACE_ROOT / "rules" / "skills",
    ]
    return {
        "scan_roots": [root.relative_to(WORKSPACE_ROOT).as_posix() for root in roots],
        "recent_files_by_root": collect_recent_file_context(
            roots=roots,
            per_root_limit=4,
            excerpt_limit=900,
        ),
        "recent_root_files": collect_root_file_context(
            limit=5,
            excerpt_limit=700,
        ),
        "noise_filters": [
            "contexts/daily_records/",
            "__pycache__/",
            ".pytest_cache/",
            "artifacts/",
            "backup/",
            "backups/",
            ".env",
        ],
    }


def build_codex_prompt(target_date: str, context_payload: dict[str, object]) -> str:
    context_json = json.dumps(context_payload, ensure_ascii=False, indent=2)
    return f"""
你是一个长期 context infrastructure workspace 的 L1 Observer。
你的任务是基于给定的本地上下文快照，提炼高价值观察。

只返回原始 JSON，不要使用 Markdown 代码块，不要输出额外解释。

输出结构：
{{
  "decision": "write" | "skip",
  "entries": [
    {{
      "priority": "high" | "medium" | "low",
      "tag": "短标签",
      "observation": "单行观察，可包含相对仓库路径"
    }}
  ],
  "walkthrough": "简短说明"
}}

规则：
- 目标日期是 {target_date}。
- 只能基于提供的 context JSON 作答，不要假设隐藏文件或额外上下文。
- `high` 表示可复用方法、长期约束、或架构级经验。
- `medium` 表示活跃项目的重要里程碑、决策、或未来几周仍有价值的上下文。
- `low` 表示短期但仍有用的执行上下文。
- 观察必须简洁、具体、单行化。
- 引用文件时使用相对仓库路径。
- 不要泄露秘密信息，不要臆测。
- 如果观察不够强，宁可返回 `skip`。
- 最多返回 6 条 entries。
- `walkthrough` 用中文简要说明你看了什么、为何写入或跳过。

Context JSON：
{context_json}
""".strip()


def format_entries(entries: list[dict[str, str]]) -> str:
    lines: list[str] = []
    for entry in entries:
        priority = (entry.get("priority") or "").strip().lower()
        tag = compact_line(entry.get("tag") or "Observation")
        observation = compact_line(entry.get("observation") or "")
        if priority not in PRIORITY_EMOJI or not observation:
            continue
        lines.append(f"{PRIORITY_EMOJI[priority]} {priority.title()}: [{tag}] {observation}")
    return "\n".join(lines)


def append_observations(target_date: str, entries: list[dict[str, str]], *, dry_run: bool) -> int:
    rendered_entries = format_entries(entries)
    if not rendered_entries:
        return 0

    section = f"\nDate: {target_date}\n\n{rendered_entries}\n"
    if dry_run:
        return rendered_entries.count("\n") + 1

    existing = OBSERVATIONS_PATH.read_text(encoding="utf-8") if OBSERVATIONS_PATH.exists() else ""
    separator = "" if not existing or existing.endswith("\n") else "\n"
    OBSERVATIONS_PATH.write_text(existing + separator + section, encoding="utf-8")
    return rendered_entries.count("\n") + 1


def run_codex_observer(
    target_date: str,
    *,
    model_id: str | None,
    memory_path: Path | None,
    dry_run: bool,
) -> str:
    context_payload = collect_observer_context()
    payload, raw_output = run_codex_json_task(
        build_codex_prompt(target_date, context_payload),
        schema=OBSERVER_OUTPUT_SCHEMA,
        model_id=model_id,
    )

    if not isinstance(payload, dict):
        raise RuntimeError(f"Observer returned non-object JSON: {raw_output}")

    decision = str(payload.get("decision") or "skip").strip().lower()
    entries = payload.get("entries") or []
    walkthrough = compact_line(payload.get("walkthrough") or "")
    if not isinstance(entries, list):
        raise RuntimeError(f"Observer returned invalid entries payload: {raw_output}")

    written_count = 0
    if decision == "write":
        written_count = append_observations(target_date, entries, dry_run=dry_run)
        if written_count == 0:
            decision = "skip"

    summary = (
        walkthrough
        or (
            f"Observer wrote {written_count} entries for {target_date}."
            if decision == "write"
            else f"Observer skipped {target_date}: no strong observations."
        )
    )

    write_automation_memory(
        memory_path,
        title="AI Heartbeat Observer Memory",
        lines=[
            f"Last run: {now_label()}",
            f"Backend: codex",
            f"Target date: {target_date}",
            f"Decision: {'dry-run ' if dry_run else ''}{decision}",
            f"Entries: {written_count}",
            "Context: local deterministic scan under adhoc_jobs/, periodic_jobs/, rules/skills/, and workspace root files.",
            f"Notes: {summary}",
        ],
    )
    return summary


def run_legacy_observer(
    target_date: str,
    *,
    backend: str,
    model_id: str | None,
    delete_after: bool,
) -> str:
    prompt = build_legacy_prompt(target_date)
    print(
        f"Triggering observer for {target_date} with backend={backend} model={model_id or '(default)'}"
    )
    result = run_agent_task(
        prompt,
        backend=backend,
        model_id=model_id,
        session_title=f"Heartbeat L1 - Persistence Mode - {target_date}",
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

    parser = argparse.ArgumentParser(description="L1 Observer Agent")
    parser.add_argument(
        "date",
        nargs="?",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Target date (YYYY-MM-DD)",
    )
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

    target_date = args.date
    backend = normalize_backend(args.backend)
    model_id = args.model
    delete_after = not args.no_delete
    memory_path = Path(args.memory_file) if args.memory_file else (
        DEFAULT_OBSERVER_MEMORY if backend == "codex" else None
    )

    if OBSERVATIONS_PATH.exists():
        content = OBSERVATIONS_PATH.read_text(encoding="utf-8")
        if f"Date: {target_date}" in content:
            summary = f"Idempotent skip: entry for {target_date} already exists in OBSERVATIONS.md"
            write_automation_memory(
                memory_path,
                title="AI Heartbeat Observer Memory",
                lines=[
                    f"Last run: {now_label()}",
                    f"Backend: {backend}",
                    f"Target date: {target_date}",
                    "Decision: skip-existing-entry",
                    f"Notes: {summary}",
                ],
            )
            print(summary)
            return

    if backend == "codex":
        summary = run_codex_observer(
            target_date,
            model_id=model_id,
            memory_path=memory_path,
            dry_run=args.dry_run,
        )
        print(summary)
        return

    run_legacy_observer(
        target_date,
        backend=backend,
        model_id=model_id,
        delete_after=delete_after,
    )


if __name__ == "__main__":
    main()
