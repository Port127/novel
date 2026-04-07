# AI小说写作系统 - 设计规范 v2

> 基于 Claude Code 源码借鉴设计

---

## 核心设计原则

1. **多项目支持** - 同时管理多本小说，项目隔离
2. **小而专的Skill** - 单一职责，可组合
3. **参数化** - 支持位置参数和命名参数
4. **自动状态同步** - Hooks机制自动更新索引
5. **记忆系统** - 跨会话保持用户偏好和项目决策
6. **诊断能力** - 一键检查项目完整性
7. **场景化编排层** - 用 `pipeline-*`（当前 8 个）把高频流程收束为薄编排预设
8. **文件即输入** - 高频 skill 支持 `--from` 引用文件内容，章节类 skill 支持从当前打开文件自动推断上下文
9. **共享协议** - 跨 skill 复用的通用逻辑（如章节推断、引用提取）提取为 `_protocols/`，各 skill 引用而非重复

> 能力地图见 `README.md`，场景使用指南见 `docs/USAGE-GUIDE.md`，本文件聚焦技术规范。

---

## 目录结构

```
novel/
├── .claude/
│   ├── skills/                    # Skill定义
│   │   ├── _protocols/            # 共享协议（跨 skill 复用的逻辑）
│   │   │   ├── chapter-auto-inference.md
│   │   │   └── from-extraction.md
│   │   ├── novel-init/
│   │   │   └── SKILL.md
│   │   ├── character-add/
│   │   │   └── SKILL.md
│   │   └── ...
│   ├── memory/                    # 记忆系统
│   │   ├── MEMORY.md              # 记忆索引
│   │   ├── user/                  # 用户偏好
│   │   ├── feedback/              # 反馈记忆
│   │   ├── project/               # 项目记忆
│   │   └── reference/             # 外部引用
│   └── settings.local.json        # 项目设置（本地）
│
├── shared/                        # 共享资源
│   └── styles/                    # 风格模板
│       └── templates.yaml
│
├── projects/                      # 小说项目
│   ├── 仙途/
│   │   ├── .novel/
│   │   │   ├── meta.yaml          # 项目元信息
│   │   │   ├── state.yaml         # 项目状态（AI维护）
│   │   │   └── materials.yaml     # 素材引用（指向 novel-material）
│   │   ├── characters/
│   │   ├── compliance/
│   │   ├── plot/
│   │   ├── quality/
│   │   ├── scenes/
│   │   ├── timeline/
│   │   ├── worldbuilding/
│   │   │   └── entries/           # 设定集条目
│   │   └── chapters/
│   └── 都市情缘/
│       └── ...
│
├── templates/                     # 项目模板
│   └── project/
│       ├── .novel/
│       ├── characters/
│       ├── compliance/
│       ├── plot/
│       ├── quality/
│       ├── timeline/
│       └── worldbuilding/
│
├── .current.yaml                  # 当前工作项目
├── .projects.yaml                 # 项目列表
└── README.md                      # 项目说明与命令导航

# 素材库（独立项目）
../novel-material/
├── data/                          # 素材数据
│   ├── index.yaml                 # 素材总索引
│   ├── plot_index.yaml            # 剧情索引（跨小说剧情结构）
│   ├── character_index.yaml       # 人物索引（跨小说人物汇总）
│   ├── tags.yaml                  # 标签字典（6层19维）
│   └── novels/                    # 每部小说独立文件夹
│       └── {material_id}/
│           ├── scenes_index.yaml  # 倒排索引（标签→场景）
│           └── scenes_manifest.yaml # 场景清单
└── .claude/skills/                # 素材Skills
```

---

## Skill规范

### Frontmatter格式

```yaml
---
name: skill-name
description: 一行描述（用于skill列表）
when_to_use: 何时使用，触发条件示例
argument-hint: "[参数1] [参数2] [参数3]"
arguments: arg1 arg2 arg3          # 命名参数
allowed-tools:                     # 允许的工具
  - Read
  - Write
  - Edit
  - Glob
  - Grep
user-invocable: true               # 用户可调用
context: inline                    # inline | fork
---
```

### 参数替换

支持以下格式：

| 格式 | 说明 | 示例 |
|------|------|------|
| `$ARGUMENTS` | 全部参数字符串 | `张三 25岁 剑客` |
| `$0` `$1` `$2` | 位置参数 | `$0` = 张三 |
| `$name` | 命名参数 | 需声明 `arguments: name` |

示例：
```markdown
用户输入: /character-add 张三 25岁 剑客

Skill内容:
姓名：$0
年龄：$1
职业：$2
```

### Skill文件结构

每个skill一个目录：
```
skill-name/
├── SKILL.md           # Skill定义（必需）
├── templates/         # 模板文件（可选）
├── examples/          # 示例文件（可选）
└── prompts/           # 子prompt片段（可选）
```

### Skill内容模板

```markdown
---
name: skill-name
description: 描述
argument-hint: "[参数说明]"
arguments: arg1 arg2
---

# 任务

一句话描述任务目标。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 如果为空，提示用户先使用 `/novel-init` 或 `/novel-switch`
3. 所有路径基于 `current_path`

## 输入参数

- `$0` (arg1): 参数1说明
- `$1` (arg2): 参数2说明

## 执行步骤

### 1. 步骤名称

具体操作说明。

**成功标准**: 如何判断此步骤完成

### 2. 下一步骤

...

## 输出格式

```
✅ 操作完成

相关信息展示
```

## 注意事项

- 注意点1
- 注意点2
```

---

## Memory系统

### 四种记忆类型

| 类型 | 用途 | 示例 |
|------|------|------|
| `user` | 用户画像、写作偏好 | "用户喜欢简洁文风，讨厌废话" |
| `feedback` | 用户纠正、指导 | "不要用emoji，用户觉得不专业" |
| `project` | 项目决策、进度 | "第一章已写完，第二章卡住了" |
| `reference` | 外部资源引用 | "素材库在 ../novel-material/data/" |

### 记忆文件格式

```markdown
---
name: 记忆名称
description: 一行描述
type: user | feedback | project | reference
---

记忆内容

**Why**: 为什么记录这条
**How to apply**: 如何应用
```

### 记忆索引 (MEMORY.md)

```markdown
# Memory Index

## User
- [写作风格偏好](user/writing-style.md)

## Feedback
- [不要用emoji](feedback/no-emoji.md)

## Project
- [仙途进度](project/xiantu-progress.md)

## Reference
- [素材库位置](reference/novel-material-location.md)
```

---

## 状态管理

### .current.yaml

```yaml
current_project: 仙途
current_path: projects/仙途
last_updated: 2024-04-01
```

### projects/{name}/.novel/state.yaml

```yaml
project:
  name: 仙途
  genre: 仙侠
  created: 2024-04-01
  updated: 2024-04-01

ingestion:
  status: completed
  brief_file: ingestion_brief.md
  source_draft: ""

characters:
  - name: 张三
    role: 主角
    file: characters/张三.yaml

timeline:
  start: 第1天
  end: 第3年
  events_count: 20

plot:
  structure: 三幕式
  chapters: 15

worldbuilding:
  locations_count: 3
  rules_defined: true
  entries_count: 8
  confirmed_count: 5
  tentative_count: 3

current_focus: 第8章
```

---

## Hooks机制

自动触发机制：

| 事件 | 触发条件 | 动作 |
|------|----------|------|
| 写入角色卡片 | Write to `characters/*.yaml` | 更新 state.yaml 的 characters 列表 |
| 添加时间线 | Write to `timeline/main.yaml` | 检查时间冲突 |
| 切换项目 | `/novel-switch` | 更新 .current.yaml |

实现方式：在skill中显式调用状态更新步骤。

---

## Skill清单

### Pipeline 编排
| Skill | 功能 | 参数 |
|-------|------|------|
| `/pipeline-outline-bootstrap` | 从想法启动大纲 | $0+=premise |
| `/pipeline-outline-polish` | 补强现有大纲 | [$0+=focus] |
| `/pipeline-chapter-kickoff` | 生成可开写章节 | $0=章节ID $1+=章节目标 |
| `/pipeline-draft-polish` | 生成可修订草稿 | $0=章节ID |
| `/pipeline-setting-consolidate` | 设定整固与确认 | [$0+=整固重点] |
| `/pipeline-note-triage` | 混合笔记分拣入库 | $0=文件路径 [--quick] [--dry-run] |
| `/pipeline-continuity-gate` | 输出连续性修复清单 | [$0=范围] |
| `/pipeline-compliance-gate` | 执行发布前合规闸口 | $0=章节ID或范围 |

### 项目管理
| Skill | 功能 | 参数 |
|-------|------|------|
| `/novel-init` | 创建新项目 | $0=书名 $1=类型 |
| `/novel-switch` | 切换项目 | $0=项目名 |
| `/novel-status` | 查看状态 | - |
| `/novel-list` | 列出所有项目 | - |
| `/novel-doctor` | 诊断检查 | - |
| `/novel-edit` | 编辑项目基础信息 | $0=字段 $1+=新值 |
| `/skill-doctor` | 评估 skill 变更影响，检查一致性，同步文档 | $0=skill名称\|sync\|--full |
| `/draft-ingest` | 深度消化草稿/素材文档 | $0=草稿路径 |
| `/project-weekly-report` | 生成双视角项目周报 | $0=范围 |
| `/novel-kpi` | 计算项目核心KPI | $0=范围 |

### 角色管理
| Skill | 功能 | 参数 |
|-------|------|------|
| `/character-add` | 创建角色 | $0=姓名 $1=定位 $2=年龄... |
| `/character-edit` | 编辑角色 | $0=姓名 $1+=修改内容 |
| `/character-query` | 查询角色 | $0=查询内容 |
| `/relationship-add` | 建立关系 | $0=角色1 $1=角色2 $2=关系 |
| `/relationship-map` | 关系图谱 | [$0=角色名] |
| `/relationship-log` | 记录关系演进事件 | $0=角色1 $1=角色2 $2+=变化描述 |
| `/relationship-evolution` | 查看关系演进轨迹 | $0=角色名 |
| `/relationship-check` | 检查关系逻辑断裂 | - |

### 章节管理
| Skill | 功能 | 参数 |
|-------|------|------|
| `/chapter-create` | 创建章节与元数据 | $0=章节ID $1+=章节目标 |
| `/chapter-draft` | 基于大纲辅助生成初稿 | $0=章节ID [--style] [--focus] |
| `/chapter-update` | 更新章节状态/字段 | $0=章节ID |
| `/chapter-board` | 查看章节进度看板 | [--status=状态] |
| `/chapter-review` | 审查章节结构与节奏 | $0=章节ID |
| `/chapter-export` | 导出章节为连续文档 | $0=范围 [--format md\|txt] [--clean] |

### 剧情管理
| Skill | 功能 | 参数 |
|-------|------|------|
| `/plot-init` | 初始化大纲（默认从素材推导结构） | [$0=结构类型\|auto] |
| `/plot-add` | 添加情节 | $0=章节 $1+=内容 |
| `/plot-edit` | 编辑已有大纲节点 | $0=节点标识 $1+=修改内容 |
| `/plot-query` | 查询大纲信息（伏笔/角色线/冲突） | $0+=查询内容 |
| `/plot-review` | 审查大纲结构与节奏 | [$0+=优化重点] |
| `/plot-suggest` | 情节建议 | $0+=描述 |

### 世界观与场景
| Skill | 功能 | 参数 |
|-------|------|------|
| `/setting-add` | 创建/更新设定集条目 | $0=设定名称 [--category 类别] [--quick] [--from] |
| `/setting-edit` | 编辑已有设定条目 | $0=设定名称或ID $1+=修改内容 [--status] |
| `/scene-add` | 创建场景档案 | $0=场景名称 [--location] [--category] |
| `/worldbuilding-review` | 审查设定自洽性与剧情支撑度 | [$0+=优化重点] |

### 时间线
| Skill | 功能 | 参数 |
|-------|------|------|
| `/timeline-add` | 添加事件 | $0=时间 $1+=事件 |
| `/timeline-check` | 检查冲突 | - |
| `/timeline-view` | 查看时间线 | [$0=范围] |

### 合规管理
| Skill | 功能 | 参数 |
|-------|------|------|
| `/inspiration-log` | 登记借鉴来源 | $0=章节ID $1=素材ID(nm_xxx) $2+=借鉴说明 |
| `/inspiration-check` | 检查借鉴风险 | $0=章节ID |
| `/inspiration-report` | 汇总借鉴与风险报告 | $0=范围 |

### 素材检索与融合
| Skill | 功能 | 参数 |
|-------|------|------|
| `/material-search` | 检索参考素材（场景/人物/技法） | $0+=需求描述 |
| `/material-search apply` | 将参考场景融合到写作中 | $0=场景ID $1=模式(draft\|plot\|setting\|rhythm\|character) [$2=目标] |
| `/material-search link` | 关联素材到当前项目 | $0=素材ID |
| `/material-search unlink` | 取消素材关联 | $0=素材ID |
| `/material-search list` | 列出当前项目已关联的素材 | - |
| `/material-search available` | 列出素材库中所有可用素材 | - |

### 写作工具
| Skill | 功能 | 参数 |
|-------|------|------|
| `/style-list` | 列出风格 | - |
| `/style-create` | 创建风格 | $0=名称 $1+=特征 |
| `/rewrite` | 风格改写 | $0+=内容 |
| `/anti-ai-check` | 检测 AI 痕迹 | $0=章节ID |
| `/anti-ai-rewrite` | 去 AI 感改写 | $0=章节ID |
| `/voice-check` | 检查人物对白辨识度 | $0=角色名 [$1=章节范围] |

### 一致性
| Skill | 功能 | 参数 |
|-------|------|------|
| `/consistency-check` | 全面检查 | - |

### 共享协议
| 协议 | 用途 | 引用者 |
|------|------|--------|
| `_protocols/chapter-auto-inference.md` | 章节 ID 自动推断 | chapter-review, chapter-update, anti-ai-check, anti-ai-rewrite, voice-check, chapter-draft |
| `_protocols/from-extraction.md` | `--from` 引用提取 | character-add, plot-add, setting-add |

---

## 外部依赖

### novel-material（可选）

素材库是独立项目，位于 `../novel-material/`。以下功能依赖它：

| 功能 | 依赖程度 | 无素材库时行为 |
|------|---------|--------------|
| `/inspiration-log` | 软依赖 | 素材 ID 无法校验，提示用户确认有效性 |
| `/inspiration-check` | 软依赖 | 无法获取素材详情，仅基于登记信息评估 |
| `/inspiration-report` | 软依赖 | 仅展示素材 ID，无法展示素材名称 |
| `/material-search` | 核心依赖 | 素材库不存在时提示用户，无法检索 |
| `/chapter-draft` | 可选增强 | 起草前自动检索参考场景，素材库不存在时跳过 |
| `/plot-suggest` | 可选增强 | 生成建议时检索类似案例，素材库不存在时跳过 |

没有素材库时，合规功能可用但精度下降，创作辅助功能仅依赖项目本地数据。

素材库提供的检索入口：
- `data/index.yaml` — 素材总索引
- `data/character_index.yaml` — 跨小说人物检索（含心理深度维度）
- `data/plot_index.yaml` — 跨小说剧情结构检索
- `data/tags.yaml` — 标签字典（6层19维场景标签 + 小说级标签）

> 使用示例与场景指南见 `docs/USAGE-GUIDE.md`。