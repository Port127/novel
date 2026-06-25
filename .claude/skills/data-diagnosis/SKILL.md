---
name: data-diagnosis
description: 数据诊断。导入平台数据，分析追读率/互动率，定位问题章节。
---

# 数据诊断

导入平台后台数据，分析追读率、互动率，定位问题章节并给出改进建议。

---

## 工作流程

### 1. 导入数据

用户从平台后台导出数据 CSV，提供文件路径。

### 2. 解析数据

```python
from novel.core.skills.analyze_stats import AnalyzeStatsSkill
skill = AnalyzeStatsSkill()
chapter_stats = skill.parse_stats_csv(csv_data)
```

### 3. 综合分析

```python
overall = skill.calculate_overall_stats(chapter_stats)
retention_issues = skill.detect_retention_drop(chapter_stats)
engagement_issues = skill.detect_low_engagement(chapter_stats)
verdict = skill.evaluate(chapter_stats)
```

### 4. 展示诊断报告

输出：

```
== 数据诊断报告 ==

总体数据：
- 总章数: 50
- 平均追读率: 65%
- 平均完读率: 72%

问题章节：
- 第12章：追读率下降 25%（从 70% 降至 52%）
- 第23章：互动率偏低（评论 3，平均 25）

改进建议：
- 第12章节奏拖沓，建议精简
- 第23章缺少冲突，建议增加打脸情节
```

### 5. 输出

生成 `data_diagnosis_report.yaml`。

---

## 输出文件

- `data_diagnosis_report.yaml`

## 参考

- 引擎: `src/novel/core/skills/analyze_stats.py`
