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
7. **场景化编排层** - 用 `pipeline-*` 把高频流程收束为薄编排预设

---

## 能力地图（按业务场景）

### 立项与项目运营

- 立项与切换：`/novel-init` `/novel-switch` `/novel-list` `/novel-status`
- 项目诊断：`/novel-doctor` `/consistency-check`
- 运营复盘：`/project-weekly-report` `/novel-kpi`

### Pipeline 编排层

- 大纲启动：`/pipeline-outline-bootstrap`
- 大纲补强：`/pipeline-outline-polish`
- 开章启动：`/pipeline-chapter-kickoff`
- 草稿打磨：`/pipeline-draft-polish`
- 连续性闸口：`/pipeline-continuity-gate`
- 合规闸口：`/pipeline-compliance-gate`

### 章节生产流水线

- 创建与推进：`/chapter-create` `/chapter-update` `/chapter-board`
- 审查与打磨：`/chapter-review` `/anti-ai-check` `/anti-ai-rewrite`

### 角色与关系演进

- 角色管理：`/character-add` `/character-edit` `/character-query`
- 关系网络：`/relationship-add` `/relationship-map`
- 关系演进：`/relationship-log` `/relationship-evolution` `/relationship-check`

### 素材资产与检索（独立项目）

素材管理已独立为 `novel-material` 项目，见 `../novel-material/CLAUDE.md`

小说侧保留的借鉴登记能力：
- `/inspiration-log` 记录章节借鉴来源（素材ID引用 novel-material）
- `/inspiration-check` 检查借鉴风险（读取 novel-material 素材元数据）
- `/inspiration-report` 汇总借鉴合规报告

### 合规与风险控制

- 借鉴登记：`/inspiration-log`
- 风险检查：`/inspiration-check`
- 报告复盘：`/inspiration-report`

补充规格见：`docs/product-specs/novel-pipeline.md`

---

## 目录结构

```
novel/
├── .claude/
│   ├── skills/                    # Skill定义
│   │   ├── novel-init/
│   │   │   ├── SKILL.md
│   │   │   └── templates/
│   │   ├── character-add/
│   │   │   ├── SKILL.md
│   │   │   └── templates/
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
│   │   │   ├── state.yaml         # 项目状态
│   │   │   └── materials.yaml     # 素材引用（指向 novel-material）
│   │   ├── characters/
│   │   ├── compliance/
│   │   ├── plot/
│   │   ├── quality/
│   │   ├── timeline/
│   │   ├── worldbuilding/
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
│   ├── plot_index.yaml            # 剧情索引
│   ├── character_index.yaml       # 人物索引
│   ├── tags.yaml                  # 标签字典
│   └── chunks/                    # 分段存储
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

characters:
  - name: 张三
    role: 主角
    file: characters/张三.md

timeline:
  start: 第1天
  end: 第3年
  events_count: 20

plot:
  structure: 三幕式
  chapters: 15

current_focus: 第8章
```

---

## Hooks机制

自动触发机制：

| 事件 | 触发条件 | 动作 |
|------|----------|------|
| 写入角色卡片 | Write to `characters/*.md` | 更新 state.yaml 的 characters 列表 |
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
| `/chapter-update` | 更新章节状态/字段 | $0=章节ID |
| `/chapter-board` | 查看章节进度看板 | [--status=状态] |
| `/chapter-review` | 审查章节结构与节奏 | $0=章节ID |

### 剧情管理
| Skill | 功能 | 参数 |
|-------|------|------|
| `/plot-init` | 初始化大纲 | [$0=结构类型] |
| `/plot-add` | 添加情节 | $0=章节 $1+=内容 |
| `/plot-review` | 审查大纲结构与节奏 | [$0+=优化重点] |
| `/plot-suggest` | 情节建议 | $0+=描述 |

### 世界观
| Skill | 功能 | 参数 |
|-------|------|------|
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

---

## 使用示例

```bash
# 创建新项目
/novel-init 仙途 仙侠

# 从一句话想法启动大纲
/pipeline-outline-bootstrap 主角因宗门灭门被迫踏上复仇与求真之路

# 添加主角
/character-add 张三 主角 25岁 剑客 隐忍坚毅

# 启动新章节
/pipeline-chapter-kickoff ch001 主角在危机中被迫离开故土

# 查看项目状态
/novel-status

# 诊断检查
/novel-doctor

# 草稿完成后做一轮打磨
/pipeline-draft-polish ch001
```

---

## 业务能力补全

为贴合真实网文/长篇创作流程（章节流水线、关系演进、借鉴合规、去 AI 感、素材分段与剧情索引等），新增一份专项扩展文档：

- [业务能力补全清单](BUSINESS-EXPANSION.md)

建议按文档中的 P0/P1 优先级逐步落地新增 Skill 与数据结构。