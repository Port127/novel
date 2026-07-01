# Schema Alignment Design — nv_20260625_00t3

**Date**: 2026-07-01
**Scope**: 将 `novels/nv_20260625_00t3` 的 9 个设定文件与项目最新 schema/template 定义对齐
**Method**: 方案 B — 逐文件分步迁移，每个 commit 独立可回滚
**Migration strategy**: 内容优先 — 保留所有创意内容，适配到 Schema 结构
**Enum policy**: 不强行映射 — enum 为文档型注释（99% 无代码校验），保留原始值

---

## 1. Background

`nv_20260625_00t3` 是一本处于 planning 阶段的都市脑洞网文，目标番茄小说平台，800 章 / 320 万字。项目已完成丰富的设定内容（世界观、角色、大纲、弧线、节奏、选题报告），但文件结构与项目 V4 schema 存在严重不对齐。

### 1.1 问题总结

| 文件 | 对齐度 | 严重等级 | 核心问题 |
|------|--------|----------|----------|
| `project.yaml` | 90% | 低 | `genre: 都市脑洞` 不在 schema 枚举内（保留，见 enum policy） |
| `scout_report.yaml` | 95% | — | 基本完美对齐，不纳入修复 |
| `chapters_index.yaml` | 85% | 低 | 多 2 个超纲字段，低风险，不在本次范围 |
| `pacing.yaml` | 70% | 中 | 中文键名，无独立 schema，不在本次范围 |
| `arcs.yaml` | 70% | 中 | 中文键名，无独立 schema，不在本次范围 |
| **`characters.yaml`** | **20%** | **P1** | 分组对象 vs schema 要求的扁平 `characters[]` 数组 |
| **`outline.yaml`** | **25%** | **P1** | premise 对象化、缺 `acts[]`、hooks 结构错误 |
| **`notes.yaml`** | **0%** | **P1** | 自由笔记 vs 结构化状态追踪系统 |
| **`worldbuilding.yaml`** | **15%** | **P1** | 缺 `world_type` 等必填字段，全部自定义结构 |

### 1.2 Enum 调研结论

- 项目 schema 中的枚举 **99% 是文档型注释**（`# 可选值：...`），无代码校验
- **唯一例外**：`notes.foreshadowing[].status` 被 `check-notes.js` 校验（`open/resolved/dropped`）
- 没有中央 enum 注册表，各 schema 独立定义
- 模板与 schema 之间本身就存在不一致（`setting_type` vs `world_type`、`成长` vs `成长弧线`）
- **结论**：不强行映射枚举值，保留原始创意用语

### 1.3 目录问题

| 问题 | 当前 | 期望 |
|------|------|------|
| 正文路径漂移 | `content/chapters/`（空） | `content/chapter_*.md`（直接在 content/ 下） |
| 缺少蓝图目录 | 不存在 | `settings/chapter_outlines/` |

---

## 2. Design Decisions

### D1: 迁移策略 — 内容优先

保留所有创意内容，重新组织到 Schema 标准字段中。Schema 无对应字段的内容作为扩展字段保留，零信息丢失。

### D2: notes.yaml — 拆分

当前 notes.yaml 是创意备忘（金手指规则/许嵩接触线等），与 Schema 定义的状态追踪系统用途完全不同。

- **创意备忘** → 迁移到 `references/mechanics.yaml`（新文件）
- **notes.yaml** → 按 Schema 重建结构化追踪骨架

### D3: outline.yaml 与 arcs.yaml 的边界

- **outline.yaml**：`acts[]` 写高层概要（每幕 2-3 个 sequence 的框架描述），与 arcs.yaml 互补不重复
- **arcs.yaml**：保留现有的详细章节节拍，不受影响

### D4: Enum 处理 — 保留原始值

| 字段 | 保留值 | 不映射到 |
|------|--------|----------|
| `project.genre` | `都市脑洞` | ~~`都市`~~ |
| `characters[].archetype` | `重生逆袭型` / `青梅竹马型` | ~~`废柴逆袭` / `其他`~~ |
| `outline.theme[]` | `商业逆袭/多女主恋爱/副本冒险/青春校园` | ~~`成长/爱情/探索/其他`~~ |
| `outline.tone[]` | `轻松/爽文/温馨` | 保留 |
| `characters[].arc.type` | `成长弧线` | 恰好匹配，保留 |

### D5: 数据一致性修复

- `outline.yaml` 原 `premise.target_chapters: 500` 与 `project.yaml` 的 `target.chapters: 800` 冲突 → 迁移后不保留 `target_chapters`（该字段属于 project.yaml）

---

## 3. Detailed Migration Plan

### 3.1 Commit 1: `worldbuilding.yaml`

**策略**：顶部新增 Schema 必填字段作为结构骨架，现有内容重新归类到对应 Schema 字段下，保留扩展字段。

**Schema 字段映射**：

| Schema 字段 | 内容来源 | 目标值 |
|-------------|----------|--------|
| `world_type` | 无（缺失） | `"都市"` |
| `setting_period` | `era_context.year` + `era_context.month` | `"2009年12月"` |
| `core_rules[]` | 从 notes 金手指规则和 foreknowledge_advantages.limitations 提取 | 时代铁律类规则 |
| `power_system` | notes 金手指规则 + foreknowledge_advantages | `name: "梦入歌曲"`, `type: "异能"`, `ranks[]` 从自主权成长线映射（初期/中期/后期 = 3 级），`rules[]` 从金手指规则提取，`limitations[]` 从 limitations 提取 |
| `factions[]` | 从 school_info 提取 | 合工大、中科大、安医大等关键势力 |
| `locations[]` | `school_info` | 每个学校一个 location 条目，含 sub_locations |
| `lore.history[]` | `era_context.key_events` | 时代大事件 |

**扩展字段保留**（Schema 外，内容保留）：

| 字段 | 说明 |
|------|------|
| `university_life` | 完整保留（academics/campus_culture/tech_environment/career_landscape） |
| `social_context` | 完整保留（economy/culture/technology） |
| `foreknowledge_advantages` | 保留 business_opportunities/tech_advantages/cultural_advantages（limitations 已迁入 power_system） |

### 3.2 Commit 2: `characters.yaml`

**策略**：分组对象 → 扁平 `characters[]` 数组，每个条目带 `role` 字段区分。

**角色映射**：

| 当前结构 | 目标 | role | archetype | 处理要点 |
|----------|------|------|-----------|----------|
| `protagonist` | `characters[0]` | `protagonist` | `重生逆袭型`（保留） | arc.type: `成长` → `成长弧线`（恰好匹配枚举）；age/school/major → 扩展字段 `background` |
| `heroine_1` | `characters[1]` | `supporting` | `青梅竹马型`（保留） | `romance_arc` → `arc`（type: 成长弧线）；新增 `relationships[]` 指向男主；background/school → 扩展字段 |
| `heroine_2` | `characters[2]` | `supporting` | `待定` | 同上结构，内容保留待定 |
| `heroine_3` | `characters[3]` | `supporting` | `待定` | 同上 |
| `supporting_characters[0]` | `characters[4]` | `supporting` | `其他` | 原 `role: "室友/合伙人"` 并入 description；`id` 丢弃 |
| `supporting_characters[1]` | `characters[5]` | `supporting` | `其他` | 原 `role: "高中同学（安农大）"` 并入 description |
| `antagonists[0]` | `characters[6]` | `antagonist` | `反派` | 新增 psychology 骨架（obsession 从 motivation 提取）；新增 arc 骨架 |
| `antagonists[1]` | `characters[7]` | `antagonist` | `反派` | 同上 |

**超纲字段处理**：

| 字段 | 处理 |
|------|------|
| `design_principles` | 移出到 `references/design_principles.yaml` |
| `relationships: []`（顶层空数组） | 丢弃，关系改为各角色内的 `relationships[]` |
| 各女主的 `background`/`romance_arc` | 保留为扩展字段 |

### 3.3 Commit 3: `outline.yaml`

**策略**：拆 premise 为扁平字段，从 arcs.yaml 提炼高层 `acts[]`，伏笔框架重构为 `plotlines[]`。

**premise 拆解**：

| Schema 字段 | 来源 | 目标值 |
|-------------|------|--------|
| `premise` (string) | `premise.statement` | 直接提取 |
| `theme[]` | `premise.themes` | 提升为顶层：`[商业逆袭, 多女主恋爱, 副本冒险, 青春校园]` |
| `tone[]` | `premise.tones` | 提升为顶层：`[轻松, 爽文, 温馨]` |

**丢弃**：`premise.target_chapters`（与 project.yaml 重复且冲突）、`premise.structure_note`（内容合并到 acts 描述）

**acts[] 结构**：

从 arcs.yaml 的 6 个 arc 提炼高层概要，每个 act 包含 2-3 个 sequence，每个 sequence 包含 2-5 个 beats。beat 带 `chapter`（int）、`description`（≥30字）、`tension`（1-5）。

| act | title | chapters | 来源 |
|-----|-------|----------|------|
| 1 | 穿越觉醒 | [1, 5] | arc_1_穿越觉醒 |
| 2 | 庐州月副本 | [6, 14] | arc_2_庐州月副本 |
| 3 | 宝藏与觉醒 | [15, 25] | arc_3_宝藏与觉醒 |
| 4 | 素颜副本+创业加速 | [26, 50] | arc_4_素颜副本 |
| 5 | 工作室升级+新角色 | [51, 75] | arc_5_工作室升级 |
| 6 | 卷一高潮 | [76, 100] | arc_6_卷一高潮 |

每个 act 含 `turning_point`（从 arcs 的关键节拍提取）。

**hooks → plotlines 映射**：

| 原结构 | 目标 | 处理 |
|--------|------|------|
| `hooks.core` (f001-f004) | `plotlines[0-3]` | name 保留，setup/development/payoff 合并为 description，importance: primary，chapters_covered 从 payoff 推断 |
| `hooks.business` (f005-f006) | `plotlines[4-5]` | 同上 |
| `hooks.dungeon` (f007) | `plotlines[6]` | 同上 |
| — | `hooks: []` | 暂空，留给 design-chapters 阶段填充 |
| — | `pacing_curve: []` | 暂空 |

### 3.4 Commit 4: `notes.yaml` 拆分

**4a: 新建 `references/mechanics.yaml`**

从当前 notes.yaml 整体迁移以下段落（保持自由格式不变）：
- `穿越设定`
- `金手指规则`
- `许嵩接触线`
- `入梦机制`
- `梦境奖励示例`
- `自主权成长线`

**4b: 重写 `settings/notes.yaml`**

按 Schema 重建结构化骨架：

```yaml
version: 1

tracking:
  recent_chapters: []
  ten_chapter_summaries: []
  volume_overview:
    - volume: 1
      goal: "重生回归 + 初恋重逢 + 第一桶金"
      current_state: "未开始"
  character_states: []
  foreshadowing:
    - id: f001
      planted_chapter: 0
      status: open
      planned_resolution_chapter: 400
      note: "金手指规则 — 第一卷建立，第四卷完全掌握"
    - id: f002
      planted_chapter: 0
      status: open
      planned_resolution_chapter: 350
      note: "女主一的真实身份 — 第一卷埋伏，第三-四卷收束"
    - id: f003 ~ f007
      # ... 共 7 条伏笔，从原 outline.yaml hooks 转换

preferences:
  style_notes: []
  banned_settings: []
  pending_confirmations: []
```

`foreshadowing.status` 严格遵守枚举 `open/resolved/dropped`（唯一有 `check-notes.js` 校验的字段）。

### 3.5 Commit 5: 目录修复

| 操作 | 路径 | 说明 |
|------|------|------|
| 删除 | `content/chapters/` | 废弃路径，空目录 |
| 新建 | `settings/chapter_outlines/.gitkeep` | design-chapters 阶段的产物目录 |
| 新建 | `references/mechanics.yaml` | Commit 4 的产物（在此 commit 统一提交） |

---

## 4. Out of Scope

| 项 | 原因 |
|----|------|
| `chapters_index.yaml` 超纲字段（`total_chapters`/`completeness`） | 低风险，可在 design-chapters 阶段顺手清理 |
| `arcs.yaml` / `pacing.yaml` 中文键名 | 无独立 schema，风格差异不影响功能 |
| Schema 文件本身的 enum 注释更新 | 项目基础设施改进，与本小说迁移无关 |
| `templates/default/` 与 schema 不一致 | 项目级问题，不在本小说修复范围 |
| `REFACTOR_SUMMARY.md` | 历史文档，不需要改动 |

---

## 5. Commit Plan

| 序号 | 涉及文件 | 说明 |
|------|----------|------|
| 1 | `settings/worldbuilding.yaml` | 补 schema 骨架字段，现有内容重新归类 |
| 2 | `settings/characters.yaml` | 分组对象 → `characters[]` 扁平数组 |
| 3 | `settings/outline.yaml` | 拆 premise、补 acts、hooks → plotlines |
| 4 | `settings/notes.yaml` + `references/mechanics.yaml` | 创意备忘迁出，新建结构化 notes |
| 5 | 删除 `content/chapters/` + 新建 `settings/chapter_outlines/.gitkeep` + 新建 `references/design_principles.yaml` | 目录和文件规范化 |

Commit message 遵循 commit-msg skill。

---

## 6. Success Criteria

- [ ] 每个文件的核心 Schema 必填字段存在且格式正确
- [ ] 所有原始创意内容可在迁移后的文件中找到（零丢失）
- [ ] `references/mechanics.yaml` 包含原 notes.yaml 的全部创意备忘
- [ ] `references/design_principles.yaml` 包含原 characters.yaml 的 design_principles
- [ ] `content/chapters/` 目录已删除
- [ ] `settings/chapter_outlines/` 目录已创建
- [ ] 5 个 commit 各自独立可回滚
- [ ] `notes.foreshadowing[].status` 全部为 `open/resolved/dropped` 之一
