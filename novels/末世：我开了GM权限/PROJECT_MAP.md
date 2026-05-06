# 《末世：我开了GM权限》项目文件结构说明

> 生成时间：2026-04-08
> 项目状态：drafting（写作中）

---

## 项目概述

| 属性 | 值 |
|------|-----|
| 项目ID | proj_20260408_gm01 |
| 类型 | 都市异能 / 末世生存 / 规则博弈 |
| 主角 | 陈默 |
| 目标章节 | 50章（第一阶段完整故事弧） |
| 当前进度 | 第1章已完成（final） |

---

## 目录结构

```
末世：我开了GM权限/
│
├── .novel/                    # 项目元数据（系统维护）
│   ├── meta.yaml              # 项目元信息（ID、类型、状态）
│   ├── state.yaml             # 项目状态（当前焦点、消化状态）
│   └── materials.yaml         # 关联的素材库引用
│
├── chapters/                  # 章节文件
│   ├── index.yaml             # 章节索引（状态、字数、伏笔）
│   └── ch001.md               # 第1章《倒计时》
│
├── characters/                # 角色档案
│   ├── character.yaml         # 角色模板（空文件）
│   ├── character_index.yaml   # 角色索引（18个角色）
│   ├── relations.yaml         # 关系快照
│   ├── relations.md           # 关系图谱可视化
│   ├── relation_events.yaml   # 关系演进事件日志
│   │
│   ├── 陈默.yaml              # 主角
│   ├── 宋行舟.yaml            # 配角（僚机）
│   ├── 林知夏.yaml            # 配角（医疗核心）
│   ├── 韩冉.yaml              # 配角（外勤/审讯）
│   ├── 周野.yaml              # 配角（战斗核心）
│   ├── 许晚.yaml              # 配角（情报核心）
│   ├── 老赵.yaml              # 配角
│   ├── 秦烬.yaml              # 反派（白烬会首领）
│   ├── 魏成.yaml              # 反派（前上司）
│   ├── 沈鸢.yaml              # 反派
│   ├── 罗魇.yaml              # 反派
│   ├── 杜阙.yaml              # 反派
│   └── ...                    # 其他配角/龙套
│
├── plot/                      # 剧情大纲
│   ├── outline.md             # 大纲主文件（50章详细规划）
│   ├── outline.yaml           # 大纲结构化数据
│   └── plot_index.yaml        # 情节节点索引
│
├── worldbuilding/             # 世界观设定
│   ├── setting.md             # 世界观概述（叙述性）
│   ├── worldbuilding.yaml     # 设定索引
│   └── entries/               # 设定条目
│       ├── rule_001.yaml      # 世界融合规则
│       ├── rule_002.yaml      # 观测权重机制
│       ├── rule_003.yaml      # 暗潮机制
│       ├── rule_004.yaml      # 据点体系
│       ├── rule_005.yaml      # 主城门槛
│       ├── power_001.yaml     # 灰盒调试器
│       ├── power_002.yaml     # 数据编译者
│       ├── faction_001.yaml   # 白烬会
│       ├── faction_002.yaml   # 烬环商会
│       ├── faction_003.yaml   # 黑潮同盟
│       ├── faction_004.yaml   # 审计者/烬序
│       └── _template.yaml     # 设定模板
│
├── timeline/                  # 时间线
│   └── main.yaml              # 主时间线事件
│
├── scenes/                    # 场景档案
│   └── scene.yaml             # 场景模板（待填充）
│
├── compliance/                # 合规与借鉴
│   ├── inspiration_log.yaml   # 借鉴登记日志
│   └── risk_report.yaml       # 风险检查报告
│
├── quality/                   # 质量管理
│   └── ai_trace_report.yaml   # AI痕迹检测报告
│
├── export/                    # 导出文件
│   └── 末世：我开了GM权限_ch001.txt
│
├── drafts/                    # 原始素材草稿
│
├── ingestion_brief.md         # 素材消化摘要
└── tags.yaml                  # 项目标签
```

---

## 文件说明

### 1. `.novel/` — 项目元数据

由系统自动维护，记录项目的核心状态信息。

| 文件 | 用途 | 维护方式 |
|------|------|----------|
| `meta.yaml` | 项目ID、类型、创建时间、写作配置 | `/novel-init` 创建，系统自动更新 |
| `state.yaml` | 当前焦点、消化状态、剧情结构 | `/novel-status` 查看，系统自动维护 |
| `materials.yaml` | 关联的外部素材库 | `/material-search link` 维护 |

---

### 2. `chapters/` — 章节文件

每章一个 `.md` 文件，包含元数据、场景大纲、正文草稿、伏笔记录。

| 文件 | 说明 |
|------|------|
| `index.yaml` | 章节索引，记录状态、字数、伏笔埋设/回收 |
| `ch001.md` | 第1章正文，状态：final |

**章节状态流转**：
```
idea → outline → draft → revise → final → published
```

**相关命令**：
- `/chapter-create ch002` — 创建新章节
- `/chapter-draft ch002` — 生成章节初稿
- `/chapter-update ch001 --status final` — 更新章节状态
- `/chapter-export ch001-ch010 --format txt --clean` — 导出正文

---

### 3. `characters/` — 角色档案

每个角色一个 `.yaml` 文件，记录五件套（致命缺陷、执念、软肋、误判、反差习惯）。

| 文件 | 说明 |
|------|------|
| `character_index.yaml` | 角色索引，共18个角色（1主角+6配角+7龙套+5反派） |
| `relations.yaml` | 关系快照，当前关系状态 |
| `relation_events.yaml` | 关系演进事件日志 |
| `陈默.yaml` | 主角完整档案 |

**相关命令**：
- `/character-query 陈默` — 查询角色信息
- `/character-edit 陈默` — 编辑角色档案
- `/relationship-add 陈默 林知夏` — 建立角色关系
- `/relationship-map` — 生成关系图谱

---

### 4. `plot/` — 剧情大纲

| 文件 | 说明 |
|------|------|
| `outline.md` | 50章详细大纲，含四阶段结构、伏笔追踪表 |
| `outline.yaml` | 结构化大纲数据 |

**四阶段结构**：
1. 生存奠基（1-10章）：从恐惧到"做项目"
2. 据点成型（11-25章）：从小队到据点治理
3. 远征天穹（26-40章）：从守住到攻城
4. 主城入城（41-50章）：权力与代价

**相关命令**：
- `/plot-query ch001` — 查询章节大纲
- `/plot-add 第2章 首次击杀...` — 添加情节点
- `/plot-review` — 审查大纲结构

---

### 5. `worldbuilding/` — 世界观设定

| 类型 | 文件前缀 | 数量 |
|------|----------|------|
| 规则 | `rule_*.yaml` | 5条 |
| 能力 | `power_*.yaml` | 2种 |
| 势力 | `faction_*.yaml` | 4个 |

**核心设定**：
- **灰盒调试器**：开发者模式入口，代价是观测权重累积
- **观测权重**：权力使用的隐形账本，高权重=被锁定
- **暗潮机制**：每夜0:00-6:00，怪物强化、精神污染上升
- **白烬会**：猎杀GM的组织，反派核心势力

**相关命令**：
- `/setting-add rule_006 新规则名` — 添加设定条目
- `/setting-edit rule_001 --status confirmed` — 确认设定
- `/worldbuilding-review` — 审查世界观自洽性

---

### 6. `timeline/` — 时间线

记录关键事件的时间顺序，用于一致性检查。

**相关命令**：
- `/timeline-add 2026-04-08 世界融合启动` — 添加时间线事件
- `/timeline-check` — 检查时间线冲突
- `/timeline-view` — 查看时间线

---

### 7. `compliance/` — 合规管理

| 文件 | 说明 |
|------|------|
| `inspiration_log.yaml` | 借鉴来源登记（素材ID、借鉴维度） |
| `risk_report.yaml` | 借鉴风险检查报告 |

**相关命令**：
- `/inspiration-log ch001 nm_novel_20260408_bfg7 借鉴了进场模式`
- `/inspiration-check ch001` — 检查章节借鉴风险
- `/inspiration-report ch001-ch010` — 生成范围报告

---

### 8. `quality/` — 质量管理

| 文件 | 说明 |
|------|------|
| `ai_trace_report.yaml` | AI痕迹检测报告（评分、问题片段） |

**相关命令**：
- `/anti-ai-check ch001` — 检测AI痕迹
- `/anti-ai-rewrite ch001 --level 2` — 去AI感改写

---

### 9. `export/` — 导出文件

用于预览、投稿或发布的干净正文文件。

**相关命令**：
- `/chapter-export ch001-ch010 --format txt --clean`

---

## 项目统计

| 维度 | 数量 |
|------|------|
| 章节总数 | 1（目标50章） |
| 角色总数 | 18 |
| 主角 | 1（陈默） |
| 配角 | 6 |
| 龙套 | 7 |
| 反派 | 5 |
| 世界观设定 | 11条 |
| 规则 | 5条 |
| 能力 | 2种 |
| 势力 | 4个 |
| 已埋设伏笔 | 2 |

---

## 常用工作流

### 开始新章节
```
/pipeline-chapter-kickoff ch002
/chapter-draft ch002
/chapter-review ch002
/pipeline-draft-polish ch002
/chapter-update ch002 --status final
```

### 设定补全
```
/setting-add rule_006 新规则名
/worldbuilding-review
```

### 一致性检查
```
/consistency-check
/timeline-check
/relationship-check
```

### 导出投稿
```
/chapter-export ch001-ch010 --format txt --clean
```

---

## 注意事项

1. **状态文件**：`state.yaml` 只存不可推导状态，派生数据由读取方从源文件计算
2. **交叉引用**：角色文件含 `cross_references`，设定文件含 `character_links`，由 `/project-reindex` 统一维护
3. **伏笔管理**：`outline.md` 中有伏笔追踪表，埋设/回收需保持一致
4. **素材借鉴**：每次融合外部素材后，建议用 `/inspiration-log` 登记来源

---

*此文档由系统自动生成，如需更新请运行相关命令后重新生成。*