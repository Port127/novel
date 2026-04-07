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
- 世界观与设定集管理
- 素材检索与参考（通过 `../novel-material` 素材库）
- 合规与借鉴可追溯性
- 写作风格与去 AI 质量控制
- 流程编排（8 个 pipeline 预设）

## 素材库集成
独立素材库 `../novel-material/` 提供场景、人物、技法的多维检索。集成方式：
- 项目配置：`projects/{name}/.novel/materials.yaml` 注册素材库路径和引用
- 桥接 Skill：`/material-search` 在本 workspace 内直接调用素材库检索脚本
- 写作增强：`/chapter-draft` 和 `/plot-suggest` 内置可选检索步骤
- 合规链路：`/inspiration-log` → `/inspiration-check` → `/inspiration-report` 通过素材 ID 关联
- 降级策略：素材库不存在时全部跳过，不阻断主流程

## 公开契约
- 命令契约：
  - 完整命令参考在 `docs/SPEC.md`（Skill清单）。
  - 场景使用指南在 `docs/USAGE-GUIDE.md`。
  - Skill 具体行为定义在各 `SKILL.md` 中。
- 状态契约：
  - 当前项目指针：`.current.yaml`
  - 项目列表：`.projects.yaml`
  - 项目模板基线：`templates/project/`
- 报告契约：
  - KPI/报告命令必须使用显式来源文件，缺失数据返回 `N/A`。

## 变更边界
- 更新命令行为：编辑 `.claude/skills/` 下的目标 skill 文件。
- 更新数据模型：通过 `templates/project/` 下的模板文件。
- 更新操作指引：在 `docs/` 中更新。
- 避免将业务逻辑耦合进 harness 文档；保持链接与契约稳定。
