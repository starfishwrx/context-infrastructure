# Search Manifest

## 产出文件索引

| 文件 | 路径 | 说明 |
|---|---|---|
| Scratchpad | `tmp/fujian_2025_admission_subjects/scratchpad.md` | 主线程研究笔记与统计口径 |
| Group Stats CSV | `tmp/fujian_2025_admission_subjects/physical_group_stats_line.csv` | 从官方物理组 PDF 抽取的院校专业组数据 |
| Major Entry Stats CSV | `tmp/fujian_2025_admission_subjects/physical_major_entry_stats.csv` | 从官方物理组 PDF 抽取的专业代码条目数据 |
| Final Report | `contexts/survey_sessions/fujian_2025_admission_subjects_survey_20260620.md` | 最终报告 |

## 来源索引

| 来源 | URL | 用途 |
|---|---|---|
| 福建省教育考试院《2025年福建省普通高校招生计划》 | https://www.eeafj.cn/gkptgkgsgg/20250626/14057.html | 官方招生计划下载入口 |
| 福建省教育厅 2027 年起本科专业选考科目要求通告 | https://jyt.fujian.gov.cn/ztzl/fjsgkzhgg/zctz/202502/t20250214_6715078.htm | 解释 3+1+2 和选科要求含义 |
| 福建省教育考试院 2025 年高考考生成绩分布物理科目组 | https://www.eeafj.cn/gkptgkgsgg/20250625/14056.html | 用于确认物理科目组整体位次背景，但未提供物化生/物化政细分 |

## 覆盖评估

- 已覆盖：2025 年福建普通类物理科目组官方招生计划全部 6 个 PDF。
- 已统计：院校专业组数量、院校专业组计划数、专业代码条目数。
- 未覆盖：各选科组合实际考生人数和分数分布。公开搜索未找到官方披露。

## Subagent

本任务未使用 subagent。当前会话可用 subagent 工具要求用户显式请求后再 spawn，本次由主线程完成。
