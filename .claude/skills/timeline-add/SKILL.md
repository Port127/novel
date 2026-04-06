---
name: timeline-add
description: 添加时间线事件
when_to_use: 用户想要记录故事中的事件时间点
argument-hint: "[时间] [事件]"
arguments: time event
---

# 任务

添加时间线事件。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`

## 输入参数

- `$0` (time): 时间点，如 `第1天`、`第3天清晨`、`第10年`
- `$1+` (event): 事件描述

可选参数（通过 --指定）：
- `--chapter N` 关联章节
- `--location 地点` 发生地点
- `--characters 角色` 涉及角色

## 执行步骤

### 1. 读取时间线

读取 `{current_path}/timeline/main.yaml`。

### 2. 添加事件

```yaml
events:
  - time: "$0"
    event: "$1"
    chapter: {{如果指定}}
    location: {{如果指定}}
    characters: {{如果指定}}
```

### 3. 检查时间逻辑

验证：
- 时间顺序是否合理
- 同一时间是否有冲突事件

### 4. 更新状态

更新 `state.yaml`：
- `timeline.start/end` 范围
- `timeline.events_count` 计数

## 输出格式

```
✅ 时间线事件已添加

📅 时间：$0
📝 事件：$1

📁 已更新：timeline/main.yaml

💡 检查一致性：/timeline-check
```

## 注意事项

- 时间格式灵活
- 同一时间可有多个事件
- 自动检测顺序