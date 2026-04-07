---
name: plot-query
description: 查询大纲信息，支持按章节、伏笔、角色、冲突等维度检索
when_to_use: 用户想查看大纲中某章的计划、查找未回收伏笔、检索某角色的剧情线、或了解某个冲突的前因后果
argument-hint: "[查询内容]"
arguments: query
---

# 任务

查询大纲信息，按用户需求维度返回结构化结果。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/plot/outline.md`
3. 若存在，读取 `{current_path}/plot/outline.yaml`
4. 若存在，读取 `{current_path}/plot/plot_index.yaml`
5. 若存在，读取 `{current_path}/chapters/index.yaml`（用于对照章节实际状态）

## 输入参数

- `$0+` (query): 查询内容，支持多种形式：
  - 章节查询：`第5章` / `ch005`
  - 伏笔查询：`伏笔` / `未回收的伏笔` / `第3章埋的伏笔`
  - 角色查询：`张三的剧情线` / `张三出现在哪些章节`
  - 冲突查询：`主线冲突` / `第二幕的冲突`
  - 结构查询：`中点是什么` / `高潮在哪`
  - 范围查询：`第1-5章的概要`
  - 钩子查询：`各章结尾钩子` / `ch003的钩子`

## 执行步骤

### 1. 解析查询意图

识别查询类型：

| 模式 | 示例 | 数据源 |
|------|------|--------|
| 单章详情 | `第5章` | outline.md + outline.yaml + index.yaml |
| 范围概要 | `第1-5章概要` | outline.md |
| 伏笔清单 | `未回收伏笔` | outline.yaml → foreshadowing |
| 角色剧情线 | `张三的线` | outline.md + plot_index.yaml |
| 冲突查询 | `主线冲突` | outline.yaml → structure |
| 节奏分布 | `节奏曲线` | outline.yaml → pacing_curve |
| 钩子清单 | `各章钩子` | outline.md 中各章的转折/钩子字段 |

### 2. 提取并格式化数据

根据查询类型从对应数据源提取信息。

若查询涉及章节，同时标注该章的当前写作状态（idea / outline / draft / ...）。

### 3. 交叉标注

- 伏笔查询时，标注每条伏笔的埋设章节和回收章节（若已回收）
- 角色查询时，标注该角色在各章的功能（推动 / 阻碍 / 揭示 / 转变）
- 范围查询时，标注哪些章节已写、哪些还是计划

## 输出格式

**单章详情：**
```
📖 大纲：第5章

🎯 目标：{{goal}}
📍 时间：{{time}}
📍 地点：{{location}}
👥 人物：{{characters}}
⚔️ 事件：{{event}}
💥 冲突：{{conflict}}
🪝 钩子：{{hook}}
📌 状态：{{chapter_status}}

🔗 伏笔：
  - [埋] {{planted_hook}}
  - [收] {{revealed_hook}}
```

**伏笔清单：**
```
🪝 伏笔状态

已回收（{{count}}）：
  - {{hook}} — 埋于 {{plant_ch}}，收于 {{reveal_ch}}

未回收（{{count}}）：
  - {{hook}} — 埋于 {{plant_ch}}，预计 {{expected_reveal}}
  - {{hook}} — 埋于 {{plant_ch}}，⚠️ 尚未安排回收

💡 建议：/plot-edit {{node}} 安排伏笔回收
```

**角色剧情线：**
```
📈 {{character}} 的剧情线

ch001  开场引入，展示日常
ch003  卷入冲突，被迫选择
ch007  中点转折，发现真相
ch012  危机时刻，付出代价
...

出场章节：{{total}} 章
主要功能：{{narrative_function}}
```

## 注意事项

- 只读操作，不修改任何文件
- 查询结果来自 outline 和 index 数据，不扫描正文
- 信息缺失时明确标注"大纲中未记录"，不编造
- 对于复杂查询（如"这个故事的主题是什么"），基于 outline.yaml 的 premise/theme 回答
