---
name: pipeline-chapter-kickoff
description: 从章节想法出发，编排章节创建、状态推进和对应情节点补全，产出可直接开写的新章节。用于用户准备开始一章正文，不想手动拼接 chapter 和 plot 命令时。
when_to_use: 用户准备开写新章节，想同时创建章节卡、推进状态并补上大纲节点
argument-hint: "[章节ID] [一句话目标]"
arguments: chapter_id goal
---

# 任务

把一个章节想法落地为 `可开写章节`。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/chapters/index.yaml`
3. 读取 `{current_path}/plot/outline.md`
4. 若存在，读取 `{current_path}/plot/outline.yaml`

### 预检完整性

按 [预检完整性协议](_protocols/preflight-integrity.md) 检查目标章节 ± 2 章范围内的引用链完整性。发现孤儿索引/文件时暂停并报告。

### 章节存在性检查（三处，缺一不可）

对给定的 `chapter_id`，分别检查：

| 检查点 | 位置 |
|---|---|
| A. 章节文件 | `{current_path}/chapters/{chapter_id}.md` |
| B. 索引条目 | `chapters/index.yaml` 中是否有 `id: {chapter_id}` |
| C. 大纲条目 | `outline.md` 中是否有对应章节节点（搜索 `{chapter_id}` 或章节序号标题） |

**处理规则：**

- 三处全不存在 → 正常创建，继续执行
- 三处全存在 → 提示"章节 {chapter_id} 已完整存在，是否重新初始化？（会清除已有条目）"，等待用户确认后再执行
- 部分存在（残留状态，如只有索引条目但文件已被删除）→ **必须停下来报告**，列出哪些地方有残留、哪些已缺失，询问用户：
  - 选项 A：清理残留后重新创建
  - 选项 B：中止操作，手动检查
  
  **不得在用户确认前自动修改任何文件。**

## 输入参数

- `$0` (chapter_id): 章节 ID，如 `ch012`
- `$1+` (goal): 一句话章节目标
- `--pov`: 可选 POV 角色
- `--after`: 可选插入位置，如 `第11章`

## 执行步骤

### 0. 多章弧线检测

按 [章节容量守卫协议](_protocols/chapter-scope-guard.md) 分析用户的 goal 描述。

**检测逻辑**：如果 goal 中包含多个明显阶段（如"发现线索 → 与对手对峙 → 逃离追杀 → 伤后反思"），识别出每个独立阶段，判断是否需要拆分为多章。

**触发时**：输出多章规划建议，列出每章的核心事件和结尾钩子，等待用户选择：
1. 按建议创建多章（逐章推进，先创建第一章）
2. 只创建第一章，后续再规划
3. 全部放一章
4. 自己指定拆法

**用户确认后才执行创建。** 如果选择多章方案，将后续章节的规划摘要记入当前章节的写作备忘，方便后续 kickoff 时引用。

### 0b. 操作日志

按 [操作日志协议](_protocols/operation-journal.md)，在 `.novel/ops_log.yaml` 记录本次操作（status: in_progress）。检查是否有上次未完成的操作。

### 1. 创建章节卡

调用 `/chapter-create`，创建章节正文文件并在 `chapters/index.yaml` 中登记条目。

### 2. 推进到 outline 阶段

调用 `/chapter-update`，将章节状态设为 `outline`。若用户给出 `--pov`，同步写入 POV；必要时补标题、目标字数等最小元数据。

### 3. 补齐章节级情节细节

将本章的情节细节写入**章节文件**（`chapters/{chapter_id}.md`）的 `## 场景大纲` 区，包括：

- 章节目标
- 时间线位置
- 出场人物
- 事件推进（有画面感的描述，不是会议纪要）
- 本章冲突（角色内心撕裂，不只是外部障碍）
- 结尾钩子

如果本章属于多章弧线（步骤 0 中确认了拆分方案），额外标注：

```markdown
**本章在弧线中的位置**：{{弧线名称}} 的第 {{N}}/{{Total}} 章
**上一章留下的钩子**：{{hook_from_previous}}（无则写"弧线起点"）
**本章结尾交接**：{{交接给下一章的悬念/状态}}
```

**不写入 `outline.md`。** `outline.md` 只存放幕/弧线级结构，不承接章节粒度内容。

如本章涉及新的幕级转折（季度走向、主线拐点），则**另行**调用 `/plot-add` 在 `outline.md` 补充弧线节点，并注明关联章节 ID。

### 4. 钩子回收提醒

读取 `{current_path}/plot/outline.yaml` 的 `foreshadowing` 列表，筛选：

- status 为 `planted` 或 `pending`
- `recovery_deadline` 在本章前后 3 章范围内（含已过期）

按紧迫度分组输出：

```markdown
## 🪝 钩子回收提醒

### 已逾期（应在本章之前回收）
- [f001] 赵宋手背的疤痕（major）— 截止 ch010，已超 2 章
  💡 本章可考虑回收，或 /hook-resolve f001 --extend

### 即将到期（截止在本章附近）
- [f005] 室友的异常电话（minor）— 截止 ch015，还剩 2 章

### 可选回收（本章条件可能满足）
- [f003] 某线索（minor）— recovery_conditions 匹配本章出场人物
```

无匹配钩子时跳过此步，不输出空节。

### 4b. 设定有效期提醒

扫描 `{current_path}/worldbuilding/entries/*.yaml`，找出：

- `valid_until` 对应的章节在本章附近（前后 3 章）→ 提醒设定即将失效
- `expiry_trigger.type` 为 `event` 且该事件可能在本章发生 → 提醒
- 已过期但无后继条目（`superseded_by` 为空）→ 警告

```markdown
## ⏳ 设定有效期提醒

- 📋 现实抚平机制（rule_001）— 将在 ch030 后失效
  💡 本章是否需要体现规则变化的征兆？
  💡 后续可用 /setting-edit rule_001 --evolve 创建新版本

- ⚠️ 灰域展开规则（rule_003）— 已过期（ch025 后），但无后继版本
  💡 /setting-add [新名称] --supersedes rule_003
```

无匹配设定时跳过此步。

### 5. 输出开写前清单

至少明确：

- 本章要完成的剧情目标
- POV
- 冲突点
- 结尾钩子
- 本章可回收的钩子（若有）

## 输出格式

```markdown
## CurrentState
- 阶段：可开写章节
- 章节：{{chapter_id}}
- 目标：{{goal}}
- 状态已推进到 outline

## Risks
- {{risk_1}}
- {{risk_2}}

## NextTasks
1. 补齐本章开场场景与 POV 进入方式
2. 确认中段冲突升级点
3. 写出结尾钩子或悬念句

## RecommendedCommands
- /chapter-review {{chapter_id}}
- /chapter-update {{chapter_id}} --status draft
- /plot-add {{node}} {{content}}
```

## 注意事项

- 这是开工流程，不负责完整写正文
- 操作完成后更新 ops_log 为 completed
- 存在性检查必须三处全查，发现任何残留都要停下报告，不得静默覆盖
- 章节级细节（场景/冲突/钩子）写入章节文件，不写入 `outline.md`
- `outline.md` 只在有幕级转折时才更新，且需明确标注关联章节 ID
