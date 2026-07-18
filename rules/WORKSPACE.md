# WORKSPACE.md - 目录路由速查

目标：让 AI 每轮 session 都能快速知道"去哪里找/放什么"。**找任何文件前先查这里。**

## 路由规则

### 项目与代码
- 写代码 / 跑脚本 / 一次性项目：`adhoc_jobs/<project>/`
- 工具脚本（邮件、语义搜索、分享报告等）：`tools/`
- 定时任务：`periodic_jobs/`

### 知识与记录
- 通用调研报告：`contexts/survey_sessions/`
- 思考 / 复盘 / 方法论：`contexts/thought_review/`
- 按需加载的个人画像与项目台账：`contexts/people/`
- 每日日志：`contexts/daily_records/`

### 系统与规则
- 可复用技术方案 / Skill：`rules/skills/`
- 核心公理（Axioms）：`rules/axioms/`
- 本机受限个人规则：`rules/private/`（Git ignored；仅在身份、财务、关系、健康等相关任务中按需读取）
- 上游扩展文档 / public skill 生态：`docs/`
- 记忆系统：`contexts/memory/` + `periodic_jobs/ai_heartbeat/`

## 命名规则
- 目录和文件名：小写 + 下划线 (snake_case)
- 临时一次性项目：`tmp_<name>/`

## Python 环境
- 根目录 `.venv/` 为工作区级环境，用 `uv pip install` 管理依赖
- 需要隔离时在 `adhoc_jobs/<project>/.venv/` 建独立环境

## 快速查询

<!-- 随着你的项目增长，在这里添加活跃项目的快捷路由 -->
<!-- 格式：- `project-name` → `adhoc_jobs/project_name/` (说明) -->
- `ai-job-radar2` → `adhoc_jobs/ai_job_radar2/` (job radar project imported from Desktop)
- `ai-heartbeat` → `periodic_jobs/ai_heartbeat/` (observer/reflector prompts, docs, runtime)
- `ai-content-center` → `adhoc_jobs/ai_content_center/` (domestic AI content generation middle-platform prototype)
- `chronos-2` → `adhoc_jobs/chronos_2/` (time-series forecasting project imported from E:\demo)
- `plcagent` → `adhoc_jobs/plcagent/` (standalone Codex project)
- `hardware-diagnostics` → `adhoc_jobs/hardware_diagnostics/` (private host diagnostics and CPU/memory tuning evidence)
- `hardware-tuning` → `adhoc_jobs/hardware_tuning/` (private staged Ryzen 7900X and DDR5-6000 tuning controller; consumes diagnostics read-only)
- `e-drive-organization` → `adhoc_jobs/e_drive_organization/` (E 盘分类整理脚本, dry-run 默认, 分类规则见脚本内常量)
- `haixing-profile` → `contexts/people/haixing/profile.md` (按需加载的脱敏个人画像、阶段状态和项目证据台账)
- `haixing-sensitive` → `rules/private/USER_SENSITIVE.md` (本机受限身份、财务、家庭与关系画像；禁止进入 Git)
- `haixing-health` → `rules/private/USER_HEALTH.md` (本机受限健康画像与医疗协作边界；禁止进入 Git)
