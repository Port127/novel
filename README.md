# Novel V2

AI 辅助小说写作工具，支持交互式创作和 CLI 管理。

## 项目定位

| 项目 | 定位 | 关系 |
|------|------|------|
| **novel-material** | 素材检索库 | 上游，存储已有小说的结构化分析 |
| **novel-v2** | 写作工具 | 本项目，调用上游检索服务辅助创作 |

## 核心功能

| 功能 | 说明 | 入口 |
|------|------|------|
| 选题侦察 | 品类选择 + 选题分析 | `/scout-topic` |
| 世界观设计 | 力量体系、势力、地点 | `/worldbuilding` + `/nm` |
| 人设设计 | 主角、反派、配角档案 | `/design-character` |
| 大纲设计 | 幕 → 序列 → 节拍结构 | `/design-outline` |
| 细纲设计 | 大纲转章节节拍表 | `/design-chapters` |
| 黄金三章 | 前3章结构验证 | `/golden-chapters` |
| 付费卡点 | 最优切割点分析 | `/paywall-design` |
| 日更写作 | 生成 + 质量门禁 | `/daily-write` |
| 素材检索 | 参考同类小说 | `/nm` |
| 导出 | TXT/Markdown/EPUB | `/export-novel` |

## V4 Skill 架构

每个创作 skill 采用**自包含结构**：

```
.agents/skills/<skill-name>/
├── SKILL.md              ← Phase 化流程 + 质量门禁
├── references/           ← 领域知识文件（按需加载）
└── scripts/              ← JS 验证脚本（确定性检查）
```

**核心机制**：
- **Phase 化流程**：每个 Phase 有明确入口/出口条件，支持断点恢复
- **JS 质量门禁**：blocking/advisory 两级，blocking 必须修到 0
- **断点恢复**：`_progress.md` 记录进度，崩溃后从断点续跑
- **品类感知**：根据 `scout_report.yaml` 的 `required_elements` 动态决定检查内容

## 使用方式

### 方式一：Skills 交互式创作（推荐）

直接和 Agent 对话，交互式完成创作：

```
"帮我选个品类"
→ /scout-topic → 选择品类 → 分析市场 → 选题报告

"帮我设计世界观"
→ /worldbuilding → 逐步讨论 → 生成设定文件

"帮我设计主角"
→ /design-character → 逐步询问 → 爽感评估 → 生成人物档案

"写第1章"
→ /daily-write → 确认摘要 → 生成正文 → 质量门禁 → 定稿
```

### 方式二：CLI 命令行管理

```bash
# 创建项目
novel new "书名" --genre 修仙 --author "作者名"

# 查看项目
novel list
novel show <project_id>

# 统计和导出
novel stats <project_id>
novel export <project_id> --format txt
```

## 安装

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量（可选）
cp .env.example .env
```

## 创作流程

```
阶段0：选题侦察        → scout_report.yaml
    ↓
阶段1：世界观设定       → 完善度 ≥ 80%
    ↓
阶段2：人物设定         → 完善度 ≥ 70%
    ↓
阶段3：大纲设定         → 完善度 ≥ 85%
    ↓
阶段4：章节规划         → 目标章节 = 100%
    ↓
阶段5：黄金三章锻造     → chapter_001-003.md
    ↓
阶段6：付费卡点设计     → paywall_report.yaml
    ↓
阶段7：日更写作         → chapter_*.md
    ↓
阶段8：导出作品         → TXT/MD/EPUB
```

**强制顺序**：每个阶段有完善度检查，未达标不能进入下一阶段。

## 目录结构

```
novel/
├── novels/                    # 写作项目目录
├── src/novel/                 # 核心引擎（退化为基础设施）
├── data/schemas/              # YAML Schema 定义
├── templates/                 # 项目模板
└── .agents/skills/            # Agent Skills（V4 自包含结构）
    ├── <skill-name>/
    │   ├── SKILL.md           # Phase 化流程定义
    │   ├── references/        # 领域知识文件
    │   └── scripts/           # JS 验证脚本
    └── _shared/scripts/       # 共享脚本
```

## 文档导航

- **[用户手册](docs/USER_MANUAL.md)** — 详细使用指南
- **[需求文档](docs/REQUIREMENTS.md)** — 核心需求与设计原则
- **[Pipeline 流程](docs/PIPELINE.md)** — 创作流程详细说明
- **[Schema 定义](data/schemas/)** — YAML 文件字段规范
- **[V4 设计规格](docs/superpowers/specs/2026-06-29-skill-upgrade-v4-design.md)** — Skill 架构设计
- **[验证报告](docs/superpowers/verification/2026-06-29-final-verification-report.md)** — V4 升级验证结果

## 与 novel-material 协作

通过 `/nm` skill 检索素材库：

```
用户写作 → nm 查分类 → nm 检索参考 → 糅合写作
```

入库阈值：某类型素材少于 **50 本** 时建议入库。
