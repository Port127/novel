# Skill Contract Schema Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a maintainable Skill contract/schema audit, then apply the smallest documentation and Skill wording changes needed to align paths, schema usage, and cross-Skill contracts.

**Architecture:** The work is documentation-first. First collect evidence from current docs, Skills, scripts, schemas, templates, and the read-only reference project; then write `docs/SKILL_CONTRACT_AUDIT.md`; then make narrow edits to main docs and high-impact Skill files. No Skill Runner or Python CLI revival is included.

**Tech Stack:** Markdown, YAML schema files, Node.js Skill gate scripts, `rg`, `find`, `git`, optional read-only comparison against `other/oh-story-claudecode`.

---

## File Structure

**Create:**
- `docs/SKILL_CONTRACT_AUDIT.md` — the audit report and source of truth for this pass.

**Modify after audit confirms the need:**
- `.agents/AGENTS.md` — project-level path and schema rules.
- `README.md` — public overview and current flow.
- `docs/REQUIREMENTS.md` — product boundary and schema sufficiency principles.
- `docs/PIPELINE.md` — stage-level inputs, outputs, gates, and rollback notes.
- `docs/USER_MANUAL.md` — user-facing path references if they conflict with the audit.
- `.agents/skills/design-chapters/SKILL.md` — chapters index and detailed outline contract.
- `.agents/skills/daily-write/SKILL.md` — chapter source resolution and `notes.yaml` contract.
- `.agents/skills/golden-chapters/SKILL.md` — chapter index and script path wording.
- `.agents/skills/paywall-design/SKILL.md` — root `paywall_report.yaml` and script path wording.
- `.agents/skills/design-outline/SKILL.md` — `outline.yaml` / `arcs.yaml` / `pacing.yaml` / `notes.yaml` schema boundary.

**Read-only inputs:**
- `docs/superpowers/specs/2026-06-30-skill-contract-schema-audit-design.md`
- `data/schemas/*.schema.yaml`
- `templates/default/settings/*.yaml`
- `.agents/skills/*/scripts/*.js`
- `.agents/skills/*/references/*.md`
- `other/oh-story-claudecode`

**Do not modify:**
- `docs/feedback/archive/feedback.md` unless the user explicitly asks.
- Frozen Python implementation under `src/novel/` and legacy root `scripts/`.
- Historical plans under `docs/superpowers/plans/` except this plan file.

---

### Task 1: Baseline Evidence Collection

**Files:**
- Read: `docs/superpowers/specs/2026-06-30-skill-contract-schema-audit-design.md`
- Read: `.agents/AGENTS.md`
- Read: `README.md`
- Read: `docs/REQUIREMENTS.md`
- Read: `docs/PIPELINE.md`
- Read: `docs/USER_MANUAL.md`
- Read: `data/schemas/*.schema.yaml`
- Read: `templates/default/settings/*.yaml`
- Read: `.agents/skills/*/SKILL.md`
- Read: `.agents/skills/*/scripts/*.js`
- Read: `other/oh-story-claudecode`

- [ ] **Step 1: Verify worktree boundary**

Run:

```bash
git status --short
```

Expected:

```text
 M docs/feedback/archive/feedback.md
```

If additional files appear, identify whether they are user changes before continuing. Do not revert user changes.

- [ ] **Step 2: Re-read the approved spec**

Run:

```bash
sed -n '1,280p' docs/superpowers/specs/2026-06-30-skill-contract-schema-audit-design.md
```

Expected: output includes sections named `目标`, `Schema 三层审查`, `产物设计`, and `成功标准`.

- [ ] **Step 3: Capture current in-repo schema and Skill file list**

Run:

```bash
rg --files data/schemas templates/default/settings .agents/skills | sort
```

Expected: output includes these files:

```text
data/schemas/chapters.schema.yaml
data/schemas/characters.schema.yaml
data/schemas/completeness.schema.yaml
data/schemas/outline.schema.yaml
data/schemas/project.schema.yaml
data/schemas/scout_report.schema.yaml
data/schemas/worldbuilding.schema.yaml
templates/default/settings/chapters_index.yaml
.agents/skills/design-chapters/SKILL.md
.agents/skills/daily-write/SKILL.md
.agents/skills/paywall-design/SKILL.md
```

- [ ] **Step 4: Capture path and schema drift baseline**

Run:

```bash
rg -n "content/chapters|settings/paywall_report|content/chapter_|chapter_outlines|chapters_index|paywall_report|settings/notes|settings/arcs|settings/pacing|schema.yaml|data/schemas" README.md docs .agents data/schemas templates/default/settings
```

Expected: output may include current drift. Save the important findings mentally for `docs/SKILL_CONTRACT_AUDIT.md`; do not edit files in this task.

- [ ] **Step 5: Capture Skill script command baseline**

Run:

```bash
rg -n "node .*\\.js|scripts/.*\\.js|_shared/scripts" .agents/skills
```

Expected: output includes each Skill script invocation. Record mismatches where a Skill says `scripts/foo.js` but the actual file is under `.agents/skills/<skill>/scripts/foo.js` or `.agents/skills/_shared/scripts/foo.js`.

- [ ] **Step 6: Find reference project path**

Run:

```bash
find /Users/kiki/Documents/Project -maxdepth 6 -type d -name oh-story-claudecode
```

Expected: output contains one path ending in:

```text
other/oh-story-claudecode
```

If no path is found, continue by documenting the reference project as unavailable in the audit report.

- [ ] **Step 7: Read reference project contracts without editing it**

Run after replacing `<oh_story_path>` with the path found in Step 6:

```bash
rg --files <oh_story_path> | rg "AGENTS.md|README|schema|schemas|skills|SKILL.md|template|templates|docs"
```

Expected: output lists reference docs, schemas, templates, or Skill files. Read only files relevant to schema/contracts; do not copy files into this repository.

---

### Task 2: Create the Contract Audit Document

**Files:**
- Create: `docs/SKILL_CONTRACT_AUDIT.md`
- Read: outputs from Task 1

- [ ] **Step 1: Create the audit document with fixed sections**

Use `apply_patch` to create `docs/SKILL_CONTRACT_AUDIT.md` with this exact section structure:

```markdown
# Skill Contract Audit

## 结论摘要

## 当前统一口径

## Skill 输入输出总表

## Schema 使用矩阵

## 跨 Skill 冲突清单

## Schema 缺口与补充建议

## 参考 oh-story-claudecode 的可借鉴点

## 后续实施建议
```

Expected: file exists and all headings appear exactly once.

- [ ] **Step 2: Populate `当前统一口径`**

Add these decisions exactly:

```markdown
- 正文路径统一使用 `content/chapter_*.md`，例如 `content/chapter_001.md`、`content/chapter_XXX.md`。
- `content/chapters/` 是旧路径，不作为当前新流程路径。
- `settings/chapters_index.yaml` 是章节总索引和跨 Skill 调度表。
- `settings/chapter_outlines/chapter_*.md` 是单章详细蓝图，由 `design-chapters` 生成，可被下游读取，但不能替代章节总索引。
- `paywall_report.yaml` 位于单本小说项目根目录；`settings/paywall_report.yaml` 是旧计划残留路径。
- `_progress.md` 位于单本小说项目根目录，只用于长任务断点恢复。
- `src/novel/`、根目录 `scripts/` 和 `novel` CLI 是冻结遗留，不定义当前创作主流程。
```

Expected: these seven bullets appear under `当前统一口径`.

- [ ] **Step 3: Populate `Skill 输入输出总表`**

Create a Markdown table with these columns:

```markdown
| Skill | 主要输入 | 主要输出 | 使用 schema | 脚本门禁 | 状态文件 | 对齐结论 |
|-------|----------|----------|-------------|----------|----------|----------|
```

Add one row for each current Skill directory under `.agents/skills/` that has `SKILL.md`. Include at minimum:

```text
scout-topic
worldbuilding
design-character
design-outline
design-chapters
golden-chapters
paywall-design
daily-write
review
data-diagnosis
stock-check
export-novel
nm
feature-planning
refactor-planning
code-review-change
commit-msg
```

Expected: every row cites concrete file paths such as `settings/scout_report.yaml`, `settings/chapters_index.yaml`, `content/chapter_XXX.md`, or `paywall_report.yaml`. If a Skill has no structured schema, write `无直接 schema` in the schema column.

- [ ] **Step 4: Populate `Schema 使用矩阵`**

Create a Markdown table with these columns:

```markdown
| Schema 或产物 | 生产 Skill | 消费 Skill | 当前覆盖 | 风险 |
|---------------|------------|------------|----------|------|
```

Include rows for:

```text
data/schemas/scout_report.schema.yaml
data/schemas/worldbuilding.schema.yaml
data/schemas/characters.schema.yaml
data/schemas/outline.schema.yaml
data/schemas/chapters.schema.yaml
settings/arcs.yaml
settings/pacing.yaml
settings/notes.yaml
paywall_report.yaml
history/golden_chapters_report.md
exports/
```

Expected: rows for `settings/notes.yaml` and `paywall_report.yaml` explicitly state whether a dedicated schema exists.

- [ ] **Step 5: Populate `跨 Skill 冲突清单`**

Create a Markdown table with these columns:

```markdown
| 严重级别 | 冲突 | 证据 | 建议 |
|----------|------|------|------|
```

Use severity values:

```text
P0 阻断
P1 必须修正
P2 建议修正
P3 记录观察
```

Expected: include at least these conflicts if baseline evidence confirms them:

```text
content/chapters/ 与 content/chapter_*.md 路径漂移
chapters_index.yaml 与 chapter_outlines/ 关系未在主文档充分说明
settings/paywall_report.yaml 与根目录 paywall_report.yaml 历史残留
Skill 中 scripts/*.js 相对路径可能指向错误目录
notes.yaml tracking 节点缺少 dedicated schema
paywall_report.yaml 缺少 dedicated schema
outline.schema.yaml 与 outline/arcs/pacing 三文件边界可能不清
```

- [ ] **Step 6: Populate `Schema 缺口与补充建议`**

Create a Markdown table with these columns:

```markdown
| 建议 | 类型 | 理由 | 优先级 | 本轮动作 |
|------|------|------|--------|----------|
```

Expected: include explicit judgments for:

```text
notes.schema.yaml
paywall_report.schema.yaml
chapter_outline schema 或模板约束
golden_chapters_report schema
export 配置 schema
outline/arcs/pacing 是否拆分 schema
```

Use `本轮动作` values only from:

```text
仅记录
主文档说明
Skill 文档说明
后续单独设计
```

- [ ] **Step 7: Populate `参考 oh-story-claudecode 的可借鉴点`**

Summarize only contract-level lessons. Use this exact rule paragraph:

```markdown
本轮只吸收参考项目中有助于表达 Skill 合约、schema 边界、质量门禁和目录职责的经验；不复制与本项目 Skill 驱动、人机协同定位冲突的自动化结构。
```

Expected: this section contains no copied large blocks from the reference project.

- [ ] **Step 8: Verify audit document structure**

Run:

```bash
rg -n "^## " docs/SKILL_CONTRACT_AUDIT.md
```

Expected: output includes all seven second-level headings from Step 1.

- [ ] **Step 9: Commit audit document**

Run:

```bash
git add docs/SKILL_CONTRACT_AUDIT.md
git commit -m "docs: 添加 Skill 合约审计报告" -m "主要改动：
- 新增 Skill 输入输出、schema 使用和跨 Skill 冲突审计报告
- 明确正文路径、章节索引、单章细纲、付费报告和状态文件的当前口径
- 记录 schema 缺口、参考项目借鉴点和后续实施建议

验证结果：
- 运行 rg 检查审计文档二级标题完整
- 未修改现有 Skill、schema 或主流程文档"
```

Expected: commit succeeds and only `docs/SKILL_CONTRACT_AUDIT.md` is included.

---

### Task 3: Align Main Documentation Contracts

**Files:**
- Modify: `.agents/AGENTS.md`
- Modify: `README.md`
- Modify: `docs/REQUIREMENTS.md`
- Modify: `docs/PIPELINE.md`
- Modify: `docs/USER_MANUAL.md` only if baseline evidence shows drift
- Read: `docs/SKILL_CONTRACT_AUDIT.md`

- [ ] **Step 1: Run failing baseline drift check**

Run:

```bash
rg -n "content/chapters|settings/paywall_report|章节总索引|单章详细蓝图|Python 测试|冻结遗留" .agents/AGENTS.md README.md docs/REQUIREMENTS.md docs/PIPELINE.md docs/USER_MANUAL.md
```

Expected before edits: at least one of these conditions is true:

```text
.agents/AGENTS.md contains content/chapters/
main docs do not explain both 章节总索引 and 单章详细蓝图
main docs do not explicitly state Python tests are not the current Skill flow gate
```

- [ ] **Step 2: Update `.agents/AGENTS.md` project directory tree**

Replace the single-book directory entry:

```text
├── content/chapters/      # 章节正文
│   └── chapter_*.md
```

with:

```text
├── content/               # 章节正文
│   └── chapter_*.md
```

Add `chapter_outlines` under `settings/` if absent:

```text
│   ├── chapter_outlines/  # 单章详细蓝图，可选但推荐
│   └── notes.yaml         # 草稿/笔记
```

Expected: `.agents/AGENTS.md` no longer presents `content/chapters/` as the current path.

- [ ] **Step 3: Add current contract paragraph to `.agents/AGENTS.md`**

Insert under `## 目录结构` before `### 项目目录`:

```markdown
### 当前路径口径

- 章节正文统一写入 `content/chapter_*.md`，不使用旧路径 `content/chapters/`。
- `settings/chapters_index.yaml` 是章节总索引和跨 Skill 调度表。
- `settings/chapter_outlines/chapter_*.md` 是单章详细蓝图，由 `design-chapters` 生成，可被下游读取，但不能替代章节总索引。
- `paywall_report.yaml` 位于单本小说项目根目录，不放入 `settings/`。
- Python CLI、`src/novel/` 和根目录 `scripts/` 是冻结遗留；Python 测试红不阻断当前 Skill 主流程，除非本次任务明确维护遗留 Python。
```

Expected: the paragraph appears once.

- [ ] **Step 4: Update `README.md` single-book directory tree**

Under `settings/`, insert:

```text
│   ├── chapter_outlines/      # 单章详细蓝图，可选但推荐
```

near `chapters_index.yaml`.

After the single-book directory tree, add:

```markdown
章节规划采用双层结构：`settings/chapters_index.yaml` 是章节总索引和跨 Skill 调度表；`settings/chapter_outlines/chapter_*.md` 是单章详细蓝图，用于承载更长的分场、节拍、情绪和字数预算。下游 Skill 可以读取详细蓝图，但必须以章节总索引作为主入口。
```

Expected: README explains both index and detailed outline.

- [ ] **Step 5: Add frozen Python testing note to `README.md`**

After the paragraph that says not to use CLI as the recommended entry, add:

```markdown
冻结遗留代码可能仍有 Python 测试未通过。除非任务明确要求维护 `src/novel/`、根目录 `scripts/` 或 `novel` CLI，否则这些测试结果不作为当前 Skill 主流程是否可用的判断依据。
```

Expected: README distinguishes current Skill validation from frozen Python tests.

- [ ] **Step 6: Update `docs/REQUIREMENTS.md` data structure section**

After the single-book directory tree, add:

```markdown
章节规划采用双层结构：`settings/chapters_index.yaml` 是章节总索引和跨 Skill 调度表；`settings/chapter_outlines/chapter_*.md` 是单章详细蓝图。当前流程以章节总索引作为下游 Skill 的主入口，详细蓝图用于补充单章执行信息。

Schema 充分性按 Skill 合约判断：只要某个 Skill 生产结构化 YAML，或多个 Skill 共同读写同一份 YAML，就必须有明确 schema、模板或审计文档说明字段边界。缺少 dedicated schema 的产物必须在 `docs/SKILL_CONTRACT_AUDIT.md` 中记录。
```

Expected: requirements document contains the schema sufficiency rule.

- [ ] **Step 7: Update `docs/PIPELINE.md` stage 4 output**

In stage 4 `输出`, change it to include:

```markdown
- `settings/chapters_index.yaml`
- `settings/chapter_outlines/chapter_*.md`（单章详细蓝图，可选但推荐）
```

In stage 4 execution, add:

```markdown
`chapters_index.yaml` 必须保持可扫描、可调度；长篇分场、情绪推进和字数预算写入 `chapter_outlines/`，避免把章节总索引膨胀成不可维护的大文档。
```

Expected: pipeline document distinguishes index from detailed outline.

- [ ] **Step 8: Update `docs/PIPELINE.md` stage 6 output**

Ensure stage 6 output says:

```markdown
- `paywall_report.yaml`（单本小说项目根目录）
```

Expected: stage 6 does not imply `settings/paywall_report.yaml`.

- [ ] **Step 9: Update `docs/USER_MANUAL.md` only if needed**

Run:

```bash
rg -n "content/chapters|settings/paywall_report|chapters_index.yaml|chapter_outlines" docs/USER_MANUAL.md
```

If the output shows stale paths, edit the relevant section to match:

```markdown
章节正文路径为 `content/chapter_XXX.md`。章节总索引为 `settings/chapters_index.yaml`，详细细纲位于 `settings/chapter_outlines/chapter_*.md`。
```

Expected: user manual has no stale current-path wording.

- [ ] **Step 10: Run documentation drift verification**

Run:

```bash
rg -n "content/chapters|settings/paywall_report" .agents/AGENTS.md README.md docs/REQUIREMENTS.md docs/PIPELINE.md docs/USER_MANUAL.md
```

Expected after edits:

```text
No matches, or matches only in sentences explicitly marking the path as old or legacy.
```

- [ ] **Step 11: Commit main documentation alignment**

Run:

```bash
git add .agents/AGENTS.md README.md docs/REQUIREMENTS.md docs/PIPELINE.md docs/USER_MANUAL.md docs/SKILL_CONTRACT_AUDIT.md
git commit -m "docs: 统一 Skill 主流程路径口径" -m "主要改动：
- 统一正文路径为 content/chapter_*.md
- 明确 chapters_index.yaml 与 chapter_outlines/ 的双层章节规划关系
- 明确 paywall_report.yaml 位于单本小说项目根目录
- 补充冻结 Python 测试不阻断当前 Skill 主流程的说明

验证结果：
- 运行 rg 检查主文档中的旧正文路径和旧付费报告路径
- 确认旧路径仅作为历史或旧路径说明出现"
```

Expected: commit succeeds. `docs/feedback/archive/feedback.md` remains unstaged unless the user asked otherwise.

---

### Task 4: Align High-Impact Skill Contracts

**Files:**
- Modify: `.agents/skills/design-chapters/SKILL.md`
- Modify: `.agents/skills/daily-write/SKILL.md`
- Modify: `.agents/skills/golden-chapters/SKILL.md`
- Modify: `.agents/skills/paywall-design/SKILL.md`
- Modify: `.agents/skills/design-outline/SKILL.md`
- Read: `.agents/skills/design-chapters/scripts/check-chapters.js`
- Read: `.agents/skills/design-chapters/scripts/check-outlines.js`
- Read: `.agents/skills/paywall-design/scripts/check-paywall.js`
- Read: `.agents/skills/golden-chapters/scripts/check-golden-structure.js`
- Read: `.agents/skills/_shared/scripts/check-ai-patterns.js`
- Read: `.agents/skills/_shared/scripts/check-degeneration.js`

- [ ] **Step 1: Run failing Skill contract baseline**

Run:

```bash
rg -n "node scripts/|scripts/check-|content/chapters|settings/paywall_report|chapter_outlines|chapters_index|paywall_report|settings/notes.yaml|data/schemas/.*schema.yaml" .agents/skills/design-chapters/SKILL.md .agents/skills/daily-write/SKILL.md .agents/skills/golden-chapters/SKILL.md .agents/skills/paywall-design/SKILL.md .agents/skills/design-outline/SKILL.md
```

Expected before edits: output includes at least script path shorthand such as `node scripts/...` or contract wording that needs clarification.

- [ ] **Step 2: Update `design-chapters` outputs and script paths**

In `.agents/skills/design-chapters/SKILL.md`, ensure the output section contains both:

```markdown
> - `settings/chapters_index.yaml`（章节总索引和跨 Skill 调度表）
> - `settings/chapter_outlines/chapter_*.md`（单章详细蓝图，可选但推荐）
```

Replace script invocations:

```text
scripts/check-chapters.js settings/chapters_index.yaml
scripts/check-outlines.js settings/chapter_outlines/
```

with:

```text
node .agents/skills/design-chapters/scripts/check-chapters.js settings/chapters_index.yaml
node .agents/skills/design-chapters/scripts/check-outlines.js settings/chapter_outlines/
```

Expected: `design-chapters` describes index and detailed outlines as separate artifacts.

- [ ] **Step 3: Update `daily-write` chapter source resolution**

In `.agents/skills/daily-write/SKILL.md`, add under the Phase that loads chapter outline:

```markdown
`settings/chapters_index.yaml` 是目标章节定位和跨 Skill 调度的主入口。若存在 `settings/chapter_outlines/chapter_{N}.md`，必须读取它作为单章详细蓝图；若不存在，则只能基于章节总索引、`settings/arcs.yaml`、`settings/outline.yaml`、前文正文和 `settings/notes.yaml` 补建临时细纲，不得跳过细纲直接盲写。
```

Expected: daily-write no longer makes the detailed outline relationship ambiguous.

- [ ] **Step 4: Update `daily-write` shared script paths**

Ensure script commands use current paths:

```text
node .agents/skills/_shared/scripts/check-ai-patterns.js --check content/chapter_{N}.md
node .agents/skills/daily-write/scripts/normalize-punctuation.js content/chapter_{N}.md
node .agents/skills/_shared/scripts/check-degeneration.js --check content/chapter_{N}.md
```

Expected: all script paths exist in the repository.

- [ ] **Step 5: Update `golden-chapters` script paths and chapter index wording**

In `.agents/skills/golden-chapters/SKILL.md`, replace shorthand script paths with:

```text
node .agents/skills/golden-chapters/scripts/check-golden-structure.js settings/scout_report.yaml content/chapter_001.md
node .agents/skills/golden-chapters/scripts/check-golden-structure.js settings/scout_report.yaml content/chapter_001.md content/chapter_002.md
node .agents/skills/golden-chapters/scripts/check-golden-structure.js settings/scout_report.yaml content/chapter_001.md content/chapter_002.md content/chapter_003.md
node .agents/skills/golden-chapters/scripts/check-ai-patterns.js content/chapter_001.md content/chapter_002.md content/chapter_003.md
node .agents/skills/golden-chapters/scripts/check-degeneration.js content/chapter_001.md content/chapter_002.md content/chapter_003.md
```

Add one sentence near the first read of `chapters_index.yaml`:

```markdown
如存在 `settings/chapter_outlines/chapter_001.md` 至 `chapter_003.md`，应优先读取详细蓝图补足微节拍；但章节定位、文件名和状态仍以 `settings/chapters_index.yaml` 为准。
```

Expected: golden-chapters uses existing script locations and clear chapter source priority.

- [ ] **Step 6: Update `paywall-design` report path and script command**

In `.agents/skills/paywall-design/SKILL.md`, ensure every current output reference says:

```text
paywall_report.yaml
```

and does not say:

```text
settings/paywall_report.yaml
```

Replace ambiguous script wording:

```text
运行 `scripts/check-paywall.js` 验证切点合理性。
```

with:

```markdown
运行 `node .agents/skills/paywall-design/scripts/check-paywall.js settings/chapters_index.yaml paywall_report.yaml` 验证切点合理性。
```

Expected: script argument order matches `.agents/skills/paywall-design/scripts/check-paywall.js`.

- [ ] **Step 7: Update `design-outline` schema boundary wording**

In `.agents/skills/design-outline/SKILL.md`, add near the output list:

```markdown
`data/schemas/outline.schema.yaml` 当前作为大纲阶段的主结构约束，覆盖 `settings/outline.yaml` 的核心结构；`settings/arcs.yaml`、`settings/pacing.yaml` 和 `settings/notes.yaml` 的字段边界必须在本 Skill 示例、脚本门禁或 `docs/SKILL_CONTRACT_AUDIT.md` 中说明。若后续发现多个 Skill 共同读写这些文件且字段含义继续扩展，应单独设计 dedicated schema。
```

Expected: outline stage acknowledges multi-file schema boundary instead of implying one schema fully covers all files.

- [ ] **Step 8: Verify script paths exist**

Run:

```bash
rg -o "node [^`]+\\.js" .agents/skills/design-chapters/SKILL.md .agents/skills/daily-write/SKILL.md .agents/skills/golden-chapters/SKILL.md .agents/skills/paywall-design/SKILL.md .agents/skills/design-outline/SKILL.md
```

For each path after `node`, run:

```bash
test -f <script_path>
```

Expected: every referenced `.js` file exists.

- [ ] **Step 9: Verify no stale shorthand remains in high-impact Skills**

Run:

```bash
rg -n "node scripts/|`scripts/check-|settings/paywall_report|content/chapters" .agents/skills/design-chapters/SKILL.md .agents/skills/daily-write/SKILL.md .agents/skills/golden-chapters/SKILL.md .agents/skills/paywall-design/SKILL.md .agents/skills/design-outline/SKILL.md
```

Expected:

```text
No matches.
```

- [ ] **Step 10: Commit Skill contract alignment**

Run:

```bash
git add .agents/skills/design-chapters/SKILL.md .agents/skills/daily-write/SKILL.md .agents/skills/golden-chapters/SKILL.md .agents/skills/paywall-design/SKILL.md .agents/skills/design-outline/SKILL.md docs/SKILL_CONTRACT_AUDIT.md
git commit -m "skills: 对齐章节与卡点合约口径" -m "主要改动：
- 明确 chapters_index.yaml 与 chapter_outlines/ 的上下游读取关系
- 统一正文路径和 paywall_report.yaml 输出位置
- 将高影响 Skill 中的脚本调用改为当前仓库内实际路径
- 补充 outline/arcs/pacing/notes 的 schema 边界说明

验证结果：
- 运行 rg 检查高影响 Skill 中无旧脚本路径、旧正文路径和旧付费报告路径
- 使用 test -f 检查新增脚本路径均存在"
```

Expected: commit succeeds and includes only the listed Skill docs plus audit doc if updated.

---

### Task 5: Final Verification and Residual Risk Report

**Files:**
- Read: `docs/SKILL_CONTRACT_AUDIT.md`
- Read: modified docs and Skill files

- [ ] **Step 1: Verify global current-path consistency**

Run:

```bash
rg -n "content/chapters|settings/paywall_report" README.md docs .agents
```

Expected: matches are limited to historical docs, old-path warnings, or explicit legacy wording. Any unqualified current-path reference must be fixed before completion.

- [ ] **Step 2: Verify schema gap decisions are documented**

Run:

```bash
rg -n "notes\\.schema|paywall_report\\.schema|golden_chapters_report|outline/arcs/pacing|chapter_outline" docs/SKILL_CONTRACT_AUDIT.md docs/superpowers/specs/2026-06-30-skill-contract-schema-audit-design.md
```

Expected: output includes decisions or recommendations for all schema gap topics.

- [ ] **Step 3: Verify no accidental user-change staging**

Run:

```bash
git status --short
```

Expected: either a clean tree or only user-owned changes such as:

```text
 M docs/feedback/archive/feedback.md
```

If `docs/feedback/archive/feedback.md` remains modified and was not requested, leave it unstaged.

- [ ] **Step 4: Verify latest commits**

Run:

```bash
git log --oneline -5
```

Expected: recent commits include the audit document and any main-doc / Skill alignment commits created during execution.

- [ ] **Step 5: Report final state**

In the final response, include:

```text
- 新增或修改了哪些文件
- 哪些旧路径或 schema 缺口已经处理
- 哪些内容只记录为后续建议
- 执行过的验证命令和结果
- 是否仍保留用户未提交改动
```

Expected: the final response does not claim Python tests pass, because Python is frozen and not a verification gate for this task.
