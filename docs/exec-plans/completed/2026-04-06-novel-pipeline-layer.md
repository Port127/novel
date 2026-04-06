# Novel Pipeline Layer

## Goal

为现有原子 skill 增加一层按场景编排的 `pipeline-*` 预设，覆盖大纲启动、大纲补强、章节开工、草稿打磨、连续性闸口、合规闸口，并补齐 `plot-review` 与 `worldbuilding-review` 两个缺口能力。

## Delivered

- 新增产品规格：`docs/product-specs/novel-pipeline.md`
- 新增 gap-review skill：`plot-review`、`worldbuilding-review`
- 新增 6 个 pipeline 预设：
  - `pipeline-outline-bootstrap`
  - `pipeline-outline-polish`
  - `pipeline-chapter-kickoff`
  - `pipeline-draft-polish`
  - `pipeline-continuity-gate`
  - `pipeline-compliance-gate`
- 同步更新入口文档：`README.md`、`README-AUTHOR.md`、`docs/SPEC.md`、`docs/index.md`、`docs/product-specs/index.md`
- 刷新质量记录：`docs/QUALITY_SCORE.md`

## Verification

- 已检查新增与修改文件，未发现 linter 错误
- 已确认 `pipeline-*`、`plot-review`、`worldbuilding-review` 在技能目录、README、SPEC、产品规格中都有对应入口
- pipeline v1 不依赖本仓库未实现的 `material-*`、`tag-*` 作为必经步骤

## Notes

- v1 采用 `CurrentState / Risks / NextTasks / RecommendedCommands` 作为统一输出契约
- `创建任务` 暂以轻量 `NextTasks` 表达，未引入持久化任务系统
