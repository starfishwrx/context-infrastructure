from __future__ import annotations

import os
import subprocess
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from opencode_client import OpenCodeClient


WORKSPACE_ROOT = Path(__file__).resolve().parents[4]


@dataclass(frozen=True)
class AgentRunResult:
    backend: str
    final_message: str
    resolved_model: str | None = None
    session_id: str | None = None


def get_workspace_root() -> Path:
    return WORKSPACE_ROOT


def normalize_backend(backend: str | None) -> str:
    selected = (backend or os.getenv("AI_HEARTBEAT_BACKEND") or "codex").strip().lower()
    if selected not in {"codex", "opencode"}:
        raise ValueError(
            f"Unsupported backend: {selected}. Expected one of: codex, opencode."
        )
    return selected


def run_agent_task(
    prompt: str,
    *,
    backend: str | None = None,
    model_id: str | None = None,
    session_title: str | None = None,
    workdir: Path | None = None,
    search: bool = False,
    delete_after: bool = True,
    sandbox: str = "workspace-write",
    approval_policy: str = "never",
) -> AgentRunResult:
    selected_backend = normalize_backend(backend)
    resolved_workdir = Path(workdir or WORKSPACE_ROOT).resolve()

    if selected_backend == "codex":
        return _run_with_codex(
            prompt=prompt,
            model_id=model_id,
            workdir=resolved_workdir,
            search=search,
            sandbox=sandbox,
            approval_policy=approval_policy,
        )

    return _run_with_opencode(
        prompt=prompt,
        model_id=model_id,
        session_title=session_title,
        delete_after=delete_after,
    )


def _run_with_codex(
    *,
    prompt: str,
    model_id: str | None,
    workdir: Path,
    search: bool,
    sandbox: str,
    approval_policy: str,
) -> AgentRunResult:
    codex_bin = os.getenv("CODEX_BIN") or _default_codex_bin()
    output_dir = workdir / ".codex_tmp"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"last_message_{uuid.uuid4().hex}.txt"

    command = [
        codex_bin,
        "exec",
        "-C",
        str(workdir),
        "-s",
        sandbox,
        "-o",
        str(output_path),
        "-",
    ]
    if model_id:
        command[2:2] = ["-m", model_id]
    if search:
        command.insert(-1, "--search")

    result = subprocess.run(
        command,
        input=prompt,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
    )

    final_message = ""
    if output_path.exists():
        final_message = output_path.read_text(encoding="utf-8", errors="ignore").strip()
    if not final_message:
        final_message = (result.stdout or result.stderr).strip()

    if result.returncode != 0:
        raise RuntimeError(
            "Codex CLI task failed.\n"
            f"Command: {' '.join(command)}\n"
            f"Exit code: {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    return AgentRunResult(
        backend="codex",
        final_message=final_message,
        resolved_model=model_id or os.getenv("CODEX_MODEL"),
    )


def _run_with_opencode(
    *,
    prompt: str,
    model_id: str | None,
    session_title: str | None,
    delete_after: bool,
) -> AgentRunResult:
    client = OpenCodeClient()
    title = session_title or f"AI Heartbeat Task {datetime.now():%Y-%m-%d %H:%M}"
    session_id = client.create_session(title)
    if not session_id:
        raise RuntimeError("Failed to create OpenCode session.")

    response = client.send_message(
        session_id,
        prompt,
        model_id=model_id or os.getenv("OPENCODE_MODEL", "anthropic/claude-sonnet-4-6"),
    )
    if response is None:
        raise RuntimeError("OpenCode did not accept the task.")

    client.wait_for_session_complete(session_id)
    messages = client.get_session_messages(session_id) or []
    assistant_messages = [
        message for message in messages if (message.get("info") or {}).get("role") == "assistant"
    ]

    final_message = ""
    resolved_model = None
    if assistant_messages:
        last_message = assistant_messages[-1]
        final_message = _extract_text(last_message).strip()
        info = last_message.get("info") or {}
        provider_id = info.get("providerID")
        model_name = info.get("modelID")
        if provider_id and model_name:
            resolved_model = f"{provider_id}/{model_name}"
        elif model_name:
            resolved_model = model_name

    if delete_after:
        client.delete_session(session_id)

    return AgentRunResult(
        backend="opencode",
        final_message=final_message,
        resolved_model=resolved_model,
        session_id=session_id,
    )


def _default_codex_bin() -> str:
    appdata = os.getenv("APPDATA")
    if appdata:
        candidate = Path(appdata) / "npm" / "codex.cmd"
        if candidate.exists():
            return str(candidate)
    return "codex"


def _extract_text(value: Any) -> str:
    parts: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, str):
            parts.append(node)
            return
        if isinstance(node, list):
            for item in node:
                walk(item)
            return
        if isinstance(node, dict):
            node_type = node.get("type")
            if node_type == "text" and isinstance(node.get("text"), str):
                parts.append(node["text"])
                return
            for child in node.values():
                walk(child)

    walk(value)
    return "\n".join(part for part in parts if part)
