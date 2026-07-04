# AI 海外游戏发行竞品调研 scratchpad

日期：2026-06-19

## Scope

调研目标：判断市面上是否已有端到端 AI 海外发行 / AI game publishing / AI mobile game marketing OS 产品，并按商业竞品线覆盖以下类别：

- AI 广告投放与 UA
- AI 创意、素材生成、creative intelligence
- ASO 与 app intelligence
- 本地化
- 评论、客服、社群
- agentic marketing 平台
- 游戏发行 service-platform

## Claim Extraction

| Claim | 来源层级 | 验证通道 | 当前状态 |
|---|---|---|---|
| CAS.AI 宣称 full-cycle / end-to-end mobile game publishing | Tier 1 官方 | 查看 CAS.AI publishing、workflow、案例；对比是否覆盖本地化、客服、社群、合规 | 证实其覆盖 UA、ASO、creative、monetization、analytics，但更像 publisher/service，不是通用 AI OS |
| Arcade 宣称 data-first、E2E launch infrastructure | Tier 1 官方 + Tier 2 媒体 | 查看 Arcade 官网、新闻、行业报道 | 证实覆盖验证、产品优化、UA、monetization、creative、data；AI 主要来自 AI.tech/adtech infrastructure，未证明全流程 autonomous |
| 主流广告平台已把 campaign setup、targeting、bidding、creative optimization AI 化 | Tier 1 官方 | 查看 Google、Meta、TikTok、AppLovin、Moloco 官方说明 | 已证实，但覆盖的是投放子流程，不覆盖发行全链路 |
| 创意智能已出现专门面向 mobile game marketer 的 AI copilot | Tier 1 官方 + Tier 2 YC/GamesBeat | Reforged Labs Boa、Segwise、Alison、Layer | 已证实，主要覆盖 ad creative research、tagging、generation、iteration，不负责媒体预算、ASO、客服、社区 |
| ASO、localization、customer support 已有成熟 AI 工具 | Tier 1 官方 | AppTweak、Lokalise、Crowdin、Zendesk、Helpshift 等 | 已证实，但都是模块化工具 |
| agentic marketing 平台可迁移到游戏发行 | Tier 1 官方 + Tier 2 媒体 | AdsGency、Salesforce、HubSpot、Demandbase、Tofu | 部分可迁移到 campaign orchestration，但原生场景偏 B2B、CRM、DTC，不懂 App Store、MMP、ROAS/LTV、游戏素材语义 |

## Provisional Judgment

当前市场存在三类接近答案：

1. 游戏发行 service-platform：CAS.AI、Arcade、Supersonic。它们最接近端到端，但本质是 publisher 或 agency/publisher hybrid，不是可由发行团队直接配置的 AI operating system。
2. 游戏增长 AI 模块：Reforged Labs Boa、Segwise、Layer、Alison、Gamelight 等。它们在游戏 UA 和素材链路很强，但局部化明显。
3. 通用 agentic marketing：AdsGency、Salesforce Agentforce、HubSpot Breeze、Demandbase Agentbase、Tofu。它们证明端到端营销 agent 方向成立，但缺少游戏发行域模型。

结论候选：尚未发现真正覆盖海外游戏发行全流程的 AI 产品。市场空白在于游戏发行专用 orchestration layer：把 UA、creative、ASO、本地化、评论客服、社群舆情、monetization 和 BI 连接成闭环，而不是替代每个底层工具。

