---
name: project-lint
description: 机械化验证项目文件完整性、索引一致性、命名规范和操作日志健康度。把协议中的"软约束"变成可执行检查。
when_to_use: 用户想确认项目文件没有损坏或不一致，或在重要操作（kickoff/draft/polish）前做快速健康检查。也可被其他 skill 嵌入调用。
argument-hint: "[--fix] [--scope chapters|characters|settings|hooks|ops]"
---

# 任务

对当前项目执行机械化一致性检查，输出通过/警告/错误三级报告。与 `/novel-doctor` 的区别：doctor 侧重目录结构和配置格式，lint 侧重**数据引用链的正确性**。

> 设计原则（来自 OpenAI Harness Engineering）：  
> "当文档不够时，将规则转化为代码。"  
> Linter 的错误消息中直接嵌入修复命令。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 确认项目目录存在

## 输入参数

- `--fix`：自动修复可安全修复的问题（如删除孤儿索引条目、补缺 `last_reviewed` 字段）。默认只报告不修复。
- `--scope`：只检查指定领域。可选值：`chapters`、`characters`、`settings`、`hooks`、`ops`、`all`（默认 `all`）

## 检查项

### 1. 章节文件-索引一致性（scope: chapters）

| 检查 | 方法 | 级别 |
|------|------|------|
| 索引有条目但无文件 | `chapters/index.yaml` 中的 id 在 `chapters/` 下无对应 `.md` | 错误 |
| 有文件但索引无条目 | `chapters/` 下的 `.md`（排除 `_v*.md` 和 `_review.yaml`）在 index 中无对应 id | 错误 |
| 版本文件无索引 | `chapters/{id}_v*.md` 存在但 index 中该章节无 `versions` 字段 | 警告 |
| 状态倒退 | index 中章节 status 不在合法流转路径上（idea → outline → draft → revise → final） | 错误 |
| 字数偏差 | `word_actual` 与文件实际字数偏差 > 20% | 警告 |

**错误消息示例**：
```
❌ [chapters] 索引孤儿：index.yaml 含 ch003 但 chapters/ch003.md 不存在
   → 修复：删除 index 条目（/project-lint --fix）或创建文件（/chapter-create ch003）
```

### 2. 角色文件-索引一致性（scope: characters）

| 检查 | 方法 | 级别 |
|------|------|------|
| 索引有条目但无文件 | `character_index.yaml` 中 name 无对应 `.yaml` | 错误 |
| 有文件但索引无条目 | `characters/*.yaml`（排除 index/relations/relation_events）不在索引中 | 错误 |
| 五件套缺失 | 角色卡缺少 fatal_flaw / obsession / soft_spot / misbelief / contrast_habit 中任何一个 | 警告 |
| speech_pattern 缺失 | 已出场角色（chapters/index.yaml 的 characters_involved 中出现过）无 speech_pattern | 警告 |

### 3. 设定文件-索引一致性（scope: settings）

| 检查 | 方法 | 级别 |
|------|------|------|
| 索引有条目但无文件 | `worldbuilding.yaml` 中 id 无对应 `entries/*.yaml` | 错误 |
| 有文件但索引无条目 | `entries/*.yaml`（排除 _template）不在 worldbuilding.yaml 中 | 错误 |
| 过期无后继 | `valid_until` 已触发但 `superseded_by` 为空 | 警告 |
| 长期 tentative | 状态为 tentative 且项目已有 3+ 章 draft | 警告 |

### 4. 钩子健康度（scope: hooks）

| 检查 | 方法 | 级别 |
|------|------|------|
| 逾期 major | `outline.yaml` 中 planted 状态的 major 钩子已过 recovery_deadline | 错误 |
| 逾期 minor | planted 的 minor 钩子已过 deadline | 警告 |
| 无截止日期 | major/minor 钩子无 recovery_deadline | 警告 |
| 引用章节不存在 | 钩子的 planted_chapter 或 recovery_chapter 在 index 中不存在 | 错误 |

### 5. 操作日志健康度（scope: ops）

若 `{current_path}/.novel/ops_log.yaml` 不存在，输出"ℹ️ 操作日志不存在，跳过 ops 检查"并跳过本节。

| 检查 | 方法 | 级别 |
|------|------|------|
| 遗留 in_progress | `ops_log.yaml` 中有 `status: in_progress` 的条目 | 错误 |
| 日志过大 | ops_log 条目数 > 100 | 警告（建议清理已完成条目） |

### 6. 交叉引用完整性（scope: all）

| 检查 | 方法 | 级别 |
|------|------|------|
| 关系引用幽灵角色 | `relations.yaml` 中的角色名不在 character_index 中 | 错误 |
| 大纲引用幽灵章节 | `outline.md` 中引用的 chXXX 在 index 中不存在 | 警告 |
| 时间线引用幽灵角色 | `timeline/main.yaml` 中的 characters 不在 character_index 中 | 警告 |

### 7. 命名规范（scope: characters）

读取 `{current_path}/.novel/meta.yaml` 的 `naming` 配置。若 `naming` 字段不存在或为空，输出"ℹ️ 未配置命名规范，跳过命名检查"并跳过本节。

| 检查 | 方法 | 级别 |
|------|------|------|
| 禁止模式命中 | 角色名匹配 `forbidden_patterns` 中的正则 | 警告 |
| 同音混淆 | 两个角色名拼音完全相同（需简单拼音比对） | 警告 |

## --fix 行为

仅修复**安全的、无歧义的**问题：

| 可自动修复 | 操作 |
|-----------|------|
| 索引孤儿条目（无对应文件） | 从索引中删除该条目 |
| 操作日志遗留 in_progress | 将 status 改为 failed，附注"由 project-lint 标记" |
| 操作日志过大 | 清理 30 天前的 completed 条目 |

**不会自动修复**的问题（只报告）：
- 孤儿文件（有文件无索引）——可能是用户手动创建的
- 五件套/speech_pattern 缺失——需要创作决策
- 钩子逾期——需要叙事决策
- 命名冲突——需要用户判断

## 输出格式

```
🔍 项目 Lint 报告

检查范围：{{scope}}
━━━━━━━━━━━━━━━━━━━━

❌ 错误（{{count}}）
1. [chapters] 索引孤儿：index.yaml 含 ch003 但文件不存在
   → /chapter-create ch003 或 /project-lint --fix
2. [hooks] 逾期 major 钩子：「庄怀瑾的秘密」已过截止章节 ch010
   → /hook-resolve 庄怀瑾的秘密 --recover ch012 或 --extend

⚠️ 警告（{{count}}）
1. [characters] 赵宋 缺少 speech_pattern
   → /character-edit 赵宋 补充语言画像
2. [settings] rule_001 长期 tentative（已有 5 章 draft）
   → /setting-edit rule_001 --status confirmed

✅ 通过（{{count}}）
- [chapters] 文件-索引一致 ✓
- [ops] 操作日志健康 ✓

━━━━━━━━━━━━━━━━━━━━
📊 错误 {{err}} / 警告 {{warn}} / 通过 {{pass}}
```

## 注意事项

- 本 skill 只做**机械化检查**，不做语义分析（语义分析是 `/consistency-check` 的职责）
- `--fix` 只修改索引文件和操作日志，不创建/删除内容文件
- 可被 `pipeline-chapter-kickoff` 和 `pipeline-draft-polish` 在前置检查中嵌入调用（替代或增强 preflight-integrity）
- 错误消息必须包含修复命令，让用户（或 AI）知道下一步做什么
