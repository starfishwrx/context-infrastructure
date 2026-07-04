# AI 海外游戏发行商业竞品线调研

日期：2026-06-19  
任务：深度调研子 agent 2，商业竞品线  
问题：市面上是否已有端到端 AI 海外发行 / AI game publishing / AI mobile game marketing OS 产品

## 结论先行

没有发现一个已经成熟、游戏发行专用、可自助配置的端到端 AI overseas game publishing OS。现有市场是碎片化的：广告平台把 UA 和投放优化 AI 化，创意工具把素材研究和生成 AI 化，ASO、本地化、客服和社媒各有 AI 产品，agentic marketing 平台开始覆盖通用营销编排，但它们缺少游戏发行需要的 App Store、MMP、ROAS/LTV、素材语义、区域发行、玩家支持、社区舆情、monetization 与 live ops 的统一闭环。

最接近端到端的是 CAS.AI、Arcade、Supersonic 这类 mobile game publisher / service-platform。它们能覆盖 UA、ASO、创意、变现、数据分析、产品优化等核心发行环节，但商业形态更像 publisher 或 agency/publisher hybrid，不是把海外发行岗位替换成一个 AI agent 平台。换句话说，VP 说的端到端 AI 海外发行流程，在方向上成立，但市场上还没有一个标准答案。

## 覆盖环节定义

| 缩写 | 环节 |
|---|---|
| MI | 市场/竞品/品类情报 |
| ASO | 商店页、关键词、转化率优化 |
| LOC | 本地化/翻译/多语言内容 |
| CR | 创意策略、素材生成、素材分析 |
| UA | 广告投放、预算、出价、受众、ROAS |
| MON | 广告变现、IAP、mediation、eCPM |
| BI | 数据分析、归因、LTV/ROAS/cohort |
| CS | 评论、客服、玩家支持 |
| SOC | 社媒、社群、舆情、KOL |
| LIVE | live ops、留存、活动运营 |

## 端到端游戏发行类

| 产品 | URL | 定位 | 覆盖环节 | 相关度 | 局限 | 关键摘录 |
|---|---|---|---|---|---|---|
| CAS.AI | https://cas.ai/ 和 https://cas.ai/publishing/ | 移动游戏 publisher + ad mediation/growth platform | UA, ASO, CR, MON, BI | 很高。最像 full-cycle mobile game publishing | 不是纯 AI OS；更像合作发行团队；未看到完整覆盖客服、社群、本地化、合规 | “We handle everything end-to-end”; “UA funding, ASO, ad monetization, creative production” |
| Arcade | https://arcade.com/ 和 https://arcade.com/publishing | data-first global mobile game publisher | MI, UA, CR, MON, BI, 产品优化 | 很高。2026 新发布，主打 casual / hybrid-casual 全球发行 | 仍是 publisher，不是自助 SaaS；AI 来自 AI.tech/adtech infrastructure，自动化深度未明 | “E2E launch infrastructure”; “data-first publishing” |
| Supersonic / Unity | https://supersonic.com/ | Unity mobile game publishing solution | UA, CR, MON, BI, 产品建议 | 高。成熟 hyper/hybrid-casual 发行体系 | Unity 2026 年有出售 Supersonic、关停 ironSource Ads Network 的市场信号，战略稳定性需核验 | “mobile game publishing solution” |
| AppAgent | https://appagent.com/ai-information/ | 移动增长代理/咨询，强调 UA、ASO、creative、monetization | MI, UA, ASO, CR, MON, BI | 中高。适合外部增长团队参照 | 服务公司，不是产品化 OS；强调 human strategy | “senior outside expertise across UA, ASO, creatives, data, and monetization” |
| Coda Platform historical | https://medium.com/coda-platform/coda-raises-4m-seed-funding-from-lvp-to-grow-out-mobile-game-publishing-platform-1763c32018d8 | 早期 end-to-end free-to-play/casual mobile game publishing platform | UA, BI, MON, publishing ops | 中。证明这个方向早有平台化尝试 | 后续转向 Coda Labs/Web3，再到 Coda.co/commerce 相关叙事，已不是当前 AI overseas publishing OS | “first end-to-end publishing platform” |

判断：这一组说明游戏发行确实可以平台化、数据化、AI 辅助化。但这些公司承担的是发行方角色，而不是卖给发行 PM 的端到端 AI 工作台。

## AI 广告投放和 UA

| 产品 | URL | 定位 | 覆盖环节 | 相关度 | 局限 | 关键摘录 |
|---|---|---|---|---|---|---|
| Google App Campaigns / PMax | https://support.google.com/google-ads/answer/6167162 和 https://support.google.com/google-ads/answer/10724817 | Google AI 驱动 app campaign / cross-channel performance campaign | UA, CR, BI | 很高。海外手游 UA 必备渠道 | 黑箱优化；需要高质量转化事件、素材池和归因；不负责发行策略 | “analyze hundreds of millions of signal combinations” |
| Meta Advantage+ App Campaigns | https://www.facebook.com/business/ads/meta-advantage-plus/app-campaigns | AI-optimized Facebook/Instagram app campaigns | UA, CR | 很高。移动游戏买量主渠道 | 自动化降低控制权；创意自动增强可能带来品牌风险 | “AI-optimized ... app downloads” |
| AppLovin AXON | https://legal.applovin.com/about-applovins-axon-ai/ 和 https://axon.ai/ | AppLovin Ads 背后的 AI advertising engine | UA, BI | 很高。游戏 UA/ROAS 强相关 | 平台黑箱；主要解决流量匹配和回报优化，不覆盖发行全链路 | “matching advertiser demand with publisher supply” |
| Moloco Ads | https://www.moloco.com/solutions/moloco-ads | AI-driven app performance ads | UA, BI | 高。移动应用和游戏增长 | 需要一方数据、MMP 和投放能力；不覆盖 ASO、客服、本地化 | “Acquire and re-engage high value users” |
| TikTok Smart+ App Campaigns | https://ads.tiktok.com/help/article/about-smart-plus-app-campaigns | TikTok AI app promotion campaigns | UA, CR | 很高。适合短视频素材和移动游戏拉新 | 仍局限 TikTok 生态；自动化与素材/版权控制需治理 | “powered by AI for your app promotion goals” |
| Gamelight | https://www.gamelight.io/ | 面向 mobile games 的 AI recommendation UA 平台 | UA | 高。游戏垂直，rewarded UA 相关 | 更像渠道/流量平台，不覆盖 ASO、本地化、客服等 | “AI-powered recommendation platform” |
| Liftoff | https://liftoff.ai/ | mobile growth acceleration platform | UA, CR, MON, BI | 高。移动应用增长与变现平台 | 仍是增长和 monetization stack，不是发行 OS | “scale revenue growth” |
| Unity UA / LevelPlay | https://unity.com/solutions/user-acquisition 和 https://unity.com/products/levelplay | Unity 增长与 ad mediation | UA, MON | 高。游戏开发与变现生态强关联 | 发行链路覆盖有限；更多是渠道和变现基础设施 | “Reach players who want to engage” |

判断：UA 平台已经高度 AI 化，但它们的 AI 是 media buying engine。它能执行投放优化，不会替发行团队决定产品定位、市场优先级、本地化策略、素材叙事、社区运营和客服闭环。

## AI 创意、素材与 Creative Intelligence

| 产品 | URL | 定位 | 覆盖环节 | 相关度 | 局限 | 关键摘录 |
|---|---|---|---|---|---|---|
| Reforged Labs Boa | https://reforgedlabs.com/ 和 https://reforgedlabs.com/blog/reforged-labs-launches-boa | mobile game marketers 的 AI creative intelligence copilot | MI, CR, UA insight | 很高。游戏垂直、素材策略强相关 | 不负责投放执行、ASO、本地化、客服 | “purpose-built for mobile games”; “what to create next” |
| Layer AI | https://www.layer.ai/industries/mobile-games | game studios 的 AI creative OS / asset production | CR, ASO素材, LIVE素材 | 高。游戏素材、UA creative、liveops 内容 | 偏生产工具，不做预算投放和发行决策 | “UA creatives, and LiveOps content 3-5x faster” |
| Alison.ai | https://alison.ai/ | creative intelligence for gaming marketers | CR, UA insight | 高。分析素材元素和表现关系 | 更偏分析与生成建议，不是发行系统 | “data-driven creative intelligence” |
| Segwise | https://segwise.ai/ | mobile app/game creative analytics and generation | CR, UA insight | 高。跨广告网络创意标签、疲劳监控 | 依赖已有投放数据；不覆盖 ASO/客服/本地化 | “tag and analyze creatives across 15+ networks” |
| Creatify | https://creatify.ai/ | AI video/image ad generator | CR | 中。可用于游戏广告素材，但偏电商 URL-to-video | 游戏语义、玩法表达、合规和渠道反馈较弱 | “Generate ... video ads ... from any URL” |
| Arcads | https://www.arcads.ai/ | AI UGC/video ad creation | CR, LOC轻量 | 中。可做 UGC 风格素材、多语种变体 | 游戏素材真实性、平台政策、版权和品牌控制需人工治理 | “Create better video ads with AI” |
| Quickads | https://www.quickads.ai/ | AI analysed ads library + ad generation | MI, CR | 中。适合素材趋势研究 | 泛广告平台，游戏专属能力有限 | “30 million ads” |
| AdCreative.ai | https://www.adcreative.ai/ | AI ad creative generator | CR | 中。横向广告素材生成 | 泛营销工具，游戏玩法创意和 UA 数据闭环弱 | “ad creatives, images, videos, and copy” |
| Scenario | https://www.scenario.com/ | game-ready assets and marketing creatives | CR | 中高。游戏资产生成相关 | 偏资产生成，不覆盖发行流程 | “game-ready assets at scale” |

判断：这一层是当前最接近游戏发行 AI 产品经理机会点的市场。特别是 Reforged、Segwise、Layer、Alison，已经把游戏素材从人工经验转向 data + AI。但它们都在素材和创意决策局部环节。

## ASO 与 App Intelligence

| 产品 | URL | 定位 | 覆盖环节 | 相关度 | 局限 | 关键摘录 |
|---|---|---|---|---|---|---|
| AppTweak Atlas AI | https://www.apptweak.com/en/atlas-ai | app store 专用 AI intelligence layer | ASO, MI, Apple Ads | 高。海外发行商店增长强相关 | 不执行 UA、客服、社区、变现；更像 ASO/Apple Ads 智能层 | “built exclusively for the app stores” |
| Sensor Tower | https://sensortower.com/ | digital/app market intelligence | MI, ASO, ad intelligence | 高。竞品、下载、收入、广告情报 | 数据情报工具，不是执行系统；价格和访问门槛较高 | “downloads and engagement ... ads served” |
| MobileAction | https://www.mobileaction.co/ | apps and games growth intelligence / ASO / Apple Ads | MI, ASO, UA辅助 | 高。ASO 和 Apple Ads 有用 | 仍偏增长情报和优化，不覆盖端到端 | “Grow apps and games” |
| AppFollow | https://appfollow.io/ | AI review management + ASO/reputation | ASO, CS, BI | 高。评论、评分、商店反馈闭环 | 不覆盖买量和素材生产；ASO 深度弱于专门 ASO 平台 | “manage user reviews, analyze user sentiment” |

判断：ASO AI 工具的边界非常明确。它们能做商店页和 app intelligence，但与广告素材、MMP 归因、客服和社区之间通常没有统一 agent workflow。

## 本地化

| 产品 | URL | 定位 | 覆盖环节 | 相关度 | 局限 | 关键摘录 |
|---|---|---|---|---|---|---|
| Lokalise | https://lokalise.com/ 和 https://lokalise.com/ai/ | AI-powered continuous localization platform | LOC | 高。游戏多语言版本、商店页、客服文本都可用 | 本地化工具，不判断市场优先级、投放、社区语境 | “continuous localization”; “smart routing with multiple LLMs” |
| Smartling | https://www.smartling.com/ | end-to-end localization & translation platform | LOC | 中高。适合企业级多内容本地化 | 游戏专属语境和发行闭环需额外配置 | “AI across every layer” |
| Phrase | https://phrase.com/ | enterprise AI localization platform | LOC | 中高。软件、游戏、营销内容可接入 | 仍是本地化中台，不是发行编排层 | “automate workflows ... global content” |
| Crowdin | https://crowdin.com/ 和 https://crowdin.com/solutions/mobile-app-localization-services | AI-powered localization platform | LOC | 高。开发者友好，适合 mobile app localization | 不负责文化化创意、当地投放和社群运营 | “700+ apps and integrations”; “mobile app localization” |

判断：本地化环节已经很成熟。真正缺的是把 LOC 输出与 ASO、广告素材、客服话术、社区内容、地区测试数据连接起来的发行记忆和决策闭环。

## 评论、客服、社群和舆情

| 产品 | URL | 定位 | 覆盖环节 | 相关度 | 局限 | 关键摘录 |
|---|---|---|---|---|---|---|
| AppFollow | https://appfollow.io/app-review-management-tool | app review aggregation/reply automation | CS, ASO | 高。App Store/Google Play 评论运营强相关 | 主要覆盖商店评论，不覆盖 Discord/Reddit/KOL 全域社区 | “reply to app reviews with ... AI” |
| Zendesk AI | https://www.zendesk.com/service/ai/ | AI customer service platform | CS | 中高。可迁移到海外玩家客服 | 泛客服；in-game SDK、游戏账号/补偿流程需集成 | “AI agents ... any channel” |
| Helpshift | https://www.helpshift.com/ | AI-native player engagement platform for games | CS, SOC, trust & safety | 很高。游戏垂直客服和玩家支持 | 更偏支持/安全/社区，不覆盖 UA、ASO、素材 | “AI-Native Player Engagement Platform for Games” |
| Sprinklr | https://www.sprinklr.com/products/consumer-intelligence/social-listening/ | enterprise social listening / CX | SOC, CS, BI | 中。可用于舆情、社媒、品牌风险 | 泛企业套件，游戏社区语境需配置 | “500 million daily conversations” |
| Brandwatch | https://www.brandwatch.com/ | AI social media management / consumer intelligence | SOC, KOL, BI | 中。适合海外舆情和 influencer | 不接发行投放和游戏内数据 | “consumer intelligence, and influencer marketing” |
| Hootsuite | https://www.hootsuite.com/ | social media management + AI | SOC | 中。适合社媒排期、监听、摘要 | 泛社媒工具，不是游戏发行 OS | “automate every part of social media management” |

判断：玩家支持是游戏发行全链路中最容易被忽视的一段。Helpshift 是该环节最游戏垂直的产品，但它不会替代 UA/ASO/创意系统。

## Agentic Marketing 平台

| 产品 | URL | 定位 | 覆盖环节 | 相关度 | 局限 | 关键摘录 |
|---|---|---|---|---|---|---|
| AdsGency | https://adsgency.ai/ | AI ad ops / agentic advertising platform | MI, CR, UA, BI | 中高。端到端 campaign automation 形态最接近 | 泛广告，不是游戏发行；App Store/MMP/LTV/素材语义需适配 | “ad creation, targeting, automation, and analytics” |
| Salesforce Agentforce / Marketing Cloud Next | https://www.salesforce.com/agentforce/ 和 https://www.salesforce.com/marketing/agentic-marketing/ | enterprise agentic marketing/customer platform | CRM, campaign, CS | 中。证明大厂在做 agentic marketing | CRM/企业营销导向；游戏发行场景过重、集成成本高 | “complete agentic marketing solution” |
| HubSpot Breeze | https://www.hubspot.com/products/artificial-intelligence/breeze-ai-agents | AI agents for marketing, sales, service | CRM, content, CS | 低到中。适合轻量 GTM，不适合游戏发行核心 | B2B/SMB CRM 语境，缺游戏渠道和数据模型 | “AI Agent Growth Team” |
| Demandbase Agentbase | https://www.demandbase.com/products/agentbase-ai-agents/ | B2B GTM connected AI agents | ABM, GTM, BI | 低到中。理念可迁移 | ABM/销售市场一体化，基本不是游戏发行 | “connected AI agent system” |
| Tofu | https://www.tofuhq.com/ | agentic demand gen / ABM content campaigns | content, ads, landing pages | 低到中。campaign personalization 可借鉴 | B2B demand gen，不懂移动游戏商店和买量 | “campaigns across email, landing pages, and ads” |

判断：agentic marketing 说明端到端营销 agent 已经开始商业化，但迁移到游戏海外发行需要重做领域模型、数据接口和治理规则。最有参考价值的是 AdsGency 的跨渠道广告 agent 形态，其次是 Salesforce/HubSpot 的 agent + CRM + workflow 设计。

## 竞品矩阵

| 类型 | 代表产品 | 端到端程度 | 游戏垂直度 | AI 自主性 | 最适合借鉴的点 |
|---|---|---:|---:|---:|---|
| 游戏 publisher/service-platform | CAS.AI, Arcade, Supersonic | 高 | 高 | 中 | 发行流程拆解、数据驱动 scaling、publisher 角色边界 |
| UA / ad network AI | Google, Meta, AppLovin, Moloco, TikTok, Gamelight | 中 | 中到高 | 高 | 自动出价、受众探索、素材组合测试、ROAS 优化 |
| Creative intelligence | Reforged, Segwise, Alison, Layer | 中 | 高 | 中到高 | 玩法/素材语义标签、竞品广告理解、brief 生成 |
| ASO / app intelligence | AppTweak, Sensor Tower, MobileAction, AppFollow | 低到中 | 中 | 中 | 商店数据、关键词、竞品追踪、评论洞察 |
| Localization | Lokalise, Smartling, Phrase, Crowdin | 低 | 低到中 | 中 | continuous localization、术语库、AI + human QA |
| Player support/community | Helpshift, Zendesk, Sprinklr, Brandwatch, Hootsuite | 低到中 | Helpshift 高，其余中低 | 中 | 玩家支持、评论自动回复、社群舆情摘要 |
| Agentic marketing | AdsGency, Agentforce, Breeze, Demandbase, Tofu | 中 | 低 | 中到高 | 多 agent 编排、campaign planning/execution/optimization |

## 对吉比特海外发行 AI 产品经理面试的含义

可以把 VP 的命题拆成两层回答：

第一层：海外发行所有工作都能被 AI 辅助或半自动执行，这个判断基本成立。市场已经证明 UA、创意、ASO、本地化、客服、社媒和营销编排各环节都有成熟 AI 产品。

第二层：直接端到端自动发行，目前还没有被单一产品完整解决。原因不是模型能力不足，而是发行链路跨越多个系统和责任边界：广告平台、MMP、App Store、素材库、本地化 TMS、客服系统、社媒平台、数据仓库、游戏内事件、收入和留存模型。现有工具各自优化一个局部目标，缺少统一的 game publishing memory 和决策控制面。

如果要提出产品方案，合理定位不是做另一个素材生成器或 ASO 工具，而是做 AI overseas publishing cockpit：

1. 接入 MMP、广告平台、商店后台、素材库、客服评论、本地化系统和 BI。
2. 建立游戏、地区、玩家、创意、渠道、版本的统一对象模型。
3. 让 agent 先做建议和执行草案：市场优先级、素材 brief、ASO 文案、本地化检查、评论回复、投放实验、ROAS 复盘。
4. 在高风险动作上保留审批：预算变更、素材上线、客服补偿、社媒发布、商店页发布。
5. 用每轮投放和商店反馈更新发行知识库，形成持续学习闭环。

最小可行 MVP 建议聚焦 creative + UA + ASO 的闭环。因为这三个环节距离收入最近，数据反馈最快，也最能体现 AI 产品经理的价值：把创意洞察转成素材 brief，把投放数据转成下一轮测试计划，把商店页转化和评论反馈反哺广告叙事。

最终判断：商业市场已经有足够多的模块化 AI 能力，但端到端 AI 游戏海外发行仍是未充分产品化的空白。吉比特如果要做，机会不在底层大模型，而在游戏发行领域流程、数据接口、审批治理和人机协作产品设计。

