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
| 世界观设定 | 力量体系、势力、地点 | `/create-novel` + `/nm` |
| 人物设计 | 主角、反派、配角档案 | `/generate-character` |
| 大纲规划 | 幕 → 序列 → 节拍结构 | `/generate-outline` |
| 章节规划 | 大纲转章节摘要 + 张力曲线 | `/generate-chapter` |
| 正文写作 | 生成、续写、改写 | `/write-chapter` |
| 素材检索 | 参考同类小说 | `/nm` |
| 导出 | TXT/Markdown/EPUB | `/export-novel` |

## 使用方式

### 方式一：Skills 交互式创作（推荐）

直接和 Agent 对话，交互式完成创作：

```
"帮我创建一部修仙小说"
→ /create-novel 引导流程 → 世界观 → 人物 → 大纲 → 章节

"帮我设计主角"
→ /generate-character → 逐步询问 → 生成人物档案

"写第1章"
→ /write-chapter → 确认摘要 → 生成正文 → 调整
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
阶段1：世界观设定    → 完善度 ≥ 80%
    ↓
阶段2：人物设定      → 完善度 ≥ 70%
    ↓
阶段3：大纲设定      → 完善度 ≥ 85%
    ↓
阶段4：章节规划      → 目标章节 = 100%
    ↓
阶段5：正文写作      → 完成
```

**强制顺序**：每个阶段有完善度检查，未达标不能进入下一阶段。

## 目录结构

```
novel/
├── novels/                    # 写作项目目录
├── src/novel/                 # 核心引擎及 CLI
│   ├── project.py             # 项目管理
│   ├── stats.py               # 统计查看
│   └── export.py              # 导出
├── data/schemas/              # YAML Schema 定义
└── .agents/skills/            # Agent Skills
```

## 文档导航

- **[用户手册](docs/USER_MANUAL.md)** — 详细使用指南
- **[需求文档](docs/REQUIREMENTS.md)** — 核心需求与设计原则
- **[Pipeline 流程](docs/PIPELINE.md)** — 创作流程详细说明
- **[Schema 定义](data/schemas/)** — YAML 文件字段规范

## 与 novel-material 协作

通过 `/nm` skill 检索素材库：

```
用户写作 → nm 查分类 → nm 检索参考 → 糅合写作
```

入库阈值：某类型素材少于 **50 本** 时建议入库。
