# Architecture

## 系统拓扑
本仓库是一个以 Skill 为中心的写作系统。

核心层级：
1. 命令/Skill 层：`.claude/skills/*`
2. 状态与记忆层：`.current.yaml`、`.projects.yaml`、`.claude/memory/*`
3. 项目模板/数据层：`templates/project/*`、`shared/styles/*`
4. 产品文档层：`README*.md`、`docs/*`

## 主要领域
- 项目管理与报告
- 章节生产流水线
- 角色与关系演进
- 时间线与剧情管理
- 合规与借鉴可追溯性
- 写作风格与去 AI 质量控制

## 公开契约
- 命令契约：
  - 用户命令在 `README.md`（完整清单）与 `docs/index.md`（导航）中文档化。
  - Skill 具体行为定义在各 `SKILL.md` 中。
- 状态契约：
  - 当前项目指针：`.current.yaml`
  - 项目列表：`.projects.yaml`
  - 项目模板基线：`templates/project/`
- 报告契约：
  - KPI/报告命令必须使用显式来源文件，缺失数据返回 `N/A`。

## Harness 契约
- 导航入口：`AGENTS.md`
- 计划入口：`docs/PLANS.md`
- 质量基线入口：`docs/QUALITY_SCORE.md`
- Eval 入口：`docs/evals/index.md`

## 变更边界
- 更新命令行为：编辑 `.claude/skills/` 下的目标 skill 文件。
- 更新数据模型：通过 `templates/project/` 下的模板文件。
- 更新操作指引：在 `docs/` 中更新。
- 避免将业务逻辑耦合进 harness 文档；保持链接与契约稳定。

## 验证规则
- `AGENTS.md` 保持简洁（地图优先）。
- Harness 文档中的交叉链接必须可解析。
- 质量指标需记录显式来源或标记 `TBD`。