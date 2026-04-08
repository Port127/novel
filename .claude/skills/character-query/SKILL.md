---
name: character-query
description: 查询角色信息
when_to_use: 用户想查看角色详细信息、搜索角色，或查看某个角色的完整故事线
argument-hint: "[查询内容] [--storyline]"
arguments: query
---

# 任务

查询角色信息。支持角色卡查看、筛选检索和完整故事线追踪。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`

## 输入参数

- `$0+` (query): 查询内容，支持多种形式：
  - 角色名：`张三`
  - 特定信息：`张三的武器`
  - 筛选条件：`主角有哪些`
  - 关系查询：`谁和张三有关系`
  - 故事线：`张三 --storyline` 或 `张三的故事线`
  - 当前状态：`张三现在怎样了` 或 `张三 --status`

## 执行步骤

### 1. 解析查询意图

识别查询类型：

| 模式 | 示例 | 处理方式 |
|------|------|----------|
| 完整查询 | `张三` | 显示角色卡片 |
| 字段查询 | `张三的武器` | 提取特定字段 |
| 筛选查询 | `主角有哪些` | 按role筛选 |
| 关系查询 | `谁和张三...` | 提取关系信息 |
| 故事线 | `张三 --storyline` | 四层聚合故事线视图 |
| 当前状态 | `张三现在怎样了` | 显示 current_state 快照 |

### 2. 读取相关数据

- 读取 `{current_path}/characters/character_index.yaml` 获取角色列表
- 读取相关角色卡片文件

若为故事线模式，额外读取：
- `{current_path}/chapters/index.yaml`（章节摘要和出场记录）
- `{current_path}/plot/outline.md`（大纲中的角色计划）
- `{current_path}/characters/relation_events.yaml`（关系演进事件）

### 3. 格式化输出

根据查询类型格式化。

## 输出格式

**完整查询：**
```
$0

定位：{{role}}
年龄：{{age}}
身份：{{identity}}

性格
{{personality}}

能力
{{abilities}}

关系
{{relationships}}

详情：characters/$0.yaml
```

**字段查询：**
```
$0的{{字段}}

{{value}}
来源：characters/$0.yaml
```

**筛选查询：**
```
角色定位为「$0」的角色：

1. 张三 - 主角 - 25岁 - 剑客
2. 赵六 - 女主 - 22岁 - 灵师
```

**当前状态查询：**
```
$0 的当前状态（截至 {{as_of_chapter}}）

位置：{{location}}
情绪：{{emotional_state}}
行动目标：{{active_goal}}
身体状况：{{condition}}

已知信息：
  - {{knows_1}}
  - {{knows_2}}

未解悬念：
  - {{tension_1}}
```

**故事线查询（--storyline）：**

聚合四个层面的数据，输出该角色的完整故事纵览：

```
$0 的故事线
━━━━━━━━━━━━━━━━━━━━

一、剧情轨迹（已写章节）
{{从 index.yaml 的 summary + characters_involved 中提取该角色出场的章节}}

ch001  {{summary中与该角色相关的部分}}
ch003  {{...}}
ch005  {{...}}
  ↕ 未出场：ch002, ch004

二、大纲计划（未写章节）
{{从 outline.md 中提取该角色在未写章节中的计划}}

ch006（outline）目标：{{...}}
ch009（idea）  目标：{{...}}

三、关系演进
{{从 relation_events.yaml 中提取该角色相关的事件}}

ch001  与李四：初识，张三试探性接触
ch003  与李四：因误会降温
ch005  与王五：结盟，共同目标

四、人物弧光
{{从角色卡 arc 字段提取}}

起点（ch001）：{{state}}  [性格展示]
转折（ch005）：{{state}}  [道德抉择]
  → 下一个弧光节点预期：{{...}}

五、当前状态快照（截至 {{as_of_chapter}}）
位置：{{location}}
情绪：{{emotional_state}}
目标：{{active_goal}}
已知：{{knows}}
悬念：{{pending_tensions}}

━━━━━━━━━━━━━━━━━━━━
出场章节：{{total}}章 / 全书 {{all_chapters}}章
叙事功能：{{narrative_function}}

下一步：
   /plot-query $0的剧情线       只看大纲计划
   /relationship-evolution $0   只看关系演进
   /character-edit $0           补充角色信息
```

## 注意事项

- 支持模糊匹配
- 信息缺失时提示补充
- 可跨角色关联查询
- 故事线模式下，如果章节没有 `summary`（尚未写入），显示 `goal` 代替并标注"（大纲目标，尚未写作）"
- 故事线模式下，如果角色没有 `current_state`，提示运行 `/chapter-update` 补充
- 当前状态查询（`--status`）直接读 `current_state` 块，不需要扫描章节正文
