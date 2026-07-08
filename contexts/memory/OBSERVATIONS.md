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
