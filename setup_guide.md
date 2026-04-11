# Setup Guide: Context Infrastructure

这是 AI 引导的配置指南。按步骤操作，每步完成后立刻能感受到差异。

---

## Step 1：填写身份文件（必填，5 分钟）

**价值**：完成这一步，AI 的行为立刻个性化。这是 ROI 最高的一步。

### 1a. 填写 USER.md

打开 `rules/USER.md`，用自己的信息替换模板内容。

至少填写这几项：
- **称呼**：你希望 AI 怎么叫你
- **时区**：避免时间混乱
- **背景**：你是谁、你做什么
- **技术兴趣**：越具体越好
- **会让你烦的**：帮 AI 避开你讨厌的沟通方式

**验证**：填好后，在 AI 对话里问「介绍一下你对我的了解」，看 AI 是否能准确描述你。

### 1b. 自定义 SOUL.md（可选但推荐）

打开 `rules/SOUL.md`，调整 AI 的核心行为基调。

默认内容已经是通用的良好基础（直接、有观点、不说废话）。如果你有特殊需求，在「氛围」和「核心真理」部分添加你的偏好。

---

## Step 2：探索和扩展 Skills（推荐，15 分钟）

**价值**：理解 skill 的格式，开始积累自己的可复用工作流。

### 2a. 浏览现有 Skills

打开 `rules/skills/INDEX.md`，快速扫描已有的 skill 分类：

- **BestPractice 类**：立刻可用，与你的工具和项目无关
- **Workflow 类**：调研、幻灯片制作、认知画像提取等，需要理解后适配
- **API Guide 类**：⚙️ 标记的需要配置，✅ 标记的可直接用

### 2b. 创建你的第一个 Skill

找一件你经常做的事（调用某个 API、处理某类数据、执行某个工作流），用以下格式创建 `rules/skills/<category>_<name>.md`：

```markdown
# Skill: 名称

## When to Use
什么情况下触发这个 skill

## Prerequisites  
需要什么工具/配置

## 步骤
1. 步骤一
2. 步骤二

## 示例
具体的命令或代码
```

将新 skill 添加到 `rules/skills/INDEX.md` 对应分类。

### 2c. 关于 Axioms（公理）

`rules/axioms/` 包含 43 条从真实经历中蒸馏的决策原则。这些代表原作者的视角和认知模式，对你有**参考价值**，但不能替代你自己的公理。

建议：
- 先浏览 `rules/axioms/INDEX.md` 了解分类和核心含义
- 遇到共鸣的公理，标注下来
- 未来从你自己的项目经历中积累你的公理（参考同类格式）

---

## Step 3：配置记忆系统（推荐，30 分钟）

**价值**：让 AI 自动积累你的工作经验，越用越懂你。

### 3a. 理解三层架构

```
L3（全局约束）: rules/ 下所有文件 → 每次 session 被动加载
L1/L2（动态记忆）: contexts/memory/OBSERVATIONS.md → agent 主动检索
```

L3 你已经配置好了（Step 1）。L1/L2 的主路径应当是 Codex 原生 automation；脚本入口保留给启动验证、故障排查和漏跑补跑。

### 3b. 配置 Agent 后端（为 Codex automation 做准备）

`periodic_jobs/ai_heartbeat/` 的 heartbeat 能力现在支持两种后端：

- **Codex CLI**：主路径。用于 Codex automation，也可供脚本入口复用。
- **OpenCode Server**：保留兼容，用于沿用原版 API 驱动方式。

#### 方案 A：Codex CLI（推荐）

1. 确认本机已安装 Codex CLI，并能运行 `codex exec --help`
2. 可选：在 `.env` 或系统环境变量中配置
   - `AI_HEARTBEAT_BACKEND=codex`
   - `CODEX_BIN=...`（Windows 下一般可指向 `C:\Users\<you>\AppData\Roaming\npm\codex.cmd`）
   - `CODEX_MODEL=gpt-5.4`（或你常用的 Codex 模型）
3. 用脚本做一次启动验证：

```bash
python periodic_jobs/ai_heartbeat/src/v0/observer.py --help
python periodic_jobs/ai_heartbeat/src/v0/reflector.py --help
```

#### 方案 B：OpenCode Server（兼容原版）

1. 确认本地 OpenCode Server 运行
2. 配置 `OPENCODE_BASE_URL`、`OPENCODE_PASSWORD` 等环境变量
3. 运行脚本时加 `--backend opencode`

### 3c. 配置 Codex Automations（主路径）

如果你已经在 Codex 桌面端里使用这套 workspace，这一步就是默认主路径，而不是可选增强。

参考文档：`periodic_jobs/ai_heartbeat/docs/CODEX_AUTOMATIONS.md`

推荐拆成两条：

- 每天 8:00 运行 Observer
- 每周日 9:00 运行 Reflector

这两条 automation 应该都指向当前 workspace 根目录。

### 3d. 手动脚本的定位

以下脚本入口仍然保留，但定位已经降级：

- 启动验证：确认环境变量、模型、路径和写入链路正常
- 故障排查：automation 异常时人工触发一次定位问题
- 漏跑补跑：某天 observer / reflector 没跑时人工补一次

不要把手动脚本当作长期主调度器。

### 3e. 兼容路径：如果你不用 Codex automation，再配置 Cron

只有在你明确不使用 Codex automation 时，才进入这条兼容路径：

```bash
# 每日 8:00 AM 运行 observer（扫描当日变化）
0 8 * * * cd /path/to/your/workspace && python3 periodic_jobs/ai_heartbeat/src/v0/observer.py --backend codex >> /tmp/observer.log 2>&1

# 每周一 9:00 AM 运行 reflector（蒸馏和晋升）
0 9 * * 1 cd /path/to/your/workspace && python3 periodic_jobs/ai_heartbeat/src/v0/reflector.py --backend codex >> /tmp/reflector.log 2>&1
```

调整路径和时间为你的实际情况。

### 3f. 验证

验证分成两层：

1. automation 验证：确认 Codex 里已经存在 daily observer 和 weekly reflector 两条 recurring automation
2. 脚本验证：手动运行一次 observer，确认 fallback 入口可用

```bash
python3 periodic_jobs/ai_heartbeat/src/v0/observer.py 2024-01-15 --backend codex
```

查看 `contexts/memory/OBSERVATIONS.md` 是否有新条目写入。

---

## Step 4：扩展 Tier 2 组件（按需，30-60 分钟）

以下组件独立工作，按需配置，不配不影响核心功能。

### 语义搜索（⚙️）

当你的 `contexts/` 目录积累了足够多内容后，语义搜索让你能按意思而非关键词检索历史记录。

**需要**：LLM Studio（本地）或 OpenAI API key  
**配置**：参见 `rules/skills/semantic_search.md`

### 分享报告到 Web（⚙️）

将调研报告转为 HTML 并发布到你自己的服务器。

**需要**：一台有 SSH 访问权限的服务器  
**配置**：参见 `rules/skills/share_report.md`，替换 `<your-domain>` 和 `<your-server>`

### 发送邮件通知（⚙️）

让 AI 完成任务后发邮件通知你。

**需要**：Gmail App Password  
**配置**：参见 `rules/skills/send_email.md`

---

## 何时你会感受到系统的价值

**填好 USER.md 后（立刻）**：AI 的回答更有针对性，不再是泛化的通用答复。

**使用 2-3 周后**：`contexts/` 目录里开始积累你的工作记录，AI 可以引用上下文。

**运行 1-2 个月记忆系统后**：observer 开始识别你的工作模式，reflector 把高价值经验晋升为 skill 或 axiom。

**积累 6+ 个月后**：系统开始真正了解你的判断逻辑和决策模式，你会发现 AI 给出的建议越来越接近你自己会做的决定。

---

## 常见问题

**Q：axioms 能直接用吗？**  
A：可以用来理解系统的结构，但核心内容代表原作者的视角。你的 axioms 需要从你自己的经历中提炼。参考 `rules/skills/workflow_cognitive_profile_extraction.md` 了解提炼方法。

**Q：skills 能直接用吗？**  
A：✅ 标记的可以直接用。⚙️ 标记的需要替换配置（endpoint、API key、域名等）。BestPractice 类基本都可以直接用。

**Q：observer.py 需要什么依赖？**  
A：如果你用 Codex，只需要本地可执行的 `codex exec`。但对这套 workspace 来说，`observer.py` 和 `reflector.py` 的主要定位是启动验证、故障排查和补跑；日常运行应交给 Codex automation。如果你用 OpenCode，则依赖 `opencode_client.py` 和对应的 Server API。

**Q：能用其他 AI agent（不用 OpenCode）吗？**  
A：可以。`observer.py` 的核心逻辑是构造 prompt 并调用 AI；现在仓库已内置 `Codex CLI` 与 `OpenCode` 两种后端。你也可以继续扩展成其他 Agent 后端。

---

## 下一步

系统搭好后，真正的积累才刚开始。关键是持续使用：把你的工作放在这个 workspace 里，让 AI 参与每天的工作。随着时间推移，系统会越来越懂你。
