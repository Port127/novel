# 文档目录

本目录记录 Novel V2 当前的真实使用方式：Skill 驱动的人机协同创作工作台。

## 文档适用原则

如本文档、根目录 README 与旧 CLI/Python 代码存在冲突，以当前文档和 `.agents/skills/` 为准。`src/novel`、`scripts/` 与 `novel` CLI 是历史自动化流水线遗留，保留作参考，不再作为创作主入口维护。

## 核心文档

| 文档 | 用途 |
|------|------|
| [USER_MANUAL.md](USER_MANUAL.md) | 面向使用者，说明如何通过 Agent 和 Skills 完成选题、设定、写作、审查、导出 |
| [REQUIREMENTS.md](REQUIREMENTS.md) | 面向维护者，说明产品定位、维护边界、硬规则和成功标准 |
| [PIPELINE.md](PIPELINE.md) | 面向执行者，说明 9 个创作阶段的输入、输出、确认点、门禁和回退策略 |

## 相关资料

| 路径 | 说明 |
|------|------|
| `../README.md` | 项目总入口 |
| `../.agents/AGENTS.md` | Agent 行为规则与项目硬约束 |
| `../.agents/skills/` | 当前实际执行入口，每个 Skill 的 `SKILL.md` 是具体流程真相源 |
| `../data/schemas/` | YAML Schema 与完善度标准 |
| `../templates/` | 新书项目模板 |

## 归档

以下内容均为历史产物，**不代表当前主流程**。若与 `.agents/skills/` 或正式文档冲突，以正式文档和 Skill 文件为准。

| 路径 | 说明 |
|------|------|
| `archive/superpowers/specs/` | 历史设计规格文档（含已放弃的 CLI 自动化方向） |
| `archive/superpowers/plans/` | 历史实施计划文档 |
| `archive/superpowers/verification/` | 历史验证报告 |
| `feedback/archive/` | 历史反馈和分析报告 |
