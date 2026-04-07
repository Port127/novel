---
name: novel-kpi
description: 计算小说项目核心KPI，输出产能与风险治理指标
when_to_use: 用户希望量化项目健康度，如连续更新率、完稿率、返工率和风险消解率
argument-hint: "[范围]"
arguments: range
---

# 任务

计算项目关键指标并输出简报。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取以下数据（存在则读取）：
   - `{current_path}/chapters/index.yaml`
   - `{current_path}/compliance/risk_report.yaml`
   - `{current_path}/quality/ai_trace_report.yaml`
   - `{current_path}/characters/relation_events.yaml`

## 输入参数

- `$0` (range): 时间或章节范围，如 `最近30天`、`ch001-ch050`

## 执行步骤

### 1. 产能KPI

- 连续更新率：有新增/推进记录的天数占比
- 完稿率：`final|published` 章节占比
- 返工率：进入 `revise` 的章节占比

### 2. 风险KPI

- 借鉴风险消解率：高风险章节中已修复比例
- AI痕迹消解率：AI高风险章节中已改写比例
- 关系冲突修复率：关系跳变问题中已补桥接比例

### 3. 输出结论

给出 `健康/可控/预警` 三级状态，并列出最优先动作。

## 输出格式

```
📈 项目KPI：{{project_name}}（$0）

## 产能指标
- 连续更新率：{{streak_rate}}%
- 完稿率：{{completion_rate}}%
- 返工率：{{rework_rate}}%

## 风险治理指标
- 借鉴风险消解率：{{inspiration_resolve}}%
- AI痕迹消解率：{{ai_resolve}}%
- 关系冲突修复率：{{relation_resolve}}%

## 结论
- 项目状态：{{status}}
- 最优先动作：{{next_action}}
```

## 数据可计算性说明

以下指标依赖的数据源和可靠度：

| 指标 | 数据源 | 可靠度 |
|------|--------|--------|
| 完稿率 | `chapters/index.yaml` 中 `status: final\|published` 占比 | 高 |
| 返工率 | `chapters/index.yaml` 中进入 `revise` 的章节占比 | 高 |
| 连续更新率 | 各章节 `updated` 字段的日期分布 | 中——依赖用户及时推进状态 |
| 借鉴风险消解率 | `compliance/risk_report.yaml` 中高风险已修复比例 | 中——依赖用户修复后更新报告 |
| AI 痕迹消解率 | `quality/ai_trace_report.yaml` 中高风险已改写比例 | 中 |
| 关系冲突修复率 | 需手动追踪，当前无自动数据源 | 低——标注为"预估" |

当数据不足以计算某项指标时，输出"数据缺失：{{原因}}"而非硬算一个数字。

## 注意事项

- 明确指标口径，避免同名不同义
- 指标不足时给出"数据缺失提示"而非硬算
- 缺失提示文案统一遵循 [reference-reporting.md](../reference-reporting.md)

## 参考示例

- 见 [examples.md](examples.md)
