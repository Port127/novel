# 编辑/主编手册（进度与风险视角）

这份手册面向编辑、主编、项目负责人。  
目标不是“写文”，而是“控节奏、控质量、控风险”。

---

## 先看 6 个核心命令

```bash
/novel-list
/novel-switch 项目名
/chapter-board
/consistency-check
/project-weekly-report 最近7天 --view manager
/novel-kpi 最近30天
```

---

## 三个高频管理场景

### 场景 A：周会前快速看盘

```bash
/novel-switch 仙途
/chapter-board
/project-weekly-report 最近7天 --view manager
```

关注三件事：

- 章节推进是否卡在 `draft/revise`
- 高风险章节是否在下降
- 下周重点动作是否明确到章节

---

### 场景 B：发文前风险闸口

```bash
/consistency-check
/inspiration-report ch001-ch020
/novel-kpi ch001-ch020
```

放行建议（可自定义）：

- 完稿率达到目标线
- 借鉴高风险章节已修复
- AI 痕迹高风险数量可控

如果想一次性跑完连续性检查与合规闸口，可以用：

- `/pipeline-continuity-gate [range]`：汇总关系/时间线/一致性修复清单
- `/pipeline-compliance-gate [range]`：发布前借鉴留痕与风险汇总

---

### 场景 C：多书并行排产

```bash
/novel-list
/novel-switch 项目A
/project-weekly-report 最近7天 --view manager
/novel-switch 项目B
/project-weekly-report 最近7天 --view manager
```

用于比较不同项目的：

- 产能密度（章节推进速度）
- 风险密度（高风险占比）
- 资源利用（素材复用是否过于集中）

---

## 编辑视角 KPI 看什么

- 连续更新率：判断团队执行稳定性
- 完稿率：判断产出闭环能力
- 返工率：判断初稿质量与流程设计
- 借鉴风险消解率：判断合规治理能力
- AI痕迹消解率：判断文本可读性治理能力
- 钩子健康度：逾期/未回收占比，`/hook-query --overdue` 快速查看
- 设定有效期覆盖：过期设定是否已被新版接替，`/consistency-check` 会报告

---

## 推荐管理节奏

- 每日：看一次 `chapter-board`
- 每周：`project-weekly-report --view manager`
- 每双周：`novel-kpi` 对比趋势
- 每里程碑：`consistency-check + inspiration-report`

---

## 缺失数据处理原则

遇到 `N/A` 时，不要拍脑袋补 0。  
按统一口径补录，参考：

- `.claude/skills/reference-reporting.md`

---

## 与作者协作建议

- 给作者只下“本周 1-3 条优先动作”，不要一次给太多整改项
- 风险项先修高优先级链路（关系跳变 > 借鉴高风险 > 风格微调）
- 用章节ID沟通，避免“这章/那章”的口头歧义
