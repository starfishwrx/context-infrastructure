# Search Manifest - AI Overseas Game Publishing E2E Survey

Date: 2026-06-19

## Research Question

VP claim: "All overseas publishing work can be executed by AI."  
Survey goals:

1. Feasibility: whether a direct end-to-end AI overseas publishing workflow is viable.
2. Competitors: whether similar AI products or competitors exist.
3. Open source: whether public projects can be used as references.

## Skill Workflow Applied

Workspace skill: `rules/skills/workflow_deep_research_survey.md`

Workflow phases:

1. Initial scan and claim extraction.
2. Parallel subagent research by dimension.
3. Cross-validation and synthesis.
4. Internal memo/report written to `contexts/survey_sessions/`.

## Subagent Split

| Agent | Dimension | Output |
|---|---|---|
| Hubble | Feasibility and architecture | Overseas publishing automation levels, task-by-task feasibility, AI publishing OS architecture. |
| Godel | Commercial competitors | Existing publisher/service-platforms, UA automation, creative intelligence, ASO, localization, player support, agentic marketing tools. |
| Maxwell | Open source references | Agent orchestration, workflow automation, data pipelines, localization, creative generation, BI/experimentation, LLM eval/observability. |
| Lovelace | Risks and counter-evidence | Ad-platform black boxes, AI content failures, chatbot liability, attribution limits, security and governance controls. |

## Representative Queries

| Query Theme | Queries |
|---|---|
| End-to-end game publishing platforms | `CAS.AI publishing mobile game end-to-end UA ASO ad monetization creative production`; `Arcade mobile game publishing E2E launch infrastructure AI.tech adtech infrastructure`; `Supersonic mobile game publishing solution` |
| UA automation | `Google App Campaigns automatically optimizes app ads`; `AppLovin AXON AI advertising engine`; `Meta Advantage+ app campaigns AI optimized`; `TikTok Smart+ app campaigns AI` |
| Creative intelligence | `Reforged Labs Boa AI creative intelligence platform mobile games`; `Layer AI mobile games UA creatives LiveOps content`; `Segwise mobile game creative analytics AI` |
| ASO and review management | `AppTweak Atlas AI ASO Agent Reviews Agent Ad Agent`; `AppFollow AI review management respond to app reviews any language` |
| Localization | `Lokalise AI continuous localization workflow`; `Phrase AI localization platform`; `Crowdin mobile app localization AI` |
| Open source orchestration | `LangGraph durable execution human-in-the-loop`; `n8n workflow automation native AI integrations`; `Dify LLM app platform workflow agent`; `Flowise build AI agents visually` |
| Open source business stack | `Airbyte connectors open source`; `Weblate continuous localization system`; `Tolgee translation management`; `ComfyUI node based AI workflow`; `PostHog open source product analytics`; `GrowthBook open source feature flags experiments`; `Langfuse open source LLM observability`; `Promptfoo LLM eval red teaming` |
| Risk and governance | `Meta AI generated ads Advantage+ bizarre ads`; `Air Canada chatbot liability`; `OWASP LLM Top 10 excessive agency`; `n8n critical vulnerability Python Code Node`; `Flowise security advisory arbitrary file read` |

## Claim Extraction

| Claim | Status After Survey |
|---|---|
| All overseas publishing work can be executed by AI. | Partly true if "execute" means AI performs drafts, analysis, workflow routing and low-risk actions. False if it means no human decision or approval. |
| A mature end-to-end AI overseas game publishing OS already exists. | Not supported. The market is fragmented into strong modules; publisher/service-platforms are closest but are not self-serve AI OS products. |
| UA is the most automatable link. | Supported. Google, Meta, AppLovin, Moloco and TikTok all show high automation, but black-box optimization and attribution limitations remain. |
| Creative and ASO are good AI PM entry points. | Supported. Commercial tools show mature local capabilities and clear data feedback loops. |
| Open source can build an MVP. | Supported. LangGraph/n8n/Dify/Flowise plus data/localization/creative/BI/eval tools can prototype a controlled publishing cockpit. |
| Fully autonomous production is high risk. | Supported. External content, budgets, user rights, privacy, IP, platform policy and security require approvals and auditability. |
