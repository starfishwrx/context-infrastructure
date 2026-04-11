# Memory Observations

This is the L1/L2 layer of the memory system. Daily observations are appended by the heartbeat observer, and the weekly reflector promotes only stable, reusable knowledge into `rules/`.

## Format

Each dated block uses this structure:

```text
Date: YYYY-MM-DD

High: [methodology / hard constraint] description
Medium: [project status / decision] description
Low: [ephemeral task flow] description
```

Priority meanings:

- `High`: cross-project lessons, durable constraints, or major architectural decisions worth long-term retention and possible promotion.
- `Medium`: active-project status or decisions that will still matter over the next few weeks.
- `Low`: transient execution notes, debug traces, or short-lived context that should be garbage-collected regularly.

## How to Load Memory

Do not load this entire file by default. Search by keyword or recent dates as needed.

```powershell
Select-String -Path contexts/memory/OBSERVATIONS.md -Pattern "keyword"
Select-String -Path contexts/memory/OBSERVATIONS.md -Pattern '^Date:' -Context 0,8
```

```bash
rg -n "keyword" contexts/memory/OBSERVATIONS.md
rg -n "^Date:" contexts/memory/OBSERVATIONS.md
```

---

Date: 2026-03-29

Medium: [Active project] `adhoc_jobs/plcagent/` has reached a runnable Playwright automation skeleton centered on the forum reply flow, including login detection, iframe editor filling, optional `--submit`, local `.env` loading, and screenshot capture. Keep this as short-term project memory only; promote it into a reusable workflow or skill only after the real submission path and site adaptation strategy prove stable.

Date: 2026-04-06

Low: [Quiet Window] No new high-value effective changes were found across `adhoc_jobs/`, `periodic_jobs/`, `rules/skills/`, and root-level key files after the previous observer run; noise paths such as `contexts/daily_records/`, caches, `artifacts/`, backup directories, `.env`, and `adhoc_jobs/ai_job_radar2/.codex_tmp_ai_job_radar2/` were filtered out.

Date: 2026-04-07

🟢 Low: [Quiet Window] 按 `periodic_jobs/ai_heartbeat/prompts/codex_observer.md` 扫描 `adhoc_jobs/`、`periodic_jobs/`、`rules/skills/` 与根目录关键文件后，未发现最近约 24 小时内的新有效变更；已过滤 `contexts/daily_records/`、`__pycache__/`、`.pytest_cache/`、`artifacts/`、备份目录、`.env` 与 `.codex_tmp_*` 等噪音路径。

Date: 2026-04-09

🟡 Medium: [CMS Architecture] `adhoc_jobs/tmp_githubuiuxnotion/backend/alembic/versions/b9d4c8a1f6e2_add_cms_tables.py`、`adhoc_jobs/tmp_githubuiuxnotion/backend/app/models.py` 与 `adhoc_jobs/tmp_githubuiuxnotion/backend/app/routers/portfolio.py` 表明该临时项目已从单页作品集推进为数据库驱动的 CMS：新增 `site_settings`、`nav_icons`、`content_categories`、`content_items`、`timeline_items`、`tag_items`、`articles`、`media_assets` 与 `admin_users`，并提供带认证的后台 CRUD、媒体上传和从旧 `site_profiles`/`site_links` 向新结构自举的迁移路径。
🟡 Medium: [Fixed IA] `adhoc_jobs/tmp_githubuiuxnotion/backend/app/routers/portfolio.py` 将首页信息架构固定为 `sites/projects/plugins/articles` 四个 section key，只允许后台编辑分区元数据与内容项本身；`adhoc_jobs/tmp_githubuiuxnotion/web/src/pages/admin-cms-page.tsx` 同步落地了 settings/theme/icons/content/timeline/tags/articles/media 多标签后台，这种“固定骨架 + 可编辑内容”的建站模式比完全自由拼装更容易保持前台布局稳定。

Date: 2026-04-11

🟢 Low: [Quiet Window] 按 `periodic_jobs/ai_heartbeat/prompts/codex_observer.md` 扫描 `adhoc_jobs/`、`periodic_jobs/`、`rules/skills/` 与根目录关键文件后，未发现自 2026-04-09 21:41 CST 以来的新源码或文档级有效变更；已过滤 `tmp_githubuiuxnotion` 中仅体现运行痕迹的日志、构建产物、`node_modules/`、`.venv/` 与其他缓存类噪音路径。
