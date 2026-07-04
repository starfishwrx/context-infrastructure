# Subagent Outputs - AI Overseas Game Publishing E2E Survey

Date: 2026-06-19

## Hubble - Feasibility and Architecture

Core conclusion: VP's claim should be reframed as: most operational work in overseas publishing can be executed by AI, but the end-to-end loop must be layered. AI can run processes, generate candidates, summarize data, trigger tasks and execute low-risk actions; humans must retain responsibility for market judgment, brand tone, budget, compliance, player commitments and crisis handling.

Key outputs:

- Automation levels: L0 manual, L1 copilot, L2 workflow, L3 supervised agent, L4 autonomous closed loop.
- High-automation candidates: data capture, review clustering, ticket routing, asset tagging, daily/weekly reports, competitor monitoring, ASO drafts, low-risk FAQ replies, low-budget ad tests, task reminders.
- L3 candidates: market research, competitor monitoring, creative production, UA review, community sentiment, CS assistant, version ops assistant.
- Human decision boundaries: market entry, positioning, major budget changes, KOL negotiation, PR crisis, player compensation, gacha/probability wording, privacy compliance, release go/no-go.
- Proposed system: AI overseas publishing OS with market, competitor, localization, ASO, creative, UA, KOL/PR, community, CS/review, version ops, data review and compliance/budget agents.

## Godel - Commercial Competitor Landscape

Core conclusion: no mature, game-overseas-publishing-specific, self-serve end-to-end AI publishing OS was found. The closest references are CAS.AI, Arcade and Supersonic as publisher/service-platform models. Mature capabilities are fragmented across UA, creative intelligence, ASO, localization, review/customer support and generic agentic marketing.

Most relevant competitor clusters:

- Publisher/service-platform: CAS.AI, Arcade, Supersonic.
- UA/ad AI: Google App Campaigns, Meta Advantage+, AppLovin AXON, Moloco, TikTok Smart+, Gamelight, Liftoff, Unity UA/LevelPlay.
- Creative intelligence/production: Reforged Labs Boa, Layer AI, Alison.ai, Segwise, Creatify, Arcads, Quickads, AdCreative.ai, Scenario.
- ASO/app intelligence: AppTweak Atlas AI, Sensor Tower, MobileAction, AppFollow.
- Localization: Lokalise, Smartling, Phrase, Crowdin.
- Player support/community: AppFollow, Zendesk AI, Helpshift, Sprinklr, Brandwatch, Hootsuite.
- Agentic marketing: AdsGency, Salesforce Agentforce, HubSpot Breeze, Demandbase, Tofu.

Strategic implication: the opportunity is not a new single-point tool. It is a game publishing orchestration layer connecting UA, creative, ASO, localization, reviews, community, monetization and BI with approvals.

## Maxwell - Open Source References

Core conclusion: open source can assemble an end-to-end MVP, but it is better suited for a publishing cockpit, data hub, draft generation, analysis recommendations and human approval workflow. Real production needs official store APIs, ad APIs, MMP, internal telemetry and approval controls.

Recommended MVP stack:

- Agent state machine: LangGraph.
- External workflow/integration: n8n.
- Quick prototype surfaces: Dify or Flowise.
- Localization: Weblate or Tolgee; LibreTranslate as a baseline/self-hosted translation layer.
- Creative generation: ComfyUI, InvokeAI, Stable Diffusion WebUI/Forge, Wan video workflows where appropriate.
- Data ingestion: Airbyte or Meltano.
- Product analytics and experimentation: PostHog and GrowthBook.
- BI: Metabase or Superset.
- LLM observability/eval: Langfuse and Promptfoo.
- Community/support integrations: discord.js/discord.py, Rasa and official Apple/Google review APIs.

Boundary: open-source scrapers are useful for public competitor monitoring but should not replace official Apple/Google APIs for production operations.

## Lovelace - Risk, Counter-Evidence and Governance

Core conclusion: the VP's direction can be accepted, but it must be calibrated into "end-to-end AI workflow", not "end-to-end unmanned decision-making." AI can automate creative drafts, UA reports, review clustering, multilingual drafts, sentiment alerts and weekly reports; budget, external publishing, player commitments, copyright, compliance, privacy and crisis handling require human review, permissions and audit.

Key counter-evidence:

- AI ad platforms are powerful but can be black-box systems with limited controls and attribution ambiguity.
- Meta AI ad cases show creative automation can generate and run inappropriate ads.
- Air Canada chatbot liability shows companies remain responsible for AI-generated external commitments.
- DPD chatbot incident shows public-facing bots are prompt-injection and brand-risk surfaces.
- SKAN and modeled conversions mean platform ROAS does not equal true incrementality.
- n8n, Flowise and LangChain ecosystem advisories show workflow/agent stacks can expose RCE, file access and prompt-injection risks if over-permissioned.

Controls recommended:

- Default read-only agents.
- Read/write token separation.
- Budget hard limits.
- External publishing whitelist.
- Sensitive data desensitization.
- Secret broker outside prompts.
- Privileged tool isolation.
- No self-approval by agents.
- Full audit logs.
- Kill switch and rollback for publishing, social, campaign and workflow actions.
