---
name: setting-edit
description: 编辑已有的设定集条目，支持修改内容、状态流转（tentative→confirmed→deprecated）和关联更新。
when_to_use: 用户想修改一条世界观设定的内容、状态或关联关系
argument-hint: "[设定名称或ID] [修改内容]"
arguments: target changes
---

# 任务

编辑 `worldbuilding/entries/` 下的已有设定条目，并同步更新索引。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 确认 `{current_path}/worldbuilding/entries/` 目录存在
3. 定位目标条目：
   - 按 ID 精确匹配（如 `rule_001`）
   - 按名称模糊匹配
   - 若无匹配，提示用户并列出现有条目

## 输入参数

- `$0` (target): 设定名称或 ID（必需）
- `$1+` (changes): 修改内容描述

支持的修改格式：
- `/setting-edit 现实抚平机制 补充约束：触发后有冷却期`
- `/setting-edit rule_001 --status confirmed`
- `/setting-edit 污染体系 描述改为：...`
- `/setting-edit faction_001 --deprecated 已被后续设定取代`
- `/setting-edit rule_002 --link plot:inciting 作为引发事件的核心规则`
- `/setting-edit rule_001 --evolve 融合进入第二阶段后规则改变`
- `/setting-edit rule_001 --valid-until ch030`
- `/setting-edit rule_001 --valid-until 灰域崩塌后`

## 字段映射

| 用户关键词 | YAML 字段 |
|-----------|-----------|
| 名称 | `name` |
| 描述/内容 | `description` |
| 概要/摘要 | `summary` |
| 规则 | `rules` |
| 约束/限制 | `constraints` |
| 状态 | `status` |
| 类别 | `category` |
| 关联剧情 | `plot_links` |
| 关联角色 | `character_links` |
| 关联设定/依赖 | `setting_links` |
| 来源 | `source` |
| 开放问题 | `open_questions` |
| 生效起点 | `valid_from` |
| 失效条件/到期 | `valid_until` |
| 过期触发 | `expiry_trigger` |
| 取代/演化 | `supersedes` / `superseded_by` |

## 执行步骤

### 1. 读取条目

读取 `{current_path}/worldbuilding/entries/{id}.yaml`。

### 2. 状态守卫

**状态流转规则：**

| 当前状态 | 允许转为 | 需要确认 |
|---------|---------|---------|
| `tentative` | `confirmed` / `deprecated` | 否 |
| `confirmed` | `deprecated` | **是** |
| `deprecated` | `confirmed`（重新激活） | **是** |

如果将 `confirmed` 设定改为 `deprecated`，执行影响分析：

a) 扫描 `plot_links` 和 `character_links`
b) 检查 `worldbuilding/worldbuilding.yaml` 中引用此条目的位置
c) 检查 `worldbuilding/setting.md` 中是否提及此设定

d) 向用户展示影响：

```
⚠️ 设定废弃影响分析

📋 设定：{{name}}（{{id}}）
📌 当前状态：confirmed → deprecated

关联影响：
  - 剧情关联：{{plot_links 列表}}
  - 角色关联：{{character_links 列表}}
  - 索引引用：worldbuilding.yaml 中 {{位置}}

废弃后：
  - 条目文件保留，status 标记为 deprecated
  - 索引中标记为 deprecated（不删除）
  - 关联剧情/角色需要手动检查是否仍成立

确认执行？(Y/N)
```

如果修改 `confirmed` 条目的**核心内容**（description, rules, constraints），也需提示：

```
⚠️ 此设定已确认，修改核心内容可能影响已写章节和关联剧情。
确认修改？(Y/N)
```

### 2b. 演化模式（--evolve）

当指定 `--evolve` 时，进入"基于当前条目创建新版本"的快捷流程：

1. **读取当前条目**完整内容
2. **询问用户**：什么改变了？（用户描述差异部分）
3. **调用 `/setting-add`**：
   - 自动带上 `--supersedes {当前条目ID}`
   - 继承当前条目的 `category`、`plot_links`、`character_links`
   - 只修改用户指定的差异字段
   - 新条目名称建议在旧名后加版本标识，如"现实抚平机制（第二阶段）"，但用户可自定义
4. **旧条目自动处理**：由 `setting-add --supersedes` 完成（标记 deprecated + 写入 superseded_by）
5. **触发影响扫描**：检查旧版本设定在已写章节中的使用情况

输出：
```
🔄 设定演化完成

旧版：{{旧名}}（{{旧ID}}）→ deprecated
新版：{{新名}}（{{新ID}}）→ {{status}}

📝 变更摘要：{{差异描述}}
📖 旧版有效范围：{{valid_from}} ~ {{valid_until}}
📖 新版生效自：{{valid_from}}

{{影响扫描结果}}
```

### 3. 执行变更

更新 `{current_path}/worldbuilding/entries/{id}.yaml` 中的目标字段。

如果状态发生变更，追加 `lifecycle` 记录：

```yaml
lifecycle:
  - from: tentative
    to: confirmed
    reason: "写入第3章后确认可用"
    date: {{今天日期}}
```

如果新增 `setting_links`，检查目标设定是否存在。

刷新 `updated` 为今天日期。

### 4. 同步索引

更新 `worldbuilding/worldbuilding.yaml`：
- 如果修改了 `name`、`category` 或 `status`，同步索引条目
- 如果修改了 `summary`，同步 `core_concepts` 或 `factions_summary` 中的 `one_liner`（若有对应条目）

### 5. 更新状态

更新 `{current_path}/.novel/state.yaml`：
- `project.updated`：今天日期

### 6. 编辑后影响扫描

按 [编辑后影响扫描协议](_protocols/post-edit-impact-scan.md) 执行。

**触发条件**：本次修改涉及 `description`、`rules`、`constraints` 等核心内容字段。纯元数据修改（`status` 流转、`source`、`open_questions`）跳过此步。

**扫描逻辑**：

1. 从本条目的 `plot_links` 和 `character_links` 找到关联章节
2. 扫描已写章节（status 为 `draft` / `revise` / `done`）正文，检查是否存在与**修改后设定**矛盾的描述
3. 输出影响扫描结果（无论有无冲突都报告）

**只报告，不修改任何章节文件。**

## 输出格式

```
✅ 设定条目已更新

📋 {{name}}（{{id}}）
📝 修改内容：
   - {{字段}}：{{旧值}} → {{新值}}
🔗 状态：{{status}}

📄 已更新：
   - worldbuilding/entries/{{id}}.yaml
   - worldbuilding/worldbuilding.yaml

{{影响扫描结果——见 _protocols/post-edit-impact-scan.md 输出格式}}

下一步：
   /setting-edit [名称]              继续编辑
   /worldbuilding-review            检查设定完整性
   /consistency-check               全面一致性检查
```

## 注意事项

- 一次只修改一条设定，避免批量误操作
- `deprecated` 条目不删除，保留历史记录
- 修改 `confirmed` 设定的核心内容需要用户确认
- 修改 `name` 时，如果其他条目通过 ID 引用此条目，引用不受影响
- 添加 `plot_links` 或 `character_links` 时验证目标是否存在
