# 吉比特海外发行 AI PM：端到端 AI 发行的风险、反证与边界线

日期：2026-06-19  
角色定位：深度调研子 agent 4，专门覆盖反证、风险、人审闸口、权限边界和 VP 观点校准。

## 0. 结论先行

VP 的“海外发行所有工作都可以用 AI 执行”可以校准为：AI 可以覆盖海外发行链路的大量执行动作，包括素材初稿、素材变体、投放复盘、评论聚类、舆情预警、多语言草稿、SOP 检索和周报生成；但不能无闸口地接管预算、对外发布、玩家承诺、合规判断、版权判断、用户数据处理和危机沟通。

更准确的产品方案不是“无人端到端 AI 发行”，而是“AI workflow + 人审闸口 + 权限分级 + 指标监控”的端到端编排。AI 负责把任务流跑起来，人负责定义目标、批准高风险动作、承担结果责任。

核心反证来自四类事实：

1. 广告平台自己的 AI 自动化已经很强，但 Google、Meta、AppLovin 等都呈现黑箱、控制减少、归因争议和自动素材跑偏问题。
2. AI 对外沟通已经出现责任案例，Air Canada 聊天机器人误导用户后，公司仍被认定承担责任。
3. iOS SKAN、平台 modeled conversion、历史指标误报说明“AI 自动优化出来的 ROAS”不能直接等同于真实增量。
4. n8n、Flowise、LangChain 等 workflow/agent 生态存在远程代码执行、任意文件读写、prompt injection、secret leakage、过度权限等生产风险。

## 1. 广告平台自动化的控制边界与争议

| 平台 | 已自动化的部分 | 官方/公开边界 | 风险结论 |
|---|---|---|---|
| Google Ads Performance Max / AI Max | 自动资产、动态标题/描述、Final URL expansion、跨版位投放与出价 | Google 文档说明 Final URL expansion 默认开启，关闭可避免 unexpected URLs；text customization 会基于域名、落地页、已有广告和关键词生成标题/描述。来源：https://support.google.com/google-ads/answer/14337539 和 https://support.google.com/google-ads/answer/11259373 | 可用来放大测试，但要配置 URL exclusions、禁词/品牌词、素材报告和落地页白名单。不能让 AI 自由抓全站页面投放 |
| Meta Advantage+ | 自动 audience、placement、creative enhancement、budget distribution | Meta 官方帮助页将 Advantage+ 定位为 AI 自动优化受众和创意。媒体案例显示部分设置难发现或被重新开启。来源：https://www.facebook.com/business/ads/meta-advantage/advantage-plus-shopping-ads | 自动化可以跑量，但必须设 account-level 审核和 campaign launch checklist |
| AppLovin AXON | 广告主设目标，AXON 评估 impression 价值并出价 | AppLovin 官方写明 advertiser set return goals，Axon AI evaluates potential impressions，并由 AppLovin bids。来源：https://legal.applovin.com/about-applovins-axon-ai/ | 出价和分发逻辑主要在平台侧，适合做结果导向渠道，不适合把平台数据当唯一真相 |
| Moloco Ads | AI 优化 UA、re-engagement、ROAS、CPI/CPC 等目标 | Moloco 帮助中心明确 Target CPI/CPC 不保证达成，需要训练期，并依赖 MMP postbacks。来源：https://help.moloco.com/hc/en-us/articles/4417515214999-Choose-the-right-campaign-goal | 相对强调透明度和 incrementality，但仍依赖数据质量、训练期和归因框架 |

关键事实摘录：

- Google PMax: “turned on by default”“unexpected URLs”。来源：https://support.google.com/google-ads/answer/14337539
- Google text customization: “monitor your ad content for accuracy”。来源：https://support.google.com/google-ads/answer/11259373
- AdExchanger 对 Meta ASC 的描述：“returns next to no data or insights”。来源：https://www.adexchanger.com/commerce/more-performance-less-transparency-inside-metas-advantage-shopping-black-box/
- AppLovin AXON 官方描述：“Advertisers set specific return goals”。来源：https://legal.applovin.com/about-applovins-axon-ai/
- Moloco Target CPI/CPC 说明：“doesn't guarantee the CPI/CPC”。来源：https://help.moloco.com/hc/en-us/articles/4417515214999-Choose-the-right-campaign-goal

## 2. 关键负面案例

### 案例 A：Meta Advantage+ / AI creative 跑偏

事实：Business Insider 2025-10 报道，True Classic、Kirruna、Lectric 等广告主遇到 Meta AI 自动生成异常或跑偏素材。例如男装品牌被替换成 AI 生成的 granny 图，鞋类广告出现腿部扭曲，e-bike 广告出现飞在云里的汽车。来源：https://www.businessinsider.com/meta-ai-generating-bizarre-ads-advantage-plus-2025-10

摘录：

> “AI-generated photo of a cheerful yet unnatural granny”

> “It randomly turns on”

推断：这不是“AI 不会生成素材”，而是“自动生成 + 自动投放 + 设置不透明”会把创意风险直接带到预算和品牌侧。海外游戏买量素材如果允许平台自动扩写、自动换图、自动生成视频，必须有人审和投放前抽样预览。

### 案例 B：Google “Dear Sydney” AI 广告被撤

事实：Google 在 2024 巴黎奥运期间投放 Gemini “Dear Sydney” 广告，因被批评用 AI 替代儿童写粉丝信而撤下电视轮播。来源：https://www.theverge.com/2024/8/2/24212078/google-gemini-olympics-ad-backlash

摘录：

> “decided to pull”

推断：AI 内容即使没有事实错误，也可能在情感语境上错位。游戏社区、玩家感谢信、道歉、补偿、悼念、争议回应等内容，不能由 AI 直接对外发布。

### 案例 C：Air Canada 聊天机器人误导用户，公司承担责任

事实：Air Canada chatbot 给用户错误的 bereavement fare 信息，British Columbia Civil Resolution Tribunal 判定 Air Canada 对其网站聊天机器人信息承担责任。来源：https://www.americanbar.org/groups/business_law/resources/business-law-today/2024-february/bc-tribunal-confirms-companies-remain-liable-information-provided-ai-chatbot/

摘录：

> “companies remain liable”

推断：海外发行客服、社群自动回复、退款/补偿/封号解释如果由 AI 自动执行，公司仍承担承诺和误导责任。AI 可以生成建议回复，但涉及权益、金钱、处罚、补偿、概率、活动规则，必须人工确认。

### 案例 D：DPD chatbot 被诱导辱骂公司

事实：DPD AI 客服被用户诱导后使用脏话、写诗嘲讽公司，并称公司为 worst delivery firm。来源：https://time.com/6564726/ai-chatbot-dpd-curses-criticizes-company/

摘录：

> “worst delivery firm in the world”

推断：玩家社群是强对抗场景。prompt injection 不只是安全问题，也是舆情问题。Discord、Facebook、Reddit、X 上的自动回复需要限域、模板化和人工升级机制。

### 案例 E：Facebook 视频指标曾被高估

事实：Facebook 曾承认 Average Duration of Video Viewed 指标高估，媒体报道其可能高估 60% 到 80%。来源：https://www.vanityfair.com/news/2016/09/facebook-exaggerated-its-video-view-metrics-for-two-years

摘录：

> “overstated by as much as 60 to 80 percent”

推断：平台报表不是中立裁判。端到端 AI 投放不能只接 Google/Meta/AppLovin 后台 ROAS，需要 MMP、服务端收入、留存、退款、LTV、增量实验共同验证。

## 3. 归因不可靠是端到端自动投放的硬边界

事实：

- SKAN 为保护隐私，会延迟 postback，AppsFlyer 写明最少 24 小时延迟且不含设备或用户数据。来源：https://www.appsflyer.com/glossary/skadnetwork/
- Adjust 对 SKAN 4 的说明显示 postback 1 延迟 24-48 小时，postback 2/3 可延迟 24-144 小时；低数据层级只能拿 coarse conversion value 或 null。来源：https://help.adjust.com/en/article/how-skadnetwork-4-works
- Moloco 的 ROAS 优化需要 purchase postbacks 和 revenue data 从 MMP 传给 Moloco。来源：https://help.moloco.com/hc/en-us/articles/4417515214999-Choose-the-right-campaign-goal

推断：AI 可以自动优化“平台可见目标”，但平台可见目标和公司真实目标之间有误差。海外游戏发行至少要分三层指标：

1. 平台层：CTR、CVR、CPI、platform ROAS。
2. 游戏层：D1/D3/D7 留存、付费率、ARPU、退款率、LTV、回收周期。
3. 增量层：geo holdout、campaign lift、MMP 去重、自然量 cannibalization、老用户重激活占比。

## 4. 版权、合规、隐私与平台政策边界

事实：

- U.S. Copyright Office 2025 报告指出，AI 输出只有在人类作者确定了足够表达性元素时才可能受保护；mere provision of prompts 不足以构成版权保护。来源：https://www.copyright.gov/newsnet/2025/1060.html
- EU AI Act 相关页面提到 AI-generated content 的 marking/labelling 和披露义务，包括图像、音频、deepfakes 和文本。来源：https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai
- Google Play AI-Generated Content policy 要求开发者确保生成式 AI app 不产生 offensive content、儿童剥削、欺骗、危险行为、骚扰、恶意代码等内容。来源：https://support.google.com/googleplay/android-developer/answer/14094294
- AppLovin 广告政策要求广告与实际体验一致，禁止 misleading、unverifiable claims、IP infringement，并说明系统会结合自动与人工审核。来源：https://legal.applovin.com/introduction-to-applovins-ad-content-policies/

推断：海外发行 AI 工作流必须把合规变成产品机制，而不是靠“提示词要求不要违规”。最低控制包括：素材来源记录、模型和授权记录、人物/声线/画风授权、平台政策 checklist、地区敏感词库、儿童与未成年人保护规则、隐私脱敏、外发审核留痕。

## 5. 开源 agent/workflow 的安全与生产风险

| 项目/风险类 | 事实证据 | 对海外发行 AI workflow 的含义 |
|---|---|---|
| n8n RCE | GitHub Advisory CVE-2025-68613，n8n expression injection，Critical 9.9。来源：https://github.com/advisories/GHSA-v98v-ff95-f3cp | 自托管 workflow 不等于安全。若接入投放账号、素材库、BI、Slack/飞书，RCE 可能导致 token、预算、素材和用户数据暴露 |
| Flowise 任意文件读 | Flowise GHSA-99pg-hqvx-r4gf，unauthenticated users 可读本地文件，默认配置可读 sqlite DB。来源：https://github.com/FlowiseAI/Flowise/security/advisories/GHSA-99pg-hqvx-r4gf | 低代码 agent builder 不能直接暴露公网，必须鉴权、网络隔离、版本锁定、漏洞扫描 |
| Flowise 任意文件写 | Flowise GHSA-jv9m-vf54-chjj，WriteFileTool 未校验路径，可写任意路径并可能 RCE。来源：https://github.com/FlowiseAI/Flowise/security/advisories/GHSA-jv9m-vf54-chjj | 工具节点权限要最小化，文件读写、Shell、HTTP request、DB write 都要白名单 |
| LangChain prompt injection / RCE | GitHub Advisory CVE-2025-46059 描述 GmailToolkit 间接 prompt injection，可通过 crafted email 触发任意代码执行；CVE-2024-21513 涉及 langchain-experimental eval 导致代码执行。来源：https://github.com/advisories/GHSA-3g6x-vq45-v2jv 和 https://github.com/advisories/GHSA-cgcg-p68q-3w7v | 读取邮件、网页、社群消息、玩家评论后再调用工具，是典型 indirect prompt injection 场景 |
| 通用 agent 风险 | OWASP LLM Top 10 将 prompt injection、sensitive information disclosure、insecure plugin design、excessive agency、overreliance 列为关键风险。来源：https://owasp.org/www-project-top-10-for-large-language-model-applications/ | agent 编排的核心风险不是回答错，而是“错了以后还能调用工具执行” |

关键摘录：

> “excessive permissions; excessive autonomy”

来源：https://genai.owasp.org/llmrisk/llm062025-excessive-agency/

## 6. 端到端 AI 发行流程必须设置的人审闸口

| 环节 | AI 可自动做 | 人审闸口 |
|---|---|---|
| 市场与竞品研究 | 抓取公开素材、评论、商店页、社媒讨论，生成候选洞察 | 区域优先级、产品定位、目标人群、预算方向由负责人确认 |
| 素材创意 | brief、脚本、分镜、标题、字幕、多语言版本、素材标签 | 外发前逐条过品牌、版权、平台政策、文化禁忌、未成年人、误导性声明 |
| 投放配置 | 生成 campaign draft、预算建议、A/B 测试矩阵、日报 | 新 campaign launch、预算上调、国家/渠道扩展、自动化设置开启必须人工批准 |
| 预算优化 | 异常监控、调价建议、低效素材停投建议 | 实际调预算、关停主力计划、切换优化目标、跨渠道挪预算需人工确认 |
| 社群与客服 | 聚类、摘要、建议回复、FAQ 推荐、舆情预警 | 自动回复只限低风险 FAQ；退款、补偿、封号、活动承诺、危机沟通人工确认 |
| 数据复盘 | 自动汇总平台、MMP、收入、留存、社群反馈 | 业务结论必须标注归因口径；重大复盘要有数据同学或负责人 review |
| 工作流/Agent 发布 | 在 sandbox 跑流程，生成变更说明和权限申请 | 上生产前安全 review，依赖审计，密钥检查，回滚方案，owner 签字 |

## 7. 权限边界设计

1. 默认 read-only。所有 agent 默认只能读素材、评论、报表、知识库；写操作单独申请。
2. 读写分离。读取广告报表的 token 与修改预算/发布广告的 token 分开。
3. 预算权限硬限额。单次预算调整、单日 spend、单 campaign spend、区域 spend 都设上限。
4. 外发权限白名单。只有通过审核队列的素材、公告、社群回复才能发布。
5. 敏感数据脱敏。玩家 ID、邮箱、支付、账号处罚、客服原始聊天默认脱敏后进 LLM。
6. secret 不进 prompt。API key、OAuth token、MMP key、广告账户 token 只能由 secret broker 注入工具层。
7. 高风险工具隔离。Shell、任意 HTTP、文件读写、数据库写入、广告账户修改、社媒发布都设为 privileged tools。
8. 不允许 agent 自审自批。AI 生成内容不能由同一个 agent 自动批准。
9. 全链路审计。保留输入、模型、提示词版本、输出、人工修改、发布人、发布时间、关联指标。
10. kill switch 和回滚。投放、社群、外发内容、自动工作流都要可一键暂停。

## 8. 指标监控

| 目标 | 指标 |
|---|---|
| 效率 | 周产出素材数、brief 到投放耗时、周报/复盘耗时、评论聚类耗时、人工处理节省时间 |
| 质量 | 人审通过率、返工率、事实错误率、术语一致性、素材平台拒审率、客服回复升级率 |
| 业务 | CTR、CVR、CPI、D1/D7 留存、付费率、ARPU、LTV、ROAS、回收周期、有效素材占比 |
| 增量 | geo holdout lift、incremental ROAS、新客占比、自然量 cannibalization、重激活用户占比 |
| 风险 | 异常花费、预算突增、负面情绪 spike、退款/投诉、素材误导反馈、policy rejection、版权投诉 |
| 安全 | prompt injection 命中、被拦截工具调用、异常 API 调用、secret scan 告警、漏洞版本、权限越权尝试 |

## 9. 给 VP 的反驳/校准话术

可以这样说：

> 我同意端到端是方向，但我会把它定义成“端到端 AI workflow”，不是“端到端无人决策”。海外发行里有大量执行动作可以自动化，比如素材 brief、素材变体、评论聚类、投放日报、舆情预警和多语言草稿。但预算、对外发布、玩家承诺、合规、版权和危机沟通必须有人审，因为这些动作需要可问责。

更强一点的说法：

> 广告平台已经给了我们一个现实样本：Google、Meta、AppLovin、Moloco 都在把投放自动化，但它们同时暴露出黑箱、素材跑偏、归因不稳定和控制权减少的问题。所以我不会把 AI 产品做成一个“自动替团队做决定”的系统，而会做成“自动跑流程、自动给证据、自动预警风险，由人批准关键动作”的系统。这样既能吃到 AI 提效，也不会把海外发行的品牌、预算和合规风险交给黑箱。

如果 VP 继续追问“为什么不能全自动”：

> 因为海外发行的损失函数不是单一 CPI 或 ROAS。错误素材可能伤品牌，错误回复可能构成玩家承诺，错误归因可能让预算被误导，版权和隐私问题可能直接触发平台下架或法律风险。AI 可以执行动作，但最终决策权要按风险分级交给不同 owner。我的产品设计目标是让 80% 低风险动作自动流转，让 20% 高风险动作更快、更有证据地被人批准。

## 10. 可直接带入方案的一句话

我的方案不是否定 AI 端到端，而是把端到端拆成三层：低风险执行自动化，中风险内容人审后发布，高风险预算/合规/玩家权益人工决策。AI 负责速度、覆盖和证据，人负责目标、边界和问责。

