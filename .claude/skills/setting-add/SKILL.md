---
name: setting-add
description: 创建或更新一条设定集条目，写入 worldbuilding/entries/ 并更新索引。支持从 ingestion_brief 批量导入，也支持单条手动添加。
when_to_use: 用户想要添加一条世界观设定（规则、势力、地理、术语等），或在 draft-ingest 后批量落地已确认的设定。
argument-hint: "[设定名称] [--category 类别]"
arguments: name
---

# 任务

创建一条结构化的设定条目，写入 `worldbuilding/entries/` 目录。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 确认 `{current_path}/worldbuilding/entries/` 目录存在，不存在则创建
3. 若存在 `{current_path}/ingestion_brief.md`，读取以获取上下文

## 输入参数

- `$0` (name): 设定名称（必需）
- `--category`: 设定类别，可选值：
  - `world_rule`：世界规则（自然法则、禁忌）
  - `power_system`：力量体系（能力、等级、代价）
  - `faction`：势力与组织
  - `geography`：地理空间
  - `lore`：背景知识（历史、文化）
  - `terminology`：术语定义
  - `species`：种族/物种
  - `artifact`：器物/道具
- `--status`: `tentative`（默认）| `confirmed`
- `--quick`: 快捕模式——只记一句话，自动填充上下文，不打断写作心流
- `--from`: 从文件或引用内容中提取设定（见步骤 0b）
- `--batch`: 从 ingestion_brief 批量创建（见步骤 4）

## 执行步骤

### 0. 快捕模式（--quick）

当指定 `--quick` 时，跳过所有交互，最小化写入：

1. 自动感知当前写作章节：
   - 从 `chapters/index.yaml` 中找到状态为 `draft` 的章节作为 `source`
   - 若有多个 draft 章节，取 `updated` 最近的
   - 若无 draft 章节，`source` 设为 "写作中灵感"

2. 将 `$0` 整句作为 `summary`，同时用作 `description`

3. 自动推断 `category`（从关键词判断，如"能量""力量""等级"→ power_system，"势力""组织"→ faction）；若无法推断，默认 `world_rule`

4. 写入条目：
   - `status: tentative`
   - `source: "ch005 写作中灵感"`（自动填充）
   - `open_questions: ["待补充完整描述和规则"]`
   - 其余字段留空

5. 更新索引和 state（同标准流程）

6. 输出极简确认：
   ```
   📌 已快捕：{{name}}（{{category}}，tentative）
   📄 entries/{{id}}.yaml
   💡 后续补全：/setting-edit {{id}}
   ```

**快捕的设定会在 `/pipeline-setting-consolidate` 时统一补全和确认。**

---

### 0b. 引用模式（--from）

当指定 `--from` 时，按 [引用提取协议](_protocols/from-extraction.md) 执行提取与确认流程。

提取重点：识别规则、势力、地理、术语等设定要素；推断 category、summary、description。每个独立设定点拆为一条条目。

可与 `--quick` 组合使用：`--from chapters/ch003.md --quick` 会提取后直接按快捕模式写入，不逐条确认。

---

### 1. 确定设定内容（标准模式）

如果用户提供了详细描述，直接使用。

如果只提供了名称：
- 检查 `ingestion_brief.md` 中是否有相关提取
- 检查 `worldbuilding/setting.md` 或草稿中是否有相关描述
- 若都没有，向用户询问核心内容

### 2. 构造设定条目

基于模板 `worldbuilding/entries/_template.yaml` 填充内容。

关键要求：
- `summary` 必须在一句话内说清楚这条设定是什么
- `description` 要足够详细，让其他 skill 可以引用
- `plot_links` 尽量填写（与大纲节点关联）
- `setting_links` 填写与其他设定的依赖关系（如力量体系依赖某条世界规则）
- `source` 必须标明来源（草稿行号、用户口述等）
- `open_questions` 记录任何模糊点

### 3. 写入文件

文件命名：`{current_path}/worldbuilding/entries/{id}.yaml`

其中 `id` 格式为 `{category}_{三位序号}`，如 `rule_001`、`faction_002`。
序号在同 category 内递增。

### 4. 批量模式（--batch）

当指定 `--batch` 时：
- 读取 `ingestion_brief.md` 中的世界规则部分
- 将"已定义"的规则创建为 `status: confirmed` 的条目
- 将"已暗示未展开"的规则创建为 `status: tentative` 的条目
- "规则缺口"不创建条目，但记录到 `worldbuilding/gaps.md`
- 每条创建前向用户展示，等待确认

### 5. 更新索引

更新 `worldbuilding/worldbuilding.yaml` 的对应分类，添加条目引用：

```yaml
entries:
  - id: rule_001
    name: "现实抚平机制"
    category: world_rule
    status: confirmed
    file: entries/rule_001.yaml
```

### 6. 更新状态

更新 `{current_path}/.novel/state.yaml`：
- `project.updated`：今天日期

## 输出格式

```
✅ 设定条目已创建

📋 {{name}}
🏷️ 类别：{{category}}
📄 文件：worldbuilding/entries/{{id}}.yaml
🔗 状态：{{status}}

关联剧情：{{plot_links 或 "暂无"}}
开放问题：{{open_questions 或 "无"}}

下一步：
   /setting-add [名称]              继续添加
   /worldbuilding-review            检查设定完整性
```

## 注意事项

- 一条设定只解决一个概念，不要把力量体系的所有规则塞进一条
- 设定之间可以互相引用（通过 id）
- `tentative` 状态的设定在写作时会被标记提醒
- 批量导入时要逐条确认，不要一次性全部写入
