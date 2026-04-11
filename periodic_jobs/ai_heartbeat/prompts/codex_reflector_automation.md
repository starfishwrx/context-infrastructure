# Codex Automation Prompt: Thin Reflector Trigger

Run this exact command from the workspace root and wait for it to finish:

```powershell
python periodic_jobs/ai_heartbeat/src/v0/reflector.py --backend codex --memory-file "C:/Users/Administrator/.codex/automations/ai-heartbeat-reflector/memory.md"
```

Rules:
- Do not perform normal workspace bootstrap.
- Do not inspect repo files yourself unless the command fails before doing any useful work.
- If the command fails, run at most one follow-up read command to inspect the error output you already have.
- Return a short walkthrough based on the command stdout.
