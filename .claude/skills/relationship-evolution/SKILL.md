---
name: relationship-evolution
description: 查看角色关系的时间演进轨迹
when_to_use: 用户想分析某角色或某角色对的关系变化历程
argument-hint: "[角色名] [--with 另一个角色]"
arguments: character
---

# 任务

基于关系事件日志输出关系演进视图。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/characters/relation_events.yaml`

## 输入参数

- `$0` (character): 目标角色
- `--with`: 可选，指定另一个角色

## 执行步骤

### 1. 过滤事件

筛选与目标角色相关的关系事件，若有 `--with` 则筛选角色对。

### 2. 时间排序

按章节顺序输出关系变化轨迹，标注关系类型与强度变化。

### 3. 给出写作建议

识别关系突变点，提示是否需要补桥接剧情。

## 输出格式

```
📈 关系演进：{{target}}

ch001  张三 ↔ 李四  师兄弟(2)  初识互助
ch006  张三 ↔ 李四  师兄弟(4)  共战后信任增强
ch011  张三 ↔ 李四  裂痕(1)    误会导致分歧

💡 建议：
- ch006 到 ch011 建议补一段导火索
```

## 注意事项

- 章节排序以章节ID或时间线为准
- 输出应区分“事实变化”和“建议推断”
