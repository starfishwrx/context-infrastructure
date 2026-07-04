# Search Manifest

## 产出文件索引

| 文件 | 路径 | 说明 |
|---|---|---|
| Scratchpad | `E:\myagentos\context-infrastructure\tmp\g_bits_injoy_overseas_pan_qinan_20260617\scratchpad.md` | Phase 1 claim extraction、Phase 3 claim verification |
| Source Index | `E:\myagentos\context-infrastructure\tmp\g_bits_injoy_overseas_pan_qinan_20260617\source_index.md` | 来源索引、可信度、用途和摘录 |
| Subagent Outputs | `E:\myagentos\context-infrastructure\tmp\g_bits_injoy_overseas_pan_qinan_20260617\subagent_outputs.md` | 子调研摘要和关键输出 |
| Search Manifest | `E:\myagentos\context-infrastructure\tmp\g_bits_injoy_overseas_pan_qinan_20260617\search_manifest.md` | 本文件 |
| 最终报告 | `E:\myagentos\context-infrastructure\contexts\survey_sessions\g_bits_injoy_overseas_publishing_pan_qinan_standard_survey_20260618.md` | 严格标准流程版最终报告 |

## Subagent 原始产出

| Agent | Agent ID | 负责范围 | URLs 覆盖 | 状态 |
|---|---|---|---|---|
| Agent 1 | `019ed631-3a7e-7131-8bc1-409664e08a5e` | 官方业务与财报线 | 未取回 | not_found，无法回收输出 |
| Agent 2 | `019ed631-4e84-7ad0-93de-cb2137d50f89` | 官方招聘与岗位链路 | 官方招聘页、招聘前端 JS、招聘接口、目标岗位移动页 | completed |
| Agent 3 | `019ed631-4fbe-7f10-8f42-188d8b8c541a` | InJoy 与小红书/社媒口碑线 | 吉比特官网、加入我们、雷霆游戏、Boltray、年报、小红书关键词、牛客/博客园/鞭牛士 | completed |
| Agent 4 | `019ed631-64a1-7ba0-9047-cf62d39fb239` | 潘奇男公开背景与可验证性线 | 极致官网、游戏客栈/转载、极致互动 2020 半年度报告、2021 年报、吉比特 2021 年报新闻 | completed |
| Agent 5 | `019edad2-22bc-7290-8004-1d559353418b` | 官方业务与财报线补位 | 未返回 | timeout 后关闭 |

## 主线程补充验证

因为 Agent 1 未能回收且 Agent 5 超时，官方业务与财报线由主线程补充验证。已直接读取和抽取：

- 吉比特 2025 年年度报告摘要 PDF：https://stockmc.xueqiu.com/202603/603444_20260327_T2M5.pdf
- 吉比特关于页：https://www.g-bits.com/zh/about.html
- 吉比特招聘接口：`POST https://joinserver.g-bits.com:8666/humanResource/recruitmentExtranet/postManage/queryPostPage`
- 极致互动 2020 半年度报告 PDF：https://notice.10jqka.com.cn/api/pdf/36fb707cea935a16_1598515412/%E6%9E%81%E8%87%B4%E4%BA%92%E5%8A%A8%3A2020%E5%B9%B4%E5%8D%8A%E5%B9%B4%E5%BA%A6%E6%8A%A5%E5%91%8A.pdf

主线程验证到的关键摘录：

- 吉比特 2025 年报摘要：“本年公司境外营业收入合计 9.29 亿元，同比增加 85.80%，主要受到以下因素综合影响：①本年上线《杖剑传说（境外版）》《问剑长生（境外版）》等游戏，贡献增量营业收入。”
- 吉比特 2025 年报摘要：“《杖剑传说（境外版）》7.92 亿元。”
- 吉比特 2025 年报摘要：“公司产品运营模式主要有自主运营、联合运营及授权运营。”
- 吉比特 2025 年报摘要：“AI 技术的应用主要贯穿游戏产品研发、发行运营两大环节。”
- 官方招聘接口：目标岗 `AI产品经理(游戏发行方向)` 的 `postType=rootPostType=发行-境外市场`。

## 数据覆盖评估

| 维度 | 覆盖情况 | 风险 |
|---|---|---|
| 官方业务/财报 | 年报、官网、招聘接口覆盖充分 | 缺少已完成 subagent 的独立二次总结，但主线程证据为官方原文 |
| 官方岗位链路 | 覆盖充分，直接来自招聘接口 | 招聘接口可能随时间变化，报告需标日期 |
| InJoy 可见性 | 多路径未命中，覆盖充分 | 无法证明内部不存在，只能证明公开不可验证 |
| 小红书/社媒 | 公开搜索覆盖有限 | App 内登录内容无法访问，不能作强结论 |
| 潘奇男背景 | 采访、极致官网、公开 PDF 覆盖充分 | 当前吉比特 VP 头衔公开不可验证 |

## 读者模式

Internal memo。报告服务于候选人面试准备，不做可发布文章。重点交付：

- 面试判断
- 事实依据
- 不确定性边界
- 可直接使用的话术
- 反问问题

