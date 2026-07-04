# Scratchpad: 端到端 AI 海外发行流程调研

调研日期：2026-06-19  
Reader mode：Internal memo  
目标：回应“海外发行所有工作都可以用 AI 执行，是否可以做直接端到端 AI 海外发行流程”的 VP 观点，完成可行性、竞品、开源参考三类调研。

## Phase 1 初步扫描

初扫方向：

- AI 广告与买量自动化：Google App Campaigns、Meta Advantage+、AppLovin AXON、Moloco、Reforged Labs、Layer AI、Alison.ai 等。
- ASO / App review / 本地化：AppTweak Atlas AI、AppFollow、Lokalise、Smartling 等。
- 开源 agent / workflow / LLMOps：LangGraph、Dify、Flowise、n8n、Langfuse、Promptfoo、Tolgee、LibreTranslate、ComfyUI、app-store-scraper、google-play-scraper 等。
- 风险边界：广告平台自动化失控、生成素材品牌/合规风险、开源 agent/workflow 安全漏洞、预算权限、隐私与平台政策。

## Claim Extraction

| Claim | 来源层级 | 初始来源 | 验证通道 | 验证状态 |
|---|---|---|---|---|
| “海外发行所有工作都可以由 AI 执行” | VP 观点 / 业务假设 | 用户二面反馈 | 将发行链路拆成任务类型，逐项评估自动化等级、权限、风险、人审需求 | 待验证 |
| 市场上已有成熟端到端 AI 海外发行产品 | 待验证市场 claim | 初扫未见完整产品 | 查广告代理、MarTech agent、mobile game marketing AI、ASO/localization/review 工具 | 待验证 |
| 当前竞品更多是局部工具，而非全流程发行 OS | 初步推断 | 初扫结果 | 竞品矩阵覆盖：广告投放、素材、ASO、本地化、评论/社群、agent 编排 | 待验证 |
| 买量投放是最接近自动闭环的环节 | Tier 1 平台官方 claim | Google、Meta、AppLovin、Moloco | 官方文档 + 独立负面案例验证平台自动化边界 | 待验证 |
| 素材生产和创意洞察已有游戏垂直 AI 工具 | Tier 1 厂商 claim | Reforged Labs、Layer AI、Alison.ai | 官方文档、媒体报道、客户案例、功能边界 | 待验证 |
| 本地化、ASO、评论管理已有可用 AI SaaS | Tier 1 厂商 claim | Lokalise、Smartling、AppTweak、AppFollow | 官方文档、功能边界、API/自动化能力 | 待验证 |
| 开源项目足以搭建原型，但不足以直接生产级运营 | 初步推断 | LangGraph、Dify、n8n、ComfyUI 等 | GitHub/文档/安全事件/维护状态/集成能力 | 待验证 |
| 端到端可行形态应是“AI 发行操作系统 + 人审闸口”，不是“全自动无人发行” | 初步判断 | 根据自动化边界 | 与竞品、开源和风险证据交叉验证 | 待验证 |

## Phase 2 分割计划

4 条线并行，overlap 约 40%：

1. 可行性与流程架构：拆海外发行任务，评估哪些可以 AI 端到端执行，哪些需要人审。
2. 商业竞品：找 AI mobile game marketing、ad tech、ASO、本地化、评论管理、agentic marketing 产品。
3. 开源参考：找 agent/workflow、素材生成、本地化、评论采集、LLMOps/eval 等可参考项目。
4. 风险与反证：找自动化广告、生成素材、agent workflow、平台 API、隐私合规的失败/边界案例。

## 待补

- subagent 输出摘要
- source index
- claim verification
- 最终报告

## Phase 3 交叉验证后的 Claim Verification

| Claim | 最终判断 | 依据 |
|---|---|---|
| “海外发行所有工作都可以由 AI 执行” | 部分成立 | 如果“执行”指草稿、分析、路由、低风险动作和流程编排，则成立；如果指无人决策、无人外发、无人预算控制，则不成立。 |
| 市场上已有成熟端到端 AI 海外发行产品 | 未发现支持 | 现有市场以模块化工具为主；CAS.AI、Arcade、Supersonic 接近端到端发行服务，但不是内部自助式 AI publishing OS。 |
| 当前竞品更多是局部工具，而非全流程发行 OS | 支持 | UA、创意、ASO、本地化、客服、社群、BI、agentic marketing 均有强工具，但缺统一游戏发行数据模型和审批控制面。 |
| 买量投放是最接近自动闭环的环节 | 支持 | Google App Campaigns、Meta Advantage+、AppLovin AXON、Moloco、TikTok Smart+ 均说明 UA 高度自动化，但存在黑箱和归因风险。 |
| 素材生产和创意洞察已有游戏垂直 AI 工具 | 支持 | Reforged Labs Boa、Layer、Segwise、Alison.ai 等显示游戏素材 AI 进入垂直化阶段。 |
| 本地化、ASO、评论管理已有可用 AI SaaS | 支持 | Lokalise、Phrase、Crowdin、AppTweak、AppFollow、Helpshift 等工具已有成熟能力。 |
| 开源项目足以搭建原型，但不足以直接生产级运营 | 支持 | LangGraph/n8n/Dify/Flowise 等可拼 MVP；生产必须补官方 API、权限、审批、审计、安全和数据治理。 |
| 端到端可行形态应是“AI 发行操作系统 + 人审闸口”，不是“全自动无人发行” | 强支持 | 可行性、竞品、开源和风险线均收敛到同一结论。 |

## Phase 4 输出文件

- 最终报告：`contexts/survey_sessions/ai_overseas_publishing_e2e_standard_survey_20260619.md`
- 商业竞品子报告：`contexts/survey_sessions/ai_game_publishing_competitors_survey_20260619.md`
- 风险边界子报告：`contexts/survey_sessions/g_bits_overseas_ai_publishing_risk_boundaries_survey_20260619.md`
- 搜索清单：`tmp/ai_overseas_publishing_e2e_20260619/search_manifest.md`
- 来源索引：`tmp/ai_overseas_publishing_e2e_20260619/source_index.md`
- 子 agent 输出摘要：`tmp/ai_overseas_publishing_e2e_20260619/subagent_outputs.md`

## 最终口径

> 我同意 VP 的方向，但我会把它定义成端到端 AI workflow，而不是端到端无人决策。AI 负责速度、覆盖和证据，人负责目标、边界和问责。
