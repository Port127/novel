---
name: anti-ai-check
description: 检测章节中的AI痕迹并输出量化评分
when_to_use: 用户想降低AI感，或在发布前做文本质检
argument-hint: "[章节ID]"
arguments: chapter_id
---

# 任务

对指定章节进行去 AI 感检查。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 按 [章节自动推断协议](_protocols/chapter-auto-inference.md) 确定目标章节
3. 读取 `{current_path}/chapters/$0.md`
4. 读取 `shared/styles/anti_ai_rules.yaml`（若存在）

## 执行步骤

### 1. 指标分析

- 句式重复率
- 高频套话密度
- 机械并列结构占比
- 对话同质化程度
- 空泛情绪词占比

### 2. 评分

给出总分（0-100），并按严重度列出问题段落。

### 3. 修复建议

针对每类问题给出“保留剧情不变”的改写建议。

### 4. 写入检测报告

将本次检测结果追加到 `{current_path}/quality/ai_trace_report.yaml`：

```yaml
reports:
  - chapter: $0
    score: {{score}}
    level: {{level}}
    issues: [...]
    date: {{今天日期}}
```

## 输出格式

```
🧪 去AI感检测：$0

总分：{{score}}/100
等级：{{level}}

高风险项：
- 句式重复率偏高（{{value}}%）
- 套话密度偏高（{{value}}%）

修复建议：
1. ...
2. ...
```

## 注意事项

- 不改变核心剧情事实
- 建议优先修复高风险片段
