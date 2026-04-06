# AGENTS

本仓库使用轻量级 harness 进行 Agent 驱动开发。

## 项目标识
- 名称：AI小说写作系统
- 类型：Skill Package
- 用途：面向长篇连载与多项目管理的写作工作台。

## 如何使用本 harness
1. 先阅读本文件作为导航入口。
2. 阅读 `ARCHITECTURE.md` 了解边界与契约。
3. 打开 `docs/index.md` 获取完整文档地图。
4. 在 `docs/` 中选择一个入口：
   - 设计上下文：`docs/DESIGN.md`
   - 计划与执行状态：`docs/PLANS.md`
   - 可靠性/安全基线：`docs/RELIABILITY.md`、`docs/SECURITY.md`
   - 质量评分策略：`docs/QUALITY_SCORE.md`
5. 实现工作请在 `docs/exec-plans/active/` 新增/更新文件，完成后移至 `completed/`。
6. Eval 工作请从 `docs/evals/index.md` 开始。

## 领域地图
- 项目运营：项目状态、KPI、周报
- 章节流水线：创建、更新、看板、审查
- 角色与关系：关系图谱与演进日志
- 合规与风险：借鉴日志、风险检查与报告
- 写作质量：去 AI 痕迹、改写、对白一致性

## 真实来源（现有文档）
- 产品与命令概览：`README.md`、`README-AUTHOR.md`、`README-EDITOR.md`
- 当前系统规范：`docs/SPEC.md`
- 业务扩展 backlog：`docs/BUSINESS-EXPANSION.md`
- 命令清单与结构：`README.md` 与 `docs/index.md`

## Harness 结构
- `AGENTS.md`：入口地图（本文件）
- `ARCHITECTURE.md`：拓扑图 + 公开契约
- `docs/DESIGN.md`：稳定设计上下文
- `docs/PLANS.md`：计划索引与执行链接
- `docs/QUALITY_SCORE.md`：质量评分卡与基线日志
- `docs/RELIABILITY.md`：可靠性目标与检查
- `docs/SECURITY.md`：安全模型与控制措施
- `docs/design-docs/`：核心信念与深度设计笔记
- `docs/exec-plans/`：进行中/已完成执行计划 + 技术债
- `docs/product-specs/`：产品规格索引
- `docs/evals/`：Eval 策略与套件

## 工作流程协议
使用以下顺序：发现 -> 预览 -> 确认 -> 执行 -> 验证 -> 报告。

## 护栏
- 保持本文件为地图，而非百科全书。
- 链接指向细节，而非重复内容。
- 未有可复现来源前，不得声称指标。
- 优先使用确定性检查，再做主观判断。