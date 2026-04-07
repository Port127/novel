---
name: anti-ai-rewrite
description: 在保持剧情信息不变前提下，对章节进行去AI感改写
when_to_use: anti-ai-check 发现高风险后，用户希望快速降AI痕
argument-hint: "[章节ID] --level [1-3]"
arguments: chapter_id
---

# 任务

按等级执行去 AI 感改写。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 按 [章节自动推断协议](_protocols/chapter-auto-inference.md) 确定目标章节
3. 读取 `{current_path}/chapters/$0.md`
4. 建议先运行 `/anti-ai-check $0`

## 输入参数

- `$0` (chapter_id): 章节ID
- `--level`: 改写强度
  - `1` 轻改（句式和词汇）
  - `2` 中改（节奏与段落组织）
  - `3` 深改（叙事视角微调但不改事实）

## 执行步骤

### 1. 标记高风险片段

优先处理重复句式、模板化转折、空泛抒情段。

### 2. 执行分级改写

保持人物设定、事件顺序、关键信息点不变。

### 3. 输出改写版本

生成可替换段落，并附“修改原因”。

## 输出格式

```
✍️ 去AI感改写完成：$0

改写强度：L{{level}}
处理片段：{{count}}处

关键改动：
- ...
- ...
```

## 注意事项

- 不删除关键伏笔
- 改写后建议再次运行 `/anti-ai-check`
