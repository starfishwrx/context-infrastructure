# Skill: Context Infrastructure Health Check

## 元数据

- **类型**: Workflow
- **适用场景**: 检查这个 workspace 是否还适合长期使用，或在初始化后做一次体检
- **创建日期**: 2026-03-28

---

## When to Use

在以下场景触发：

- 新 clone 或刚迁移到新机器后，确认基础设施能否正常运行
- 感觉 AI 开始变笨、找不到上下文、或历史记忆没有积累时
- 准备启用 Codex automation 前，先做一次配置体检

---

## 核心检查项

按这个顺序检查，避免泛泛扫描：

1. **rules**
   - `SOUL.md`、`USER.md`、`COMMUNICATION.md`、`WORKSPACE.md` 是否已经个性化
   - `WORKSPACE.md` 的快速路由是否覆盖活跃项目
2. **contexts**
   - `contexts/memory/OBSERVATIONS.md` 是否已有真实日期条目
   - `survey_sessions/`、`thought_review/`、`daily_records/` 是否开始积累真实内容
3. **skills**
   - `rules/skills/INDEX.md` 是否只有框架 skill，还是已经出现用户自己的高频 workflow
   - 若缺少用户专属 skill，优先补最常重复的任务
4. **runtime**
   - `.env` 是否存在，heartbeat 的 backend / model / path 是否可用
   - `periodic_jobs/ai_heartbeat/prompts/codex_observer.md` 与 `codex_reflector.md` 是否存在，作为 automation 的稳定策略入口
   - Codex 里是否已经存在 daily observer 和 weekly reflector 两条 recurring automation
   - 手动脚本只作为 fallback：`python periodic_jobs/ai_heartbeat/src/v0/observer.py --help`、`reflector.py --help` 是否正常
   - 如需验证 fallback，再手动运行一次 observer，确认 `OBSERVATIONS.md` 能写入

---

## 输出格式

输出必须包含三部分：

1. 当前是否适合长期使用：一句判断
2. 最关键的 3 个缺口：按优先级排序
3. 下一步动作：只给最短执行路径

---

## 示例命令

```powershell
python periodic_jobs/ai_heartbeat/src/v0/observer.py --help
python periodic_jobs/ai_heartbeat/src/v0/reflector.py --help
```
