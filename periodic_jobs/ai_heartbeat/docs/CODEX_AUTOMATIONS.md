# Codex Automations Guide

目标：用 Codex 自带的 recurring automation 作为 AI heartbeat 的默认主路径，而不是依赖 cron、Windows Task Scheduler 或手动脚本。

## 推荐拆分

保留两条 automation，不要合并：

- `AI Heartbeat Observer`
  - 每天运行一次
  - 负责把过去一天的高价值变化追加到 `contexts/memory/OBSERVATIONS.md`
- `AI Heartbeat Reflector`
  - 每周运行一次
  - 负责把稳定规律晋升到 `rules/` 并清理 `OBSERVATIONS.md`

这样符合原版的角色隔离：Observer 只记录，Reflector 才允许晋升规则。

## 运行原则

- 日常运行：Codex automation
- 启动验证：手动脚本
- 故障排查：手动脚本
- 漏跑补跑：手动脚本

如果 automation 已经配好，就不要再把 `observer.py` / `reflector.py` 当作长期主调度器。

## Automation Prompt 设计

Codex automation 最稳的做法不是把超长 prompt 全塞进 automation 配置，而是：

1. 在仓库里维护稳定 prompt 文件
2. automation 只负责让 Codex 打开这些文件并执行

当前建议使用：

- `periodic_jobs/ai_heartbeat/prompts/codex_observer.md`
- `periodic_jobs/ai_heartbeat/prompts/codex_reflector.md`

## 推荐 Prompt

### Observer automation

让 Codex：

1. 打开 `periodic_jobs/ai_heartbeat/prompts/codex_observer.md`
2. 将 `{{TARGET_DATE}}` 视为 automation 运行当天的本地日期
3. 按 prompt 要求完成扫描和写入
4. 最终回复简短 walkthrough

### Reflector automation

让 Codex：

1. 打开 `periodic_jobs/ai_heartbeat/prompts/codex_reflector.md`
2. 读取 `contexts/memory/OBSERVATIONS.md`
3. 晋升正式规则并做垃圾回收
4. 最终回复简短晋升汇报

## 手动触发

即使启用了 automations，手动入口也保留：

```bash
python periodic_jobs/ai_heartbeat/src/v0/observer.py --backend codex
python periodic_jobs/ai_heartbeat/src/v0/reflector.py --backend codex
```

这两个脚本和 automation 共用同一套 prompt 文件，所以行为应该一致。

手动入口的推荐用途只有三个：启动验证、故障排查、漏跑补跑。

## 什么时候改 prompt 文件

以下情况优先改 prompt 文件，而不是改 Python：

- 你想调整 Observer 的扫描范围
- 你想提高或收紧晋升门槛
- 你想改变 walkthrough 的输出格式
- 你想加入新的白名单/黑名单目录

以下情况再改 Python：

- 你要新增后端
- 你要改 CLI 参数
- 你要改路径解析逻辑
