# Memory Observations

This is the L1/L2 layer of the memory system. Daily observations are appended by the heartbeat observer, and the weekly reflector promotes only stable, reusable knowledge into `rules/`.

## Format

Each dated block uses this structure:

```text
Date: YYYY-MM-DD

High: [methodology / hard constraint] description
Medium: [project status / decision] description
Low: [ephemeral task flow] description
```

Priority meanings:

- `High`: cross-project lessons, durable constraints, or major architectural decisions worth long-term retention and possible promotion.
- `Medium`: active-project status or decisions that will still matter over the next few weeks.
- `Low`: transient execution notes, debug traces, or short-lived context that should be garbage-collected regularly.

## How to Load Memory

Do not load this entire file by default. Search by keyword or recent dates as needed.

```powershell
Select-String -Path contexts/memory/OBSERVATIONS.md -Pattern "keyword"
Select-String -Path contexts/memory/OBSERVATIONS.md -Pattern '^Date:' -Context 0,8
```

```bash
rg -n "keyword" contexts/memory/OBSERVATIONS.md
rg -n "^Date:" contexts/memory/OBSERVATIONS.md
```

---

Date: 2026-05-04

🟡 Medium: [ai-content-center] `adhoc_jobs/ai_content_center/` is still worth retaining as short-term memory because it stabilizes a 4399-first ContentOps shape: external platforms serve as inspiration inputs, while the internal pipeline owns briefs, drafts, deterministic review gates, publish plans, takedown/account workflows, and post-publish feedback loops.

Date: 2026-06-06

🟡 Medium: [survey-playbook] `contexts/survey_sessions/g_bits_game_ai_pm_interview_survey_20260603.md` turns a company-specific interview memo into a reusable AI-ops research pattern by decomposing an AI product role into concrete workflow surfaces, low-risk pilot scenarios, governance boundaries, success metrics, and a 30/60/90-day rollout path for game publishing or other operations-heavy teams.

Date: 2026-06-18

🟡 Medium: [g-bits-overseas] `contexts/survey_sessions/g_bits_injoy_overseas_publishing_pan_qinan_survey_20260617.md` captures durable near-term context for the 吉比特海外发行 AI PM interview: the role is better modeled as an internal AI workflow PM for overseas publishing, with evidence tied to official “发行-境外市场”岗位、海外收入增长、素材生产、版本管理、社群反馈和区域市场协作链路.

Date: 2026-06-20

🟡 Medium: [admissions-comparison] `contexts/survey_sessions/fujian_2025_admission_subjects_survey_20260620.md` and `tmp/fujian_2025_admission_subjects/` establish a reusable comparison pattern for choice-heavy planning questions: convert official PDF plans into structured CSVs, use `院校专业组计划数` as the primary decision metric with professional-entry counts as a secondary view, and separate plan-side coverage conclusions from unverified competition-side claims when candidate distribution data is unavailable.

Date: 2026-06-21

🟡 Medium: [publishing-cockpit-demo] `adhoc_jobs/gbits_overseas_ai_cockpit/` now packages a workflow-first overseas publishing AI cockpit as a lightweight Vite/React demo: it converts multi-region player feedback into clustered issues, risk-tagged action queues, human approval gates, and KPI回流, which is a reusable way to present AI as an operations console for发行/运营 teams rather than as a generic chatbot.

Date: 2026-06-27

🟡 Medium: [resume-positioning] `docs/resume_product_ops_engineer_ai_latest_20260626.md` turns the recent AI+业务岗位反思 into an execution-facing resume pattern: lead with concrete运营 workflow automation, context/knowledge infrastructure, alerting and capacity-response cases, and explicit人效/成本 outcomes so AI is framed as业务提效能力 rather than as generic tool familiarity or platform-style concept work for ops-heavy roles.

Date: 2026-07-05

🟡 Medium: [hardware-diagnostics] `adhoc_jobs/hardware_diagnostics/` now packages a private, evidence-first diagnostics workflow for the Ryzen 9 7900X / Gigabyte B650 machine: project-local sensor tooling, hash/signature-locked dependency tracking, snapshot/sample/profile-compare actions, and explicit human gates around BIOS, chipset, and tuning changes instead of auto-tuning.
🟡 Medium: [phone-hardware-triage] `contexts/survey_sessions/iqoo11pro_wifi_failure_survey_20260704.md` captures a reusable troubleshooting pattern for intermittent phone radio failures: treat WiFi/hotspot toggle failure as backup-first board-risk evidence, use Bluetooth联动 to separate subsystem faults from generic network issues, and limit software attempts to one official no-loss pass before escalating to written repair diagnostics and quotes.

Date: 2026-07-06

🟢 Low: [observer-quiet-window] `adhoc_jobs/`, `periodic_jobs/`, `rules/skills/`, and root docs had no new eligible post-checkpoint writes after the last observer run at 2026-07-05 20:01:17 +08:00; a widened workspace scan only surfaced the prior observer writeback in `contexts/memory/OBSERVATIONS.md`.

Date: 2026-07-08

🟡 Medium: [realtime-state-context] `contexts/daily_records/2026_05_04_to_2026_07_08_feishu_daily_context.md` and `contexts/thought_review/realtime_state_snapshot_20260708.md` capture the user's recent state shift from AI content-center experiments, resume/interview pushes, and gbit demo prep toward a clearer business-first job-search loop: build one public, experienceable deep project, train higher-signal spoken interview answers, screen hard job constraints earlier, and keep low-friction voice records as realtime context rather than unstructured diary backlog.
🟢 Low: [observer-quiet-window] `adhoc_jobs/`, `periodic_jobs/`, `rules/skills/`, root `docs/`, and the widened workspace had no new eligible post-checkpoint writes after the last observer run at 2026-07-06 23:17:04 +08:00; the only post-cutoff non-noise change was the prior observer writeback in `contexts/memory/OBSERVATIONS.md`.

Date: 2026-07-11

🔴 High: [cognitive-profile-workflow] `rules/skills/workflow_cognitive_profile_extraction.md` adds a reusable认知画像提取 workflow that treats axiom building as a multi-round, subagent-driven research system with explicit Opus routing, pressure tests, prediction-backtesting, boundary-condition handling, and a hard split between delegated evidence gathering and non-delegated final writing.
🟡 Medium: [codex-proxy-repair] `adhoc_jobs/codex_network_repair_20260711/README.md` and `contexts/thought_review/codex_windows_update_issue_log_2026_07_11.md` turn the Codex/Windows update fix into a reusable local troubleshooting pattern: let FL Clash exclusively own the WinINET proxy switch, enable Codex `respect_system_proxy`, remove persistent user proxy env vars, and reset WinHTTP to direct so apps do not keep failing against a dead `127.0.0.1:7890` proxy after the proxy client closes.

Date: 2026-07-12

🔴 High: [hardware-tuning-gates] `adhoc_jobs/hardware_diagnostics/docs/tuning_plan_review_20260712.md` upgrades the local hardware-tuning method into a stricter staged workflow: gate Windows-side CPU tuning on VBS/Ryzen Master compatibility first, treat Win11 migration as a larger performance lever than BIOS-first tweaking, re-validate DDR5-6000 baseline stability before any A/B tuning, and enforce explicit voltage/temperature abort ceilings plus BIOS re-entry verification after session-side success.
🟡 Medium: [e-drive-organization] `adhoc_jobs/e_drive_organization/organize_e_drive.py` and the added `rules/WORKSPACE.md` route establish a conservative disk-organization utility pattern: default to dry-run, move only whitelisted folder groups or extension-classified loose files, flatten only named drawer folders one level deep, keep installers as report-only candidates, and hard-exclude system directories, live app data, and the workspace itself from bulk moves.

Date: 2026-07-13

🔴 High: [mutation-safe-controller] `adhoc_jobs/hardware_tuning/` turns risky host tuning into a reusable mutation-safe controller pattern: keep `hardware_tuning -> hardware_diagnostics` as a one-way read-only dependency, persist only sanitized atomic campaign state, default stage actions to dry-run or blocked, and require per-change operator cards plus explicit human execution for BIOS or other destructive steps.
🟡 Medium: [bios-validation-mode] `adhoc_jobs/hardware_tuning/docs/rm_vbs_compatibility_20260713.md`, `adhoc_jobs/hardware_tuning/README.md`, and `adhoc_jobs/hardware_tuning/docs/decisions.md` lock the current Ryzen campaign into `bios_operator_cards_with_windows_validation`: preserve Windows 10 + WSL2/VBS, treat Ryzen Master 3.1 startup success as insufficient without stable control/readback semantics, and keep Windows tools in a read-only telemetry/WHEA-verdict role while parameters remain manual.

Date: 2026-07-15

🔴 High: [private-user-context-boundary] `.gitignore`, `rules/USER.md`, and `rules/WORKSPACE.md` now split collaboration context into a business-first default user profile plus Git-ignored `rules/private/` overlays for identity, finance, relationship, and health details, establishing an on-demand privacy boundary instead of keeping sensitive personal state in the always-loaded rule layer.
🟡 Medium: [post-flash-rm-manual-gate] `adhoc_jobs/hardware_diagnostics/docs/tuning_campaign_plan_20260712.md`, `adhoc_jobs/hardware_tuning/docs/working.md`, `adhoc_jobs/hardware_tuning/docs/operator_cards/OC-8_ryzen_master_manual_apply.md`, and `adhoc_jobs/hardware_tuning/src/HardwareTuning.psm1` shift the 7900X tuning campaign into a post-F42b delta-validation flow: verify clean JEDEC defaults after Q-Flash first, then gate CPU/RAM changes behind Ryzen Master manual diff cards, screenshot-based readback, and external telemetry while BIOS persistence switches stay off during experiments.

Date: 2026-07-18

🔴 High: [authorized-reverse-engineering] `contexts/survey_sessions/ai_models_reverse_engineering_security_survey_20260716.md` turns recent reverse-engineering model research into a reusable security workflow rule: do not treat jailbreaks or uncensored checkpoints as the main capability lever; instead separate refusal from actual RE competence and build around tool-augmented analysis, deterministic authorization, sandboxed execution, programmatic verification, and multi-model blind review.
🟡 Medium: [weekly-ai-job-radar2] `adhoc_jobs/ai_job_radar2/weekly_pipeline.py`, `adhoc_jobs/ai_job_radar2/recommendation_service.py`, `adhoc_jobs/ai_job_radar2/config/weekly_radar.json`, and `adhoc_jobs/ai_job_radar2/scripts/install_weekly_task.ps1` now package the local AI job radar as a durable weekly operating loop: fixed city/keyword coverage, business-first scoring, explicit profile-confirmation and login-risk pauses via `needs_attention`, partial-failure and JD-coverage thresholds, rule-only fallback when no model is available, and a Windows scheduled run for recurring Top 20 review.
🟡 Medium: [hermes-cn-api-playbook] `contexts/survey_sessions/hermes_cn_api_no_vpn_survey_20260717.md` captures a reusable mainland现场修复 playbook for Hermes-style agents: prefer native China providers over ad-hoc custom endpoints when available, separate failures into network/auth/protocol/Hermes four-layer checks, and treat the U-disk as a version-matched rescue bundle with installers and dependency cache rather than as raw source copy.
