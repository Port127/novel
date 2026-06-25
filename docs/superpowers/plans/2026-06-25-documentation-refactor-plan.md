# 文档全量更新实施计划 (Writing-Plans)

## 目标
执行对项目中残留的过时 CLI 调用的全量替换，使得全部 Markdown 文档反映真实的 V3 代码架构 (`novel` 命令行入口)。基于 TDD 思想，我们将通过执行全局字符串扫描来作为最终的“测试用例”。

## 替换映射规则 (Mapping Rules)

以下是具体的文字级替换规则（用于执行阶段）：

| 旧字符串 (Bad) | 新字符串 (Good) |
| --- | --- |
| `python scripts/project.py create` | `novel new` |
| `python scripts/project.py list` | `novel list` |
| `python scripts/project.py show` | `novel show` |
| `python scripts/project.py delete` | `novel delete` |
| `python scripts/utils/completeness_check.py` | `novel check` (如果在 CLI 里有的话，或保持内部调用说明，但当前 CLI 并没有 check，应修改为直接用 `novel generate` 让它自动阻断) |
| `python scripts/generate.py world` | `novel generate world` |
| `python scripts/generate.py character` | `novel generate character` |
| `python scripts/generate.py outline` | `novel generate outline` |
| `python scripts/generate.py chapter` | `novel generate chapter` |
| `python scripts/write.py new` | `novel write new` |
| `python scripts/write.py continue` | `novel write continue` |
| `python scripts/write.py revise` | `novel write revise` |
| `python scripts/stats.py` | `novel stats` (若无则说明尚待开发) |
| `python scripts/export.py` | `novel export` (若无则说明尚待开发) |

## 任务拆解

### 任务 1: 核心门面文档更新
- **文件**: `README.md`, `CLAUDE.md`
- **动作**: 结合上表的映射规则，进行逐行替换；更新“目录结构”部分，突出 `src/novel/` 并将 `scripts/` 的描述淡化。

### 任务 2: 规范与记录文档更新
- **文件**: `docs/PIPELINE.md`, `docs/REQUIREMENTS.md`
- **动作**: 修正表格中的命令示例。
- **文件**: `docs/analysis_report.md`
- **动作**: 在文件首行插入 `> [!WARNING]\n> **历史归档警告**：此文档为 V3 引擎重构前生成的分析报告，报告中指出的“缺少生成脚本”问题已在随后的重构中解决。本文档现已失效，仅作历史参考。`

### 3. 任务 3: AI 技能书翻新 (SKILLS)
- **文件群**: `.claude/skills/**/*.md`
- **动作**: 将所有引导大模型使用的 `python scripts/...` 指令替换为最新的终端命令。大模型将依据这些更新后的文件正确工作。

## 验收测试 (Validation)
**执行手段**:
运行严格的 `grep_search`，搜索 `python scripts/`。
**期望结果**:
在所有的 `.md` 格式文件里，该搜索结果的匹配数必须为 **0**。这即是我们文档重构的“绿灯通过 (Green)”。
