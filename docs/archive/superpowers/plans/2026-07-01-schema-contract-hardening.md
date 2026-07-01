# Schema Contract Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Harden the main writing pipeline schema contracts so shared artifacts are consistent across schemas, templates, Skill instructions, and deterministic JS gates.

**Architecture:** This is a documentation/schema/script hardening pass, not a runtime rebuild. The implementation first creates small committed fixtures that expose current contract failures, then updates schemas/templates/scripts/Skill wording task by task. Each task keeps scope narrow and verifies with `rg`, Node gate scripts, and fixture-based negative/positive checks.

**Tech Stack:** Markdown, YAML-style schema comment files, Node.js built-in modules only, `rg`, `git`, shell `test`, fixture files under `tests/fixtures/schema-contract/`.

---

## File Structure

**Create:**
- `tests/fixtures/schema-contract/chapters_index.valid.yaml` — valid chapters index fixture.
- `tests/fixtures/schema-contract/chapters_index.invalid-template-drift.yaml` — legacy/template-drift fixture that should fail after hardening.
- `tests/fixtures/schema-contract/chapters_index.paywall-valid.yaml` — compact paywall validation fixture with 20 tension values.
- `tests/fixtures/schema-contract/chapter_outlines/chapter_001.md` — valid chapter outline fixture.
- `tests/fixtures/schema-contract/chapter_outlines/chapter_002.invalid.md` — invalid chapter outline fixture.
- `tests/fixtures/schema-contract/paywall_report.valid.yaml` — valid paywall report fixture.
- `tests/fixtures/schema-contract/paywall_report.invalid.yaml` — invalid paywall report fixture.
- `data/schemas/chapter_outline_frontmatter.schema.yaml` — frontmatter contract for chapter outline Markdown files.
- `data/schemas/notes.schema.yaml` — contract for `settings/notes.yaml`.
- `data/schemas/paywall_report.schema.yaml` — contract for `paywall_report.yaml`.

**Modify:**
- `data/schemas/chapters.schema.yaml` — align field names/ranges with current contract.
- `data/schemas/outline.schema.yaml` — clarify it covers `settings/outline.yaml` only, unless explicitly noted.
- `templates/default/settings/chapters_index.yaml` — align with `chapters.schema.yaml`.
- `templates/default/settings/notes.yaml` — align with `notes.schema.yaml`.
- `templates/default/settings/arcs.yaml` — clarify `arcs.yaml` boundary and chapter/beat locator fields.
- `templates/default/settings/pacing.yaml` — align tension range with `chapters_index.yaml`.
- `.agents/skills/design-chapters/references/chapter-template.md` — align frontmatter with `chapter_outline_frontmatter.schema.yaml`.
- `.agents/skills/design-chapters/scripts/check-chapters.js` — validate current chapters index contract.
- `.agents/skills/design-chapters/scripts/check-outlines.js` — validate chapter outline frontmatter plus existing budget checks.
- `.agents/skills/paywall-design/scripts/check-paywall.js` — validate paywall report required fields plus current tension checks.
- `.agents/skills/design-chapters/SKILL.md` — mention schema/template/gate mapping.
- `.agents/skills/design-outline/SKILL.md` — clarify outline/arcs/pacing/notes schema boundaries.
- `.agents/skills/daily-write/SKILL.md` — mention `notes.schema.yaml`, `paywall_report.schema.yaml`, and outline source priority.
- `.agents/skills/paywall-design/SKILL.md` — mention `paywall_report.schema.yaml`.
- `docs/SKILL_CONTRACT_AUDIT.md` — update status from “缺口记录” to “schema 合约已设计/实施”.

**Do not modify:**
- `src/novel/`
- root `scripts/`
- `docs/feedback/archive/feedback.md`, unless the user explicitly asks
- historical `docs/superpowers/plans/*` other than this plan

---

## Contract Decisions

Use these decisions consistently in implementation:

```yaml
# chapters_index.yaml current standard
chapters:
  - chapter: 1
    title: "第一章 标题"
    file: "content/chapter_001.md"
    outline_file: "settings/chapter_outlines/chapter_001.md"
    status: "planned"
    words_target: 3000
    words: 0
    density: "密"
    tension: 3
    summary:
      main_plot: "主线推进"
      character_change: "人物变化"
      foreshadowing: "伏笔"
      emotion: "情绪"
      hook: "章末钩子"
    beats:
      - "节拍 1"
      - "节拍 2"
      - "节拍 3"
    functions:
      - "开局引入"
    characters:
      - "主角"
    beat_ref:
      act: 1
      sequence: 1
      beat: 1
stats:
  total: 1
  planned: 1
  draft: 0
  written: 0
  revised: 0
  total_words: 0
```

Important choices:
- Use `chapter`, not `number`.
- Use `words_target`, not `word_count` or `target_words`.
- Use `file` for the future/current正文 path, e.g. `content/chapter_001.md`.
- Use `outline_file` for the detailed outline path, e.g. `settings/chapter_outlines/chapter_001.md`.
- Use `tension` range `1-5` across chapters and pacing.
- Treat missing `outline_file` as blocking for `design-chapters` output, because this project now expects detailed outlines from that Skill.

---

### Task 1: Add Contract Fixtures and Prove Current Drift

**Files:**
- Create: `tests/fixtures/schema-contract/chapters_index.valid.yaml`
- Create: `tests/fixtures/schema-contract/chapters_index.invalid-template-drift.yaml`
- Create: `tests/fixtures/schema-contract/chapter_outlines/chapter_001.md`
- Create: `tests/fixtures/schema-contract/chapter_outlines/chapter_002.invalid.md`
- Create: `tests/fixtures/schema-contract/paywall_report.valid.yaml`
- Create: `tests/fixtures/schema-contract/paywall_report.invalid.yaml`

- [ ] **Step 1: Verify current worktree boundary**

Run:

```bash
git status --short
```

Expected: either clean or only user-owned unrelated changes such as:

```text
 M docs/feedback/archive/feedback.md
```

Do not stage unrelated user changes.

- [ ] **Step 2: Add valid chapters index fixture**

Use `apply_patch` to add `tests/fixtures/schema-contract/chapters_index.valid.yaml`:

```yaml
chapters:
  - chapter: 1
    title: "第一章 旧梦醒来"
    file: "content/chapter_001.md"
    outline_file: "settings/chapter_outlines/chapter_001.md"
    status: "planned"
    words_target: 3000
    words: 0
    density: "密"
    tension: 4
    summary:
      main_plot: "主角在失败记忆中醒来，发现关键机会提前出现。"
      character_change: "从麻木自保转向主动抢占先机。"
      foreshadowing: "埋设旧账本和神秘来电。"
      emotion: "压迫感 4"
      hook: "电话那头说出了前世害死他的名字。"
    beats:
      - "醒来确认时间线"
      - "验证前世记忆"
      - "抢先拿到账本线索"
    functions:
      - "开局引入"
      - "钩子建立"
    characters:
      - "林周"
    beat_ref:
      act: 1
      sequence: 1
      beat: 1
stats:
  total: 1
  planned: 1
  draft: 0
  written: 0
  revised: 0
  total_words: 0
```

Expected: fixture exists and uses only current standard fields.

- [ ] **Step 3: Add invalid legacy/template-drift fixture**

Use `apply_patch` to add `tests/fixtures/schema-contract/chapters_index.invalid-template-drift.yaml`:

```yaml
target_chapters: 1
completed_chapters: 0
chapters:
  - number: 1
    title: "第一章 旧模板"
    summary: "旧模板摘要"
    word_count: 3000
    tension: 8
    status: planned
    beats:
      - "节拍 1"
      - "节拍 2"
      - "节拍 3"
    characters:
      - "林周"
    key_events:
      - "旧字段"
    emotional_tone: "紧张"
```

Expected after Task 2 hardening: this fixture fails because it uses `number`, `word_count`, missing `file`, missing `outline_file`, missing `words_target`, and tension exceeds `1-5`.

- [ ] **Step 4: Add valid chapter outline fixture**

Use `apply_patch` to add `tests/fixtures/schema-contract/chapter_outlines/chapter_001.md`:

```markdown
---
chapter: 1
title: "第一章 旧梦醒来"
content_file: "content/chapter_001.md"
outline_file: "settings/chapter_outlines/chapter_001.md"
status: "planned"
density: "密"
tension: 4
words_target: 3000
words: 0
functions:
  - "开局引入"
characters:
  - name: "林周"
    role: "protagonist"
arc_refs:
  - act: 1
    sequence: 1
    beat: 1
ready_for_draft: true
---

## 细纲（第 1 章）
### 第 1 章：旧梦醒来
- 核心事件：主角醒来并确认时间线。
- 字数目标：3000 字
- 目标情绪：压迫
- 章节定位：高压
- 章首钩子：重生确认 - 手机日期回到十年前
- 爽点：抢先拿到账本线索

#### 内容概括（五段式）
- 起因：主角从失败结局中醒来。
- 发展：他发现旧账本即将被销毁。
- 转折：他先一步联系关键人物。
- 高潮：电话中出现前世仇人的名字。
- 结尾：主角决定主动入局。

#### 情节安排（多线）
- 主线推进：主角确认新时间线并抢先行动。
- 辅线推进：无。
- 事件线 / 任务线：账本线索出现。
- 感情线 / 关系线：无显性。
- 逻辑线：醒来 → 验证 → 行动 → 新问题

#### 人物关系和出场顺序
- 出场顺序：林周 / 神秘来电
- 人物关系变化：孤立无援 → 找到突破口
- 视角/信息差：读者知道主角重生，敌人不知道。

#### 情节细化与字数预算（质量门禁核心）
- 林周醒来确认日期 + 开局引入 [密·600字]
- 搜索旧新闻验证记忆 + 信息确认 [密·500字]
- 回忆账本销毁节点 + 伏笔建立 [密·500字]
- 主角赶往旧仓库 + 行动推进 [密·700字]
- 神秘电话出现仇人名字 + 章尾钩子 [密·700字]
- 预算合计：3000字

#### 结尾设定和钩子
- 结尾设定：主角知道敌人也在找账本。
- 章尾钩子：强 - 电话那头说出了前世害死他的名字。
```

Expected: fixture has valid frontmatter and budget sum.

- [ ] **Step 5: Add invalid chapter outline fixture**

Use `apply_patch` to add `tests/fixtures/schema-contract/chapter_outlines/chapter_002.invalid.md`:

```markdown
---
chapter: 2
title: "第二章 错误细纲"
status: "planned"
tension: 9
words_target: 3000
---

## 细纲（第 2 章）
### 第 2 章：错误细纲

#### 情节细化与字数预算（质量门禁核心）
- 缺少必要路径字段 [密·100字]
- 预算合计：200字
```

Expected after Task 3 hardening: this fixture fails because it lacks `content_file`, `outline_file`, valid tension, and valid budget.

- [ ] **Step 6: Add paywall report fixtures**

Use `apply_patch` to add `tests/fixtures/schema-contract/paywall_report.valid.yaml`:

```yaml
paywall_chapter: 20
strategy:
  platform: "番茄"
  target_free_chapters: 20
  reason: "免费末章形成强悬念，付费首章立即兑现反击。"
candidate_cuts:
  - chapter: 18
    tension: 4
    reason: "悬念足够但反派压力未完全到位。"
  - chapter: 20
    tension: 5
    reason: "主线危机和反派压迫同时抵达。"
final_cut:
  chapter: 20
  free_last_chapter: 20
  paid_first_chapter: 21
  cliffhanger: "主角打开账本，却发现第一页写着自己的名字。"
  payoff_promise: "付费首章揭示账本来源，并让主角完成第一次反制。"
risks:
  - level: "advisory"
    message: "第 18-19 章需要避免连续低压。"
commercial_review:
  verdict: "pass"
  notes: "切点前有压迫，切点后有明确爽点兑现。"
```

Use `apply_patch` to add `tests/fixtures/schema-contract/paywall_report.invalid.yaml`:

```yaml
strategy:
  platform: "番茄"
candidate_cuts: []
final_cut:
  chapter: 0
```

Expected after Task 5 hardening: valid fixture passes `check-paywall.js` when paired with a chapters fixture containing chapter 20 tension; invalid fixture fails because it lacks `paywall_chapter` and required final cut details.

- [ ] **Step 7: Add compact paywall chapters fixture**

Use `apply_patch` to add `tests/fixtures/schema-contract/chapters_index.paywall-valid.yaml`:

```yaml
chapters:
  - chapter: 1
    tension: 3
  - chapter: 2
    tension: 3
  - chapter: 3
    tension: 3
  - chapter: 4
    tension: 4
  - chapter: 5
    tension: 3
  - chapter: 6
    tension: 4
  - chapter: 7
    tension: 3
  - chapter: 8
    tension: 4
  - chapter: 9
    tension: 3
  - chapter: 10
    tension: 4
  - chapter: 11
    tension: 3
  - chapter: 12
    tension: 4
  - chapter: 13
    tension: 3
  - chapter: 14
    tension: 4
  - chapter: 15
    tension: 3
  - chapter: 16
    tension: 4
  - chapter: 17
    tension: 3
  - chapter: 18
    tension: 4
  - chapter: 19
    tension: 4
  - chapter: 20
    tension: 5
```

Expected: this fixture is only for `check-paywall.js` tension extraction. It is not intended to pass `check-chapters.js`.

- [ ] **Step 8: Prove current baseline drift**

Run:

```bash
node .agents/skills/design-chapters/scripts/check-chapters.js tests/fixtures/schema-contract/chapters_index.invalid-template-drift.yaml
```

Expected before Task 2: command fails for missing current fields, proving the drift is at least partially detected.

Run:

```bash
node .agents/skills/design-chapters/scripts/check-outlines.js tests/fixtures/schema-contract/chapter_outlines
```

Expected before Task 3: command fails on `chapter_002.invalid.md`; it may not yet check all frontmatter fields. Record the missing checks in Task 3.

- [ ] **Step 9: Commit fixtures**

Run:

```bash
git add tests/fixtures/schema-contract
git commit -m "test: 添加 schema 合约验证夹具" -m "主要改动：
- 新增章节索引、章节细纲和付费报告的正反例夹具
- 用夹具固定当前 schema 合约补强的验证目标

验证结果：
- 运行 check-chapters.js 验证旧模板漂移夹具会失败
- 运行 check-outlines.js 验证错误细纲夹具会失败"
```

Expected: commit succeeds and includes only fixtures.

---

### Task 2: Align Chapters Index Schema, Template, and Gate

**Files:**
- Modify: `data/schemas/chapters.schema.yaml`
- Modify: `templates/default/settings/chapters_index.yaml`
- Modify: `.agents/skills/design-chapters/scripts/check-chapters.js`
- Modify: `.agents/skills/design-chapters/SKILL.md`
- Modify: `docs/SKILL_CONTRACT_AUDIT.md`

- [ ] **Step 1: Run baseline checks**

Run:

```bash
node .agents/skills/design-chapters/scripts/check-chapters.js tests/fixtures/schema-contract/chapters_index.valid.yaml
```

Expected before implementation: likely fails because `check-chapters.js` currently resolves `file` under `chapter_outlines/`. This proves the script still treats `file` as outline path.

Run:

```bash
rg -n "number:|word_count|target_chapters|completed_chapters|tension.*1-10" templates/default/settings/chapters_index.yaml data/schemas/chapters.schema.yaml .agents/skills/design-chapters/SKILL.md
```

Expected before implementation: matches in `templates/default/settings/chapters_index.yaml`.

- [ ] **Step 2: Update `data/schemas/chapters.schema.yaml`**

Use `apply_patch` so its chapter example contains this current standard:

```yaml
# chapter: 1                         # R | 章节号
# title: ""                          # R | 章节标题
# file: "content/chapter_001.md"     # R | 正文路径
# outline_file: "settings/chapter_outlines/chapter_001.md"  # R | 单章详细蓝图路径
# status: "planned"                  # R | 状态 planned/draft/written/revised
# words_target: 3000                 # R | 目标字数
# words: 0                           # R | 实际字数
# density: "密"                      # R | 密度（密/中/疏）
# tension: 3                         # R | 张力值（1-5）
# summary:                           # R | 五要素摘要
#   main_plot: ""
#   character_change: ""
#   foreshadowing: ""
#   emotion: ""
#   hook: ""
# beats: []                          # R | 节拍列表，3-15 个
# functions: []                      # O | 章节功能标签列表
# characters: []                     # O | 出场人物列表
# beat_ref:                          # O | 对应大纲节拍
#   act: 1
#   sequence: 1
#   beat: 1
```

Also ensure the stats block remains:

```yaml
stats:
  total: 0
  planned: 0
  draft: 0
  written: 0
  revised: 0
  total_words: 0
```

Expected: schema comments no longer mention legacy `number`, `word_count`, `target_chapters`, or `completed_chapters`.

- [ ] **Step 3: Update `templates/default/settings/chapters_index.yaml`**

Replace the template with:

```yaml
# 章节索引模板
# 章节总索引和跨 Skill 调度表。详细细纲写入 settings/chapter_outlines/chapter_*.md。
# [R] = 必填字段，[O] = 可选字段

chapters: []
# 每章包含：
#   chapter: 1
#   title: ""
#   file: "content/chapter_001.md"
#   outline_file: "settings/chapter_outlines/chapter_001.md"
#   status: "planned"
#   words_target: 3000
#   words: 0
#   density: "密"
#   tension: 3
#   summary:
#     main_plot: ""
#     character_change: ""
#     foreshadowing: ""
#     emotion: ""
#     hook: ""
#   beats: []
#   functions: []
#   characters: []
#   beat_ref:
#     act: 1
#     sequence: 1
#     beat: 1

stats:
  total: 0
  planned: 0
  draft: 0
  written: 0
  revised: 0
  total_words: 0
```

Expected: template uses the same standard fields as `chapters.schema.yaml`.

- [ ] **Step 4: Update `check-chapters.js` parser and checks**

Modify `.agents/skills/design-chapters/scripts/check-chapters.js` so:

```javascript
const VALID_STATUS = new Set(['planned', 'draft', 'written', 'revised']);
const VALID_DENSITY = new Set(['密', '中', '疏']);
```

In each chapter check, enforce:

```javascript
if (!ch.file) findings.push({ severity: 'blocking', msg: `第 ${num} 章缺少 file` });
else if (!/^content\/chapter_\d{3}\.md$/.test(ch.file)) {
  findings.push({ severity: 'blocking', msg: `第 ${num} 章 file 必须形如 content/chapter_001.md: ${ch.file}` });
}

if (!ch.outline_file) findings.push({ severity: 'blocking', msg: `第 ${num} 章缺少 outline_file` });
else {
  const expectedOutline = `settings/chapter_outlines/chapter_${String(num).padStart(3, '0')}.md`;
  if (ch.outline_file !== expectedOutline) {
    findings.push({ severity: 'blocking', msg: `第 ${num} 章 outline_file 应为 ${expectedOutline}: ${ch.outline_file}` });
  }
}

if (!VALID_STATUS.has(ch.status)) findings.push({ severity: 'blocking', msg: `第 ${num} 章 status 非法: ${ch.status}` });
if (!VALID_DENSITY.has(ch.density)) findings.push({ severity: 'blocking', msg: `第 ${num} 章 density 非法: ${ch.density}` });
```

Update `extractChapters()` to extract:

```javascript
outline_file: extractValue(block, /outline_file:\s*["']?([^"'\n]+)/),
```

Do not check that `content/chapter_001.md` exists, because planned chapters may not have正文 yet. Do not use `file` to check outline existence anymore.

Expected: valid fixture can pass once its outline file exists, and legacy fixture fails for current-contract reasons.

- [ ] **Step 5: Update `design-chapters` Skill wording**

In `.agents/skills/design-chapters/SKILL.md`, add one sentence near the output section:

```markdown
`settings/chapters_index.yaml` 必须遵循 `data/schemas/chapters.schema.yaml`；每章使用 `file` 指向 `content/chapter_XXX.md`，使用 `outline_file` 指向 `settings/chapter_outlines/chapter_XXX.md`。
```

Expected: Skill tells agents how to map content file vs outline file.

- [ ] **Step 6: Update audit document status**

In `docs/SKILL_CONTRACT_AUDIT.md`, update the row about `chapters.schema.yaml` and template drift to say this task aligns them and uses `chapter/file/outline_file/words_target/tension 1-5` as current standard.

Expected: audit no longer says the drift is unresolved after this task.

- [ ] **Step 7: Verify chapters contract**

Run:

```bash
node .agents/skills/design-chapters/scripts/check-chapters.js tests/fixtures/schema-contract/chapters_index.valid.yaml
```

Expected after implementation: pass, unless the checker also requires the outline file path to exist relative to fixture. If it requires existence, either create the expected `settings/chapter_outlines/chapter_001.md` inside fixture scope or limit existence checking to `check-outlines.js`.

Run:

```bash
node .agents/skills/design-chapters/scripts/check-chapters.js tests/fixtures/schema-contract/chapters_index.invalid-template-drift.yaml
```

Expected after implementation: fail with blocking findings for legacy fields/missing current fields.

Run:

```bash
rg -n "number:|word_count|target_chapters|completed_chapters|tension.*1-10" templates/default/settings/chapters_index.yaml data/schemas/chapters.schema.yaml
```

Expected:

```text
No matches.
```

- [ ] **Step 8: Commit chapters index alignment**

Run:

```bash
git add data/schemas/chapters.schema.yaml templates/default/settings/chapters_index.yaml .agents/skills/design-chapters/scripts/check-chapters.js .agents/skills/design-chapters/SKILL.md docs/SKILL_CONTRACT_AUDIT.md tests/fixtures/schema-contract
git commit -m "schemas: 对齐章节索引合约" -m "主要改动：
- 统一 chapters_index 的字段命名、正文路径和详细细纲路径
- 同步 chapters.schema.yaml 与默认章节索引模板
- 更新 check-chapters.js 以校验当前章节索引合约
- 在 design-chapters 与审计文档中记录当前标准

验证结果：
- 运行 check-chapters.js 验证当前标准夹具通过
- 运行 check-chapters.js 验证旧模板漂移夹具失败
- 运行 rg 确认章节索引模板和 schema 不再使用旧字段"
```

Expected: commit succeeds.

---

### Task 3: Add Chapter Outline Frontmatter Contract

**Files:**
- Create: `data/schemas/chapter_outline_frontmatter.schema.yaml`
- Modify: `.agents/skills/design-chapters/references/chapter-template.md`
- Modify: `.agents/skills/design-chapters/scripts/check-outlines.js`
- Modify: `.agents/skills/design-chapters/SKILL.md`
- Modify: `docs/SKILL_CONTRACT_AUDIT.md`

- [ ] **Step 1: Run baseline outline checks**

Run:

```bash
node .agents/skills/design-chapters/scripts/check-outlines.js tests/fixtures/schema-contract/chapter_outlines
```

Expected before implementation: fails on invalid fixture, but does not report every missing frontmatter field required by the new contract.

- [ ] **Step 2: Add frontmatter schema file**

Use `apply_patch` to add `data/schemas/chapter_outline_frontmatter.schema.yaml`:

```yaml
# chapter_outline_frontmatter.schema.yaml
# 单章详细蓝图 Markdown frontmatter schema
# 路径: novels/{project_id}/settings/chapter_outlines/chapter_*.md

# R = 必填, O = 可选

# chapter: 1                         # R | 章节号，必须与文件名 chapter_001.md 一致
# title: ""                          # R | 章节标题
# content_file: "content/chapter_001.md"  # R | 对应正文路径
# outline_file: "settings/chapter_outlines/chapter_001.md"  # R | 当前细纲路径
# status: "planned"                  # R | planned/draft/written/revised
# density: "密"                      # R | 密/中/疏
# tension: 3                         # R | 1-5
# words_target: 3000                 # R | 目标字数
# words: 0                           # R | 实际字数，初始为 0
# functions: []                      # O | 章节功能标签
# characters:                        # O | 出场角色
#   - name: ""
#     role: ""
# arc_refs:                          # O | 对应大纲/弧线定位
#   - act: 1
#     sequence: 1
#     beat: 1
# ready_for_draft: true              # R | 是否可进入正文写作
```

Expected: new schema file documents all required frontmatter fields.

- [ ] **Step 3: Update chapter template frontmatter**

In `.agents/skills/design-chapters/references/chapter-template.md`, replace frontmatter example with the schema fields:

```yaml
---
chapter: 1
title: "第一章 开始"
content_file: "content/chapter_001.md"
outline_file: "settings/chapter_outlines/chapter_001.md"
status: "planned"
density: "密"
tension: 3
words_target: 3000
words: 0
functions:
  - "开局引入"
characters:
  - name: ""
    role: "protagonist"
arc_refs:
  - act: 1
    sequence: 1
    beat: 1
ready_for_draft: true
---
```

Expected: template no longer uses `file` in outline frontmatter; it uses `content_file` and `outline_file`.

- [ ] **Step 4: Harden `check-outlines.js` frontmatter checks**

Update `.agents/skills/design-chapters/scripts/check-outlines.js` to extract and validate frontmatter fields with simple regex helpers:

```javascript
function getField(fm, name) {
  const re = new RegExp(`^${name}:\\s*["']?([^"'\\n]+)["']?\\s*$`, 'm');
  const match = fm.match(re);
  return match ? match[1].trim() : null;
}
```

For each file, add blocking checks:

```javascript
const chapter = Number(getField(fm, 'chapter'));
const expectedFile = `chapter_${String(chapter).padStart(3, '0')}.md`;
if (!chapter) findings.push({ severity: 'blocking', msg: `${file}: Frontmatter 缺少 chapter 字段` });
else if (file !== expectedFile) findings.push({ severity: 'blocking', msg: `${file}: 文件名应为 ${expectedFile}` });

const contentFile = getField(fm, 'content_file');
if (!contentFile) findings.push({ severity: 'blocking', msg: `${file}: Frontmatter 缺少 content_file 字段` });
else if (contentFile !== `content/chapter_${String(chapter).padStart(3, '0')}.md`) findings.push({ severity: 'blocking', msg: `${file}: content_file 与章节号不一致` });

const outlineFile = getField(fm, 'outline_file');
if (!outlineFile) findings.push({ severity: 'blocking', msg: `${file}: Frontmatter 缺少 outline_file 字段` });
else if (outlineFile !== `settings/chapter_outlines/${expectedFile}`) findings.push({ severity: 'blocking', msg: `${file}: outline_file 与文件名不一致` });

const status = getField(fm, 'status');
if (!['planned', 'draft', 'written', 'revised'].includes(status)) findings.push({ severity: 'blocking', msg: `${file}: status 非法或缺失` });

const tension = Number(getField(fm, 'tension'));
if (!tension || tension < 1 || tension > 5) findings.push({ severity: 'blocking', msg: `${file}: tension 必须在 1-5` });

const ready = getField(fm, 'ready_for_draft');
if (!['true', 'false'].includes(String(ready))) findings.push({ severity: 'blocking', msg: `${file}: ready_for_draft 必须为 true/false` });
```

Keep existing budget checks, but continue using `words_target`.

Expected: invalid fixture fails with missing path/frontmatter messages; valid fixture passes if only valid fixture is checked.

- [ ] **Step 5: Update Skill and audit wording**

In `.agents/skills/design-chapters/SKILL.md`, add:

```markdown
`settings/chapter_outlines/chapter_*.md` 的 YAML Frontmatter 必须遵循 `data/schemas/chapter_outline_frontmatter.schema.yaml`，正文 Markdown 结构遵循 `references/chapter-template.md`。
```

In `docs/SKILL_CONTRACT_AUDIT.md`, update `chapter_outlines` rows to reference the new frontmatter schema.

Expected: docs describe both frontmatter schema and Markdown template responsibilities.

- [ ] **Step 6: Verify outline frontmatter contract**

Run:

```bash
node .agents/skills/design-chapters/scripts/check-outlines.js tests/fixtures/schema-contract/chapter_outlines
```

Expected: fails because `chapter_002.invalid.md` is intentionally invalid.

Create a temporary directory containing only the valid outline:

```bash
mkdir -p /private/tmp/schema-contract-valid-outlines
cp tests/fixtures/schema-contract/chapter_outlines/chapter_001.md /private/tmp/schema-contract-valid-outlines/
node .agents/skills/design-chapters/scripts/check-outlines.js /private/tmp/schema-contract-valid-outlines
```

Expected: pass.

Run:

```bash
rg -n "chapter_outline_frontmatter|content_file|outline_file|ready_for_draft" data/schemas/chapter_outline_frontmatter.schema.yaml .agents/skills/design-chapters/references/chapter-template.md .agents/skills/design-chapters/SKILL.md docs/SKILL_CONTRACT_AUDIT.md
```

Expected: matches in all four files.

- [ ] **Step 7: Commit chapter outline contract**

Run:

```bash
git add data/schemas/chapter_outline_frontmatter.schema.yaml .agents/skills/design-chapters/references/chapter-template.md .agents/skills/design-chapters/scripts/check-outlines.js .agents/skills/design-chapters/SKILL.md docs/SKILL_CONTRACT_AUDIT.md tests/fixtures/schema-contract
git commit -m "schemas: 添加单章细纲 frontmatter 合约" -m "主要改动：
- 新增 chapter_outline_frontmatter schema
- 统一单章细纲模板 frontmatter 字段
- 增强 check-outlines.js 对 frontmatter 的确定性检查
- 更新 design-chapters 与审计文档中的细纲合约说明

验证结果：
- 运行 check-outlines.js 验证错误细纲夹具失败
- 运行 check-outlines.js 验证仅含有效细纲的临时目录通过
- 运行 rg 确认 schema、模板、Skill 和审计文档均引用 frontmatter 合约"
```

Expected: commit succeeds.

---

### Task 4: Add Notes Schema and Template Contract

**Files:**
- Create: `data/schemas/notes.schema.yaml`
- Modify: `templates/default/settings/notes.yaml`
- Modify: `.agents/skills/design-outline/SKILL.md`
- Modify: `.agents/skills/daily-write/SKILL.md`
- Modify: `.agents/skills/daily-write/references/state-tracking.md`
- Modify: `docs/SKILL_CONTRACT_AUDIT.md`

- [ ] **Step 1: Capture baseline notes drift**

Run:

```bash
sed -n '1,220p' templates/default/settings/notes.yaml
rg -n "tracking|近5章|十章|卷级|角色状态|伏笔|notes.schema|settings/notes.yaml" .agents/skills/design-outline/SKILL.md .agents/skills/daily-write/SKILL.md .agents/skills/daily-write/references/state-tracking.md docs/SKILL_CONTRACT_AUDIT.md
```

Expected before implementation: template is minimal and docs mention tracking without dedicated schema.

- [ ] **Step 2: Add `notes.schema.yaml`**

Use `apply_patch` to add `data/schemas/notes.schema.yaml`:

```yaml
# notes.schema.yaml
# 项目备忘与长篇上下文追踪 schema
# 路径: novels/{project_id}/settings/notes.yaml

# R = 必填, O = 可选

version: 1                             # R | notes schema 版本

tracking:                              # R | 长篇追踪节点
  recent_chapters: []                  # R | 近 5 章详记
  # - chapter: 1                       # R | 章节号
  #   file: "content/chapter_001.md"   # R | 正文路径
  #   summary: ""                      # R | 本章实际发生内容
  #   state_changes: []                # O | 状态变化列表
  #   open_hooks: []                   # O | 新增或延续钩子
  ten_chapter_summaries: []            # R | 十章概要
  # - range: "1-10"                    # R | 章节范围
  #   summary: ""                      # R | 概要
  volume_overview: []                  # R | 卷级总览
  # - volume: 1                        # R | 卷号
  #   goal: ""                         # R | 本卷目标
  #   current_state: ""                # R | 当前状态
  character_states: []                 # R | 角色状态追踪
  # - name: ""                         # R | 角色名
  #   current_state: ""                # R | 当前状态
  #   last_changed_chapter: 0          # R | 最近变化章节
  #   unresolved_conflicts: []         # O | 未解决矛盾
  foreshadowing: []                    # R | 伏笔追踪
  # - id: ""                           # R | 伏笔 ID
  #   planted_chapter: 0               # R | 埋设章节
  #   status: "open"                   # R | open/resolved/dropped
  #   planned_resolution_chapter: 0    # O | 计划回收章节
  #   note: ""                         # O | 说明

preferences:                           # R | 写作偏好和禁用项
  style_notes: []                      # R | 用户偏好
  banned_settings: []                  # R | 禁用设定
  pending_confirmations: []            # R | 待确认事项
```

Expected: new schema describes tracking, character states, foreshadowing, and preferences.

- [ ] **Step 3: Expand notes template**

Replace `templates/default/settings/notes.yaml` with:

```yaml
# 项目草稿区与长篇上下文追踪
# 对齐 data/schemas/notes.schema.yaml

version: 1

tracking:
  recent_chapters: []
  ten_chapter_summaries: []
  volume_overview: []
  character_states: []
  foreshadowing: []

preferences:
  style_notes: []
  banned_settings: []
  pending_confirmations: []
```

Expected: template is no longer just comments.

- [ ] **Step 4: Update design-outline notes creation wording**

In `.agents/skills/design-outline/SKILL.md`, near the output list or notes initialization step, add:

```markdown
`settings/notes.yaml` 必须按 `data/schemas/notes.schema.yaml` 初始化，至少包含 `tracking.recent_chapters`、`tracking.ten_chapter_summaries`、`tracking.volume_overview`、`tracking.character_states`、`tracking.foreshadowing` 和 `preferences` 节点。
```

Expected: design-outline initializes notes using the schema.

- [ ] **Step 5: Update daily-write notes update wording**

In `.agents/skills/daily-write/SKILL.md`, where it updates notes, add:

```markdown
更新 `settings/notes.yaml` 时必须保持 `data/schemas/notes.schema.yaml` 的结构：新章详记写入 `tracking.recent_chapters`，十章压缩摘要写入 `tracking.ten_chapter_summaries`，角色变化写入 `tracking.character_states`，伏笔状态写入 `tracking.foreshadowing`。
```

Expected: daily-write has concrete write targets for notes updates.

- [ ] **Step 6: Update state tracking reference**

In `.agents/skills/daily-write/references/state-tracking.md`, add a short section:

```markdown
## Schema 对齐

`settings/notes.yaml` 必须遵循 `data/schemas/notes.schema.yaml`。本文件中的状态追踪方法写入以下节点：

- `tracking.recent_chapters`
- `tracking.ten_chapter_summaries`
- `tracking.volume_overview`
- `tracking.character_states`
- `tracking.foreshadowing`
- `preferences`
```

Expected: reference method maps to schema nodes.

- [ ] **Step 7: Update audit document**

In `docs/SKILL_CONTRACT_AUDIT.md`, update `notes.yaml` rows from “缺 dedicated schema” to “已新增 dedicated schema，后续可补脚本门禁”.

Expected: audit reflects new schema status.

- [ ] **Step 8: Verify notes contract**

Run:

```bash
rg -n "notes.schema.yaml|tracking.recent_chapters|tracking.ten_chapter_summaries|tracking.volume_overview|tracking.character_states|tracking.foreshadowing|preferences" data/schemas/notes.schema.yaml templates/default/settings/notes.yaml .agents/skills/design-outline/SKILL.md .agents/skills/daily-write/SKILL.md .agents/skills/daily-write/references/state-tracking.md docs/SKILL_CONTRACT_AUDIT.md
```

Expected: matches across schema, template, Skills/reference, and audit.

- [ ] **Step 9: Commit notes schema**

Run:

```bash
git add data/schemas/notes.schema.yaml templates/default/settings/notes.yaml .agents/skills/design-outline/SKILL.md .agents/skills/daily-write/SKILL.md .agents/skills/daily-write/references/state-tracking.md docs/SKILL_CONTRACT_AUDIT.md
git commit -m "schemas: 添加 notes 上下文追踪合约" -m "主要改动：
- 新增 notes.schema.yaml
- 扩展默认 notes 模板为可读写的 tracking/preferences 结构
- 更新 design-outline 与 daily-write 对 notes.yaml 的初始化和更新规则
- 同步状态追踪参考文档与审计报告

验证结果：
- 运行 rg 确认 schema、模板、Skill、参考文档和审计报告均引用 notes 合约节点"
```

Expected: commit succeeds.

---

### Task 5: Add Paywall Report Schema and Gate Checks

**Files:**
- Create: `data/schemas/paywall_report.schema.yaml`
- Modify: `.agents/skills/paywall-design/SKILL.md`
- Modify: `.agents/skills/paywall-design/scripts/check-paywall.js`
- Modify: `.agents/skills/daily-write/SKILL.md`
- Modify: `docs/SKILL_CONTRACT_AUDIT.md`
- Modify: `tests/fixtures/schema-contract/paywall_report.valid.yaml`
- Modify: `tests/fixtures/schema-contract/paywall_report.invalid.yaml`

- [ ] **Step 1: Capture baseline paywall behavior**

Run:

```bash
node .agents/skills/paywall-design/scripts/check-paywall.js tests/fixtures/schema-contract/chapters_index.valid.yaml tests/fixtures/schema-contract/paywall_report.invalid.yaml
```

Expected before implementation: fails because `paywall_chapter` is missing.

Run:

```bash
rg -n "paywall_report.schema|paywall_chapter|candidate_cuts|final_cut|payoff_promise" .agents/skills/paywall-design/SKILL.md .agents/skills/daily-write/SKILL.md docs/SKILL_CONTRACT_AUDIT.md
```

Expected before implementation: no dedicated schema reference.

- [ ] **Step 2: Add paywall report schema**

Use `apply_patch` to add `data/schemas/paywall_report.schema.yaml`:

```yaml
# paywall_report.schema.yaml
# 付费卡点报告 schema
# 路径: novels/{project_id}/paywall_report.yaml

# R = 必填, O = 可选

paywall_chapter: 20                    # R | 最终付费切点章节

strategy:                              # R | 平台和切点策略
  platform: ""                         # R | 平台名称
  target_free_chapters: 0              # R | 目标免费章数
  reason: ""                           # R | 策略理由

candidate_cuts: []                     # R | 候选切点
# - chapter: 20                        # R | 候选章节
#   tension: 5                         # R | 候选章张力，1-5
#   reason: ""                         # R | 候选理由

final_cut:                             # R | 最终切点设计
  chapter: 20                          # R | 最终切点章节，必须等于 paywall_chapter
  free_last_chapter: 20                # R | 免费末章
  paid_first_chapter: 21               # R | 付费首章
  cliffhanger: ""                      # R | 免费末章悬念
  payoff_promise: ""                   # R | 付费首章反馈承诺

risks: []                              # O | 风险项
# - level: "advisory"                  # R | advisory/blocking
#   message: ""                        # R | 风险说明

commercial_review:                     # R | 商业复核
  verdict: "pass"                      # R | pass/rework
  notes: ""                            # R | 复核说明
```

Expected: schema file documents every field used by fixtures.

- [ ] **Step 3: Harden `check-paywall.js` required field checks**

In `.agents/skills/paywall-design/scripts/check-paywall.js`, add required text checks before tension checks:

```javascript
function hasPath(content, pathExpr) {
  const parts = pathExpr.split('.');
  let cursor = content;
  for (const part of parts) {
    const re = new RegExp(`^${part}:\\s*(.+)?$`, 'm');
    const match = cursor.match(re);
    if (!match) return false;
  }
  return true;
}
```

Because this script currently uses simple regex rather than a YAML parser, prefer explicit regex checks:

```javascript
const requiredPatterns = [
  [/paywall_chapter:\s*\d+/, '缺少 paywall_chapter'],
  [/strategy:\s*\n[\s\S]*?platform:\s*["']?[^"'\n]+/, '缺少 strategy.platform'],
  [/strategy:\s*\n[\s\S]*?target_free_chapters:\s*\d+/, '缺少 strategy.target_free_chapters'],
  [/candidate_cuts:\s*\n\s*-\s+chapter:\s*\d+/, '缺少 candidate_cuts'],
  [/final_cut:\s*\n[\s\S]*?chapter:\s*\d+/, '缺少 final_cut.chapter'],
  [/final_cut:\s*\n[\s\S]*?free_last_chapter:\s*\d+/, '缺少 final_cut.free_last_chapter'],
  [/final_cut:\s*\n[\s\S]*?paid_first_chapter:\s*\d+/, '缺少 final_cut.paid_first_chapter'],
  [/final_cut:\s*\n[\s\S]*?cliffhanger:\s*["']?[^"'\n]+/, '缺少 final_cut.cliffhanger'],
  [/final_cut:\s*\n[\s\S]*?payoff_promise:\s*["']?[^"'\n]+/, '缺少 final_cut.payoff_promise'],
  [/commercial_review:\s*\n[\s\S]*?verdict:\s*["']?(pass|rework)/, '缺少 commercial_review.verdict'],
];

for (const [pattern, message] of requiredPatterns) {
  if (!pattern.test(paywallContent)) findings.push({ severity: 'blocking', message });
}
```

Also check:

```javascript
const finalChapter = extractNumber(paywallContent, /final_cut:\s*\n[\s\S]*?chapter:\s*(\d+)/);
if (finalChapter && paywallChapter && finalChapter !== paywallChapter) {
  findings.push({ severity: 'blocking', message: `final_cut.chapter (${finalChapter}) 必须等于 paywall_chapter (${paywallChapter})` });
}
```

Expected: invalid fixture fails for multiple schema-level reasons, valid fixture reaches tension checks.

- [ ] **Step 4: Verify compact paywall fixture is used**

Keep `paywall_report.valid.yaml` at `paywall_chapter: 20` and use `tests/fixtures/schema-contract/chapters_index.paywall-valid.yaml` for paywall script verification. Do not use `chapters_index.valid.yaml` for paywall positive checks because it intentionally contains only chapter 1.

Expected: valid paywall fixture can pass deterministic checks against the compact paywall chapters fixture.

- [ ] **Step 5: Update Skill wording**

In `.agents/skills/paywall-design/SKILL.md`, add:

```markdown
`paywall_report.yaml` 必须遵循 `data/schemas/paywall_report.schema.yaml`。生成后运行 `node .agents/skills/paywall-design/scripts/check-paywall.js settings/chapters_index.yaml paywall_report.yaml`，blocking 项必须为 0。
```

In `.agents/skills/daily-write/SKILL.md`, add:

```markdown
如果存在 `paywall_report.yaml`，必须按 `data/schemas/paywall_report.schema.yaml` 读取 `paywall_chapter`、`final_cut.cliffhanger` 和 `final_cut.payoff_promise`，用于判断当前章节是否需要执行卡点前后承诺。
```

Expected: producer and consumer both mention the schema.

- [ ] **Step 6: Update audit document**

In `docs/SKILL_CONTRACT_AUDIT.md`, update `paywall_report.yaml` from “缺 dedicated schema” to “已新增 dedicated schema and check-paywall field checks”.

Expected: audit reflects new paywall schema status.

- [ ] **Step 7: Verify paywall contract**

Run:

```bash
node .agents/skills/paywall-design/scripts/check-paywall.js tests/fixtures/schema-contract/chapters_index.paywall-valid.yaml tests/fixtures/schema-contract/paywall_report.valid.yaml
```

Expected: pass.

Run:

```bash
node .agents/skills/paywall-design/scripts/check-paywall.js tests/fixtures/schema-contract/chapters_index.paywall-valid.yaml tests/fixtures/schema-contract/paywall_report.invalid.yaml
```

Expected: fail with blocking field errors.

Run:

```bash
rg -n "paywall_report.schema.yaml|candidate_cuts|final_cut|payoff_promise" data/schemas/paywall_report.schema.yaml .agents/skills/paywall-design/SKILL.md .agents/skills/daily-write/SKILL.md docs/SKILL_CONTRACT_AUDIT.md
```

Expected: matches across schema, Skills, and audit.

- [ ] **Step 8: Commit paywall schema**

Run:

```bash
git add data/schemas/paywall_report.schema.yaml .agents/skills/paywall-design/SKILL.md .agents/skills/paywall-design/scripts/check-paywall.js .agents/skills/daily-write/SKILL.md docs/SKILL_CONTRACT_AUDIT.md tests/fixtures/schema-contract
git commit -m "schemas: 添加付费卡点报告合约" -m "主要改动：
- 新增 paywall_report schema
- 增强 check-paywall.js 对报告字段的确定性检查
- 更新 paywall-design 和 daily-write 对付费报告的读写约束
- 同步审计文档中的 paywall_report 状态

验证结果：
- 运行 check-paywall.js 验证有效付费报告夹具通过
- 运行 check-paywall.js 验证缺字段付费报告夹具失败
- 运行 rg 确认 schema、Skill 和审计文档均引用 paywall_report 合约"
```

Expected: commit succeeds.

---

### Task 6: Clarify Outline, Arcs, and Pacing Schema Boundaries

**Files:**
- Modify: `data/schemas/outline.schema.yaml`
- Modify: `templates/default/settings/arcs.yaml`
- Modify: `templates/default/settings/pacing.yaml`
- Modify: `.agents/skills/design-outline/SKILL.md`
- Modify: `.agents/skills/design-outline/scripts/check-pacing.js`
- Modify: `docs/SKILL_CONTRACT_AUDIT.md`

- [ ] **Step 1: Capture baseline outline/arcs/pacing state**

Run:

```bash
sed -n '1,260p' data/schemas/outline.schema.yaml
sed -n '1,220p' templates/default/settings/arcs.yaml
sed -n '1,220p' templates/default/settings/pacing.yaml
sed -n '1,260p' .agents/skills/design-outline/scripts/check-pacing.js
```

Expected: identify whether `pacing.yaml` uses tension range inconsistent with `chapters_index.yaml`.

- [ ] **Step 2: Clarify outline schema scope**

At the top of `data/schemas/outline.schema.yaml`, add or adjust comments:

```yaml
# outline.yaml schema
# 路径: novels/{project_id}/settings/outline.yaml
# 本 schema 约束 settings/outline.yaml 的主结构。
# settings/arcs.yaml、settings/pacing.yaml、settings/notes.yaml 是同一 Skill 的相邻产物，但不由本文件完整约束。
# arcs/pacing 的字段边界由对应模板、Skill 文档和脚本门禁约束；notes 由 data/schemas/notes.schema.yaml 约束。
```

Expected: no ambiguity that one schema magically covers all four design-outline outputs.

- [ ] **Step 3: Align pacing template tension range**

In `templates/default/settings/pacing.yaml`, ensure all comments and examples use tension `1-5`. If the file has an explicit range `1-10`, replace it with `1-5`.

Expected:

```bash
rg -n "1-10|1~10|10" templates/default/settings/pacing.yaml
```

returns no tension-range match.

- [ ] **Step 4: Align check-pacing tension range**

Modify `.agents/skills/design-outline/scripts/check-pacing.js` so values below 1 or above 5 produce blocking findings. If the script already has this logic, leave the behavior unchanged and verify it with the command in Step 8.

Expected: pacing script range matches chapter index range.

- [ ] **Step 5: Clarify arcs template locator fields**

In `templates/default/settings/arcs.yaml`, add comments or minimal structure showing that arcs can be located by chapter or beat:

```yaml
# 叙事弧线模板
# 可被 daily-write 按 chapter_range 或 beat_ref 定位。

arcs: []
# - id: "arc_001"
#   name: ""
#   chapter_range: "1-10"
#   beat_refs:
#     - act: 1
#       sequence: 1
#       beat: 1
#   goal: ""
#   conflict: ""
#   payoff: ""
```

Expected: `daily-write` can understand how to map arcs to chapters/beat refs.

- [ ] **Step 6: Update design-outline Skill wording**

In `.agents/skills/design-outline/SKILL.md`, ensure the schema boundary paragraph says:

```markdown
`data/schemas/outline.schema.yaml` 只约束 `settings/outline.yaml` 的主结构。`settings/arcs.yaml` 和 `settings/pacing.yaml` 由对应模板、`check-pacing.js` 与本 Skill 文档共同约束；`settings/notes.yaml` 必须遵循 `data/schemas/notes.schema.yaml`。
```

Expected: design-outline has clear boundary wording.

- [ ] **Step 7: Update audit document**

In `docs/SKILL_CONTRACT_AUDIT.md`, update the `outline/arcs/pacing` row to say this implementation keeps a single outline schema for `outline.yaml` and clarifies adjacent artifact boundaries through templates/scripts/Skill docs.

Expected: audit no longer says the boundary is unclear.

- [ ] **Step 8: Verify outline boundary**

Run:

```bash
rg -n "outline.schema.yaml|arcs.yaml|pacing.yaml|notes.schema.yaml|1-5|chapter_range|beat_refs" data/schemas/outline.schema.yaml templates/default/settings/arcs.yaml templates/default/settings/pacing.yaml .agents/skills/design-outline/SKILL.md docs/SKILL_CONTRACT_AUDIT.md
```

Expected: matches show explicit boundaries and locator fields.

Run:

```bash
rg -n "1-10|1~10" templates/default/settings/pacing.yaml .agents/skills/design-outline/scripts/check-pacing.js data/schemas/chapters.schema.yaml templates/default/settings/chapters_index.yaml
```

Expected:

```text
No matches.
```

- [ ] **Step 9: Commit outline boundary alignment**

Run:

```bash
git add data/schemas/outline.schema.yaml templates/default/settings/arcs.yaml templates/default/settings/pacing.yaml .agents/skills/design-outline/SKILL.md .agents/skills/design-outline/scripts/check-pacing.js docs/SKILL_CONTRACT_AUDIT.md
git commit -m "schemas: 明确大纲相邻产物边界" -m "主要改动：
- 明确 outline.schema.yaml 只约束 outline.yaml 主结构
- 补充 arcs.yaml 可被章节或 beat_ref 定位的模板说明
- 统一 pacing 与章节索引的 tension 范围
- 更新 design-outline 和审计文档中的 schema 边界说明

验证结果：
- 运行 rg 确认 outline/arcs/pacing/notes 边界说明存在
- 运行 rg 确认 pacing 与章节索引不再出现 1-10 张力范围"
```

Expected: commit succeeds.

---

### Task 7: Final Contract Verification

**Files:**
- Read all modified files

- [ ] **Step 1: Run all deterministic fixture checks**

Run:

```bash
node .agents/skills/design-chapters/scripts/check-chapters.js tests/fixtures/schema-contract/chapters_index.valid.yaml
node .agents/skills/design-chapters/scripts/check-chapters.js tests/fixtures/schema-contract/chapters_index.invalid-template-drift.yaml
```

Expected:

```text
valid fixture exits 0
invalid fixture exits non-zero with blocking findings
```

Run:

```bash
mkdir -p /private/tmp/schema-contract-valid-outlines
cp tests/fixtures/schema-contract/chapter_outlines/chapter_001.md /private/tmp/schema-contract-valid-outlines/
node .agents/skills/design-chapters/scripts/check-outlines.js /private/tmp/schema-contract-valid-outlines
node .agents/skills/design-chapters/scripts/check-outlines.js tests/fixtures/schema-contract/chapter_outlines
```

Expected:

```text
valid-only directory exits 0
mixed directory exits non-zero with blocking findings for chapter_002.invalid.md
```

Run:

```bash
node .agents/skills/paywall-design/scripts/check-paywall.js tests/fixtures/schema-contract/chapters_index.paywall-valid.yaml tests/fixtures/schema-contract/paywall_report.valid.yaml
node .agents/skills/paywall-design/scripts/check-paywall.js tests/fixtures/schema-contract/chapters_index.paywall-valid.yaml tests/fixtures/schema-contract/paywall_report.invalid.yaml
```

Expected:

```text
valid paywall exits 0
invalid paywall exits non-zero with blocking findings
```

- [ ] **Step 2: Verify schema/template references**

Run:

```bash
rg -n "chapter_outline_frontmatter.schema.yaml|notes.schema.yaml|paywall_report.schema.yaml|chapters.schema.yaml|outline.schema.yaml" data/schemas templates/default/settings .agents/skills docs/SKILL_CONTRACT_AUDIT.md
```

Expected: every new schema is referenced by at least one producer/consumer Skill or audit document.

- [ ] **Step 3: Verify old chapter template drift is gone**

Run:

```bash
rg -n "number:|word_count|target_chapters|completed_chapters|tension.*1-10|1~10" data/schemas templates/default/settings .agents/skills/design-chapters .agents/skills/design-outline docs/SKILL_CONTRACT_AUDIT.md
```

Expected: no current-contract matches. If historical explanations remain in `docs/SKILL_CONTRACT_AUDIT.md`, they must explicitly say “旧字段” or “历史漂移”.

- [ ] **Step 4: Verify worktree and commits**

Run:

```bash
git status --short
git log --oneline -8
```

Expected: worktree is clean except user-owned unrelated files. Recent commits include fixture, chapters, outline frontmatter, notes, paywall, and outline-boundary commits.

- [ ] **Step 5: Final response**

Report:

```text
- 新增 schema
- 修改模板和脚本
- 哪些负例/正例验证通过
- 哪些后续项仍未做：Skill Runner、导出配置 schema、data-diagnosis 报告 schema、历史文档隔离
- 是否仍有用户未提交改动
```

Do not claim Python tests pass. They are out of scope unless implementation touched frozen Python.
