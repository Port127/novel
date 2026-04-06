# 运营类指标缺失提示规范

适用于：

- `/project-weekly-report`
- `/novel-kpi`
- 以及后续所有运营/复盘类 skill

## 目标

当数据不足时，统一输出风格，避免“硬算、误导、口径不一”。

## 输出原则

1. 缺失即标记 `N/A`，不使用 0 代替
2. 明确缺失来源文件和字段
3. 给出最小补录动作（1-2 条）
4. 区分“无法计算”和“可估算”

## 标准提示模板

### 单指标缺失

```markdown
⚠️ 指标暂不可计算：{{metric_name}} = N/A
原因：缺少 {{source_file}} 中的 {{missing_field}}
建议补录：
1. {{action_1}}
2. {{action_2}}
```

### 多指标缺失（汇总）

```markdown
⚠️ 以下指标因数据缺失暂不可计算：
- {{metric_1}}（缺少 {{field_1}}）
- {{metric_2}}（缺少 {{field_2}}）

建议先完成：
1. {{priority_action_1}}
2. {{priority_action_2}}
```

### 可估算但不精确

```markdown
ℹ️ {{metric_name}} 为估算值：{{estimated_value}}
估算依据：{{basis}}
置信度：{{confidence}}
建议：补齐 {{source_file}} 后重新计算精确值
```

## 常见缺失映射

- `chapters/index.yaml` 缺失：连续更新率、完稿率、返工率不可计算
- `compliance/risk_report.yaml` 缺失：借鉴风险消解率不可计算
- `quality/ai_trace_report.yaml` 缺失：AI痕迹消解率不可计算
- `characters/relation_events.yaml` 缺失：关系冲突修复率不可计算

## 口径一致性提醒

- 所有百分比保留整数或 1 位小数，项目内保持一致
- 周报与 KPI 报告使用同一分母口径
