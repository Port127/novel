# 诊断报告模板

> **用途**：Phase 5 生成诊断报告时对照使用。

---

## 报告结构

```yaml
data_diagnosis_report:
  # 基础信息
  analysis_date: 2026-06-29
  platform: 起点
  novel_title: "我的小说"
  total_chapters: 50
  data_period: "2026-01-01 至 2026-06-29"

  # 总体指标
  overall_metrics:
    avg_retention_rate: 65%
    avg_completion_rate: 72%
    avg_engagement_rate: 3.5%
    total_reads: 125000
    total_comments: 4375

  # 趋势分析
  trend_analysis:
    retention_trend: 稳定
    completion_trend: 轻微下滑
    engagement_trend: 稳定

  # 问题章节
  problem_chapters:
    - chapter: 12
      title: "第12章 标题"
      issues:
        - type: 追读率骤降
          severity: P0
          metric: retention_rate
          value: 52%
          previous: 70%
          drop: 25%
      possible_causes:
        - pattern: 节奏拖沓
          description: 本章大量环境描写，剧情推进缓慢
      suggestions:
        - 删减非必要环境描写
        - 增加剧情冲突点
        - 控制章节字数在 3000-4000

    - chapter: 23
      title: "第23章 标题"
      issues:
        - type: 完读率偏低
          severity: P1
          metric: completion_rate
          value: 48%
          threshold: 60%
      possible_causes:
        - pattern: 章节过长
          description: 本章字数 5800，超出建议范围
      suggestions:
        - 拆分为两章
        - 精简对话内容

  # 优秀章节（可参考）
  excellent_chapters:
    - chapter: 15
      title: "第15章 标题"
      metrics:
        retention_rate: 78%
        completion_rate: 85%
        engagement_rate: 6%
      success_factors:
        - 打脸爽点设计到位
        - 章末悬念强

  # 改进建议汇总
  improvement_suggestions:
    immediate:
      - 修改第 12 章，精简节奏
      - 拆分第 23 章
    short_term:
      - 检查后续章节的节奏设计
      - 增加每章的冲突密度
    long_term:
      - 建立章节质量检查机制
      - 定期分析数据趋势

  # 风险提示
  risks:
    - type: 追读率持续下滑
      severity: 中
      description: 近 10 章追读率呈下滑趋势
      mitigation: 加快剧情节奏，增加爽点密度
```

---

## 报告展示格式

### 文本摘要

```
== 数据诊断报告 ==

【总体数据】
- 总章数: 50
- 平均追读率: 65%
- 平均完读率: 72%
- 平均互动率: 3.5%

【问题章节】
P0 - 第12章: 追读率骤降 25%（70% → 52%）
  原因: 节奏拖沓，大量环境描写
  建议: 删减描写，增加冲突

P1 - 第23章: 完读率偏低（48% < 60%）
  原因: 章节过长（5800字）
  建议: 拆分为两章

【优秀章节】
第15章: 追读率 78%，打脸设计到位

【趋势】
追读率: 稳定
完读率: 轻微下滑（需注意）

【建议】
立即处理: 修改第12章、拆分第23章
短期改进: 检查后续章节节奏
```

---

## 质量检查

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 结构完整 | 所有必需字段已填写 |
| 2 | 数据准确 | 指标计算正确 |
| 3 | 建议具体 | 每条建议可操作 |
| 4 | 优先级清晰 | P0/P1 优先处理 |
