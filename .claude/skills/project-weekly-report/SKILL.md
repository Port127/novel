---
name: project-weekly-report
description: 生成项目周报，支持管理者版与作者版双视角输出
when_to_use: 用户想复盘一周写作进展，并按不同读者视角查看周报
argument-hint: "[范围] [--view manager|author|both]"
arguments: range
---

# 任务

按范围生成可复用的项目周报。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取以下数据源（存在则读取）：
   - `{current_path}/chapters/index.yaml`
   - `{current_path}/characters/relation_events.yaml`
   - `{current_path}/compliance/inspiration_log.yaml`
   - `{current_path}/compliance/risk_report.yaml`
   - `{current_path}/quality/ai_trace_report.yaml`

## 输入参数

- `$0` (range): 时间范围或章节范围，如 `最近7天`、`ch001-ch010`
- `--view`: 输出视角，`manager|author|both`，默认 `both`

## 执行步骤

### 1. 产能统计

- 新增章节数
- 状态推进数（draft->revise->final）
- 字数完成率

### 2. 风险统计

- 关系跳变问题数
- 借鉴高风险章节数
- AI痕迹高风险章节数

### 3. 素材利用率

- 借鉴登记覆盖率
- 单素材复用占比
- 剧情/人物索引命中率（若可得）

### 4. 下周行动建议

按“高优先级/中优先级”给出明确动作。

## 输出格式

### 管理者版（manager）

```
📆 项目周报（管理者版）：{{project_name}}（$0）

## 产能
- 新增章节：{{new_chapters}}
- 状态推进：{{progress_count}}
- 字数完成率：{{word_completion}}%

## 风险
- 关系演进风险：{{rel_risk}}
- 借鉴高风险：{{insp_risk}}
- AI痕迹高风险：{{ai_risk}}

## 素材利用
- 借鉴登记覆盖率：{{coverage}}%
- 素材复用集中度：{{reuse_ratio}}%

## 下周重点
1. ...
2. ...
3. ...
```

### 作者版（author）

```
🖋️ 创作周报（作者版）：{{project_name}}（$0）

## 本周写作感受
- 高效时段：{{best_time}}
- 卡点类型：{{blocker_type}}

## 本周亮点章节
- {{chapter_id}}：{{highlight_reason}}

## 待打磨章节
- {{chapter_id}}：{{problem}}

## 下周创作计划
1. 本周先完成 {{target_chapter}}
2. 先修复 {{top_risk}}
3. 保留 {{style_advantage}}，避免 {{style_risk}}
```

## 数据可计算性说明

- **新增章节数 / 状态推进数 / 字数完成率**：从 `chapters/index.yaml` 的 `updated` 和 `status` 字段计算，可靠
- **风险统计**：从 `risk_report.yaml` 和 `ai_trace_report.yaml` 计算，依赖这些报告已生成
- **高效时段 / 卡点类型**（作者版）：当前无自动数据源，基于章节推进模式推断或标注为"需要用户补充"
- **素材利用率**：依赖 `inspiration_log.yaml` 已登记，未登记则标注覆盖率为"不可计算"

当某项数据不足时，在报告中标注"数据缺失"并给出补充建议（如"运行 `/inspiration-log` 补登记"），不硬算。

## 注意事项

- 先给事实统计，再给判断结论
- 建议项尽量对应到具体章节或角色对
- `manager` 关注进度与风险，`author` 关注可执行创作动作
- 数据缺失时统一使用运营提示规范，见 [reference-reporting.md](../reference-reporting.md)

## 参考示例

- 见 [examples.md](examples.md)
