from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from agent_runner import get_workspace_root


WORKSPACE_ROOT = get_workspace_root()
CODEX_RUNTIME_DIR = Path.home() / ".codex" / "heartbeat_runtime"
CODEX_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)

TEXT_SUFFIXES = {
    "",
    ".csv",
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".ps1",
    ".py",
    ".sh",
    ".sql",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

SKIP_DIR_MARKERS = (
    "/.git/",
    "/.next/",
    "/.pytest_cache/",
    "/.venv/",
    "/__pycache__/",
    "/artifacts/",
    "/backup/",
    "/backups/",
    "/contexts/daily_records/",
    "/node_modules/",
)

SKIP_FILE_NAMES = {".env"}


def now_label() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def relative_path(path: Path) -> str:
    return path.resolve().relative_to(WORKSPACE_ROOT).as_posix()


def is_text_candidate(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.name in SKIP_FILE_NAMES:
        return False
    return path.suffix.lower() in TEXT_SUFFIXES


def should_skip_path(path: Path) -> bool:
    if path.name in SKIP_FILE_NAMES:
        return True
    try:
        rel = "/" + relative_path(path) + ("/" if path.is_dir() else "")
    except ValueError:
        rel = "/" + path.as_posix().lstrip("/") + ("/" if path.is_dir() else "")
    rel_lower = rel.lower()
    return any(marker in rel_lower for marker in SKIP_DIR_MARKERS)


def load_text(path: Path, limit: int | None = None) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if limit is None or len(text) <= limit:
        return text
    return text[:limit] + "\n\n...[truncated]..."


def compact_line(text: str) -> str:
    return " ".join(text.replace("\r", "\n").split())


def extract_json_payload(text: str) -> Any:
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            stripped = "\n".join(lines[1:-1]).strip()
            if stripped.startswith("json"):
                stripped = stripped[4:].strip()

    decoder = json.JSONDecoder()
    for idx, char in enumerate(stripped):
        if char not in "{[":
            continue
        try:
            payload, _ = decoder.raw_decode(stripped[idx:])
            return payload
        except json.JSONDecodeError:
            continue
    raise ValueError(f"Could not parse JSON payload from model output:\n{stripped}")


def default_codex_bin() -> str:
    appdata = os.getenv("APPDATA")
    if appdata:
        candidate = Path(appdata) / "npm" / "codex.cmd"
        if candidate.exists():
            return str(candidate)
    return "codex"


def run_codex_json_task(
    prompt: str,
    *,
    schema: dict[str, Any],
    model_id: str | None = None,
) -> tuple[Any, str]:
    codex_bin = os.getenv("CODEX_BIN") or default_codex_bin()
    output_dir = CODEX_RUNTIME_DIR / ".codex_tmp"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"last_message_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
    schema_path = output_dir / "heartbeat_output_schema.json"
    schema_path.write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")

    command = [
        codex_bin,
        "exec",
        "-C",
        str(CODEX_RUNTIME_DIR),
        "--skip-git-repo-check",
        "--ephemeral",
        "--color",
        "never",
        "-s",
        "read-only",
        "--output-schema",
        str(schema_path),
        "-o",
        str(output_path),
        "-",
    ]
    if model_id:
        command[2:2] = ["-m", model_id]

    result = subprocess.run(
        command,
        input=prompt,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
        timeout=300,
    )

    final_message = ""
    if output_path.exists():
        final_message = output_path.read_text(encoding="utf-8", errors="ignore").strip()
    if not final_message:
        final_message = (result.stdout or result.stderr).strip()

    if result.returncode != 0:
        raise RuntimeError(
            "Codex CLI inference task failed.\n"
            f"Command: {' '.join(command)}\n"
            f"Exit code: {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    payload = extract_json_payload(final_message)
    return payload, final_message


def collect_recent_file_context(
    *,
    roots: list[Path],
    per_root_limit: int = 6,
    excerpt_limit: int = 3000,
) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}

    for root in roots:
        if not root.exists():
            continue

        candidates: list[Path] = []
        for current_root, dir_names, file_names in os.walk(root):
            current_path = Path(current_root)
            dir_names[:] = [
                name
                for name in dir_names
                if not should_skip_path(current_path / name)
            ]
            for file_name in file_names:
                path = current_path / file_name
                if should_skip_path(path) or not is_text_candidate(path):
                    continue
                candidates.append(path)

        selected = sorted(
            candidates,
            key=lambda item: item.stat().st_mtime,
            reverse=True,
        )[:per_root_limit]

        records: list[dict[str, Any]] = []
        for path in selected:
            stat = path.stat()
            records.append(
                {
                    "path": relative_path(path),
                    "modified_at": datetime.fromtimestamp(stat.st_mtime)
                    .astimezone()
                    .strftime("%Y-%m-%d %H:%M:%S %z"),
                    "size_bytes": stat.st_size,
                    "excerpt": load_text(path, limit=excerpt_limit),
                }
            )
        result[relative_path(root)] = records

    return result


def collect_root_file_context(
    *,
    limit: int = 8,
    excerpt_limit: int = 2500,
) -> list[dict[str, Any]]:
    candidates = [
        path
        for path in WORKSPACE_ROOT.iterdir()
        if path.is_file() and not should_skip_path(path) and is_text_candidate(path)
    ]
    selected = sorted(
        candidates,
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )[:limit]

    records: list[dict[str, Any]] = []
    for path in selected:
        stat = path.stat()
        records.append(
            {
                "path": relative_path(path),
                "modified_at": datetime.fromtimestamp(stat.st_mtime)
                .astimezone()
                .strftime("%Y-%m-%d %H:%M:%S %z"),
                "size_bytes": stat.st_size,
                "excerpt": load_text(path, limit=excerpt_limit),
            }
        )
    return records


def write_automation_memory(
    memory_path: Path | None,
    *,
    title: str,
    lines: list[str],
) -> None:
    if memory_path is None:
        return

    memory_path.parent.mkdir(parents=True, exist_ok=True)
    content = [f"# {title}", ""]
    content.extend(f"- {line}" for line in lines)
    memory_path.write_text("\n".join(content).rstrip() + "\n", encoding="utf-8")
