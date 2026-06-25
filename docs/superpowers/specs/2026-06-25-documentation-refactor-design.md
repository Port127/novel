# V3 核心引擎：全项目文档同步重构方案 (Documentation Refactor Specs)

## 1. 背景问题
昨日项目核心代码已重构并迁移至 `src/novel/` 目录下。然而，目前不仅是 `docs/` 下的文档，就连指导大模型自身行为的 `CLAUDE.md` 和 `.claude/skills/` 中的全部技能说明，依然指向已被废弃的 `scripts/generate.py` 和 `scripts/project.py` 等脚本。这会导致严重的 AI 幻觉和运行错误。

## 2. 目标
进行无死角的“大换血”，把所有涉及到旧版 CLI 的 markdown 文件全部替换为当前 V3 引擎（`src/novel/cli/main.py` 或统一的 `novel` 命令）的真实样貌。

## 3. 具体修改项 (Proposed Changes)

### 3.1 核心指南库 (README & CLAUDE.md)
- **`README.md` & `CLAUDE.md`**：
  - 彻底替换所有的 CLI 使用示例（`project.py create` -> `novel new`, `generate.py` -> `novel generate` 等）。
  - 更新项目目录树展示（移除过时的 `scripts/` 结构，补充 `src/novel/` 架构说明）。

### 3.2 技能指导库 (`.claude/skills/**/*.md`)
这部分直接决定了交互式生成的成败，必须把里面所有的命令行调用全部翻新：
- `create-novel/SKILL.md`: 替换完整性检查和生成的命令。
- `generate-character/SKILL.md`, `generate-outline/SKILL.md`: 替换获取和生成设定的指令。
- `show-project/SKILL.md`: 替换展示项目的指令。
- `export-novel/SKILL.md`, `revise-setting/SKILL.md`: 替换对应的旧脚本路径。

### 3.3 文档及需求库 (`docs/`)
- **`docs/PIPELINE.md`**：同步 Pipeline 流程中每一阶段触发的具体命令。
- **`docs/REQUIREMENTS.md`**：更新第四章和第五章的命令表。
- **历史债务**：将 `docs/analysis_report.md` 转移或在头部添加强烈的“过期警示”标签。

## 4. 交付标准
全局检索 `python scripts/` 应当不再出现旧版的业务脚本调用，整个项目拥有唯一真实的终端命令规范。
