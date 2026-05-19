# 问题发现：设定文件结构无法支撑复杂系统

> 创建日期：26-05-19
> 问题范围：目录结构、Schema 设计、可扩展性

---

## 一、现象描述

### 1.1 当前设定文件状态

| 文件 | 行数 | 大小 | 内容 | 状态 |
|------|------|------|------|------|
| outline.yaml | 795行 | 49KB | 128个结构元素（acts/sequences/beats）| **已膨胀** |
| worldbuilding.yaml | 14行 | 169B | 空模板 | 待填写 |
| characters.yaml | 1行 | 15B | `characters: []` | 待填写 |

**outline.yaml 已膨胀**：5幕 + 14序列 + 114节拍 → 795行，49KB

### 1.2 Schema 设计的列表结构

**worldbuilding.schema.yaml**（91行）包含多个可扩展列表：

```
factions: []       # 势力列表（每个势力有 key_figures[]）
locations: []      # 地点列表（每个地点有 sub_locations[]）
lore:
  history: []      # 历史事件列表
  artifacts: []    # 重要物品列表
  terminology: []  # 术语词典列表
```

**characters.schema.yaml**（88行）包含：

```
characters: []     # 人物列表
  每个人物包含：
  - relationships: []      # 关系列表
  - key_events: []        # 关键事件列表
  - faction_affiliations: [] # 阵营归属列表
  - arc.stages: []        # 弧线阶段列表
```

**outline.schema.yaml**（81行）包含：

```
acts: []
  每个 act 包含：
  - sequences: []
    每个 sequence 包含：
    - beats: []

plotlines: []      # 情节线索列表
hooks: []          # 伏笔-回收列表
pacing_curve: []   # 节奏曲线列表
```

---

## 二、规模估算

### 2.1 典型小说规模

| 内容 | 数量范围 | 说明 |
|------|---------|------|
| 势力 | 5-15个 | 正派/反派/中立势力，每个势力有档案 |
| 地点 | 10-30个 | 城市/秘境/建筑，每个地点有描述 |
| 人物 | 15-50个 | 主角1 + 反派1-3 + 配角5-15 + 龙套若干 |
| 章节 | 100-200章 | 标准网络小说规模 |
| 节拍 | 100-300个 | 每章1-2个节拍 |

### 2.2 单文件膨胀估算

**worldbuilding.yaml 填写后估算**：

| 内容 | 数量 | 单个行数 | 总行数 |
|------|------|---------|-------|
| 势力档案 | 10个 | 15-30行 | 150-300行 |
| 地点档案 | 20个 | 10-20行 | 200-400行 |
| 历史 | 10个 | 8-15行 | 80-150行 |
| 物品 | 15个 | 10-20行 | 150-300行 |
| 术语 | 30个 | 5-10行 | 150-300行 |

**估算总计**：800-1450行，30-50KB

**characters.yaml 填写后估算**：

| 内容 | 数量 | 单个行数 | 总行数 |
|------|------|---------|-------|
| 主角档案 | 1个 | 40-80行 | 40-80行 |
| 反派档案 | 2个 | 30-60行 | 60-120行 |
| 配角档案 | 10个 | 20-40行 | 200-400行 |
| 龙套档案 | 20个 | 5-10行 | 100-200行 |

**估算总计**：400-800行，15-30KB

**outline.yaml 完整估算**：

| 内容 | 数量 | 单个行数 | 总行数 |
|------|------|---------|-------|
| 幕 | 5个 | 10行 | 50行 |
| 序列 | 15个 | 5行 | 75行 |
| 节拍 | 200个 | 8行 | 1600行 |
| hooks | 30个 | 8行 | 240行 |
| pacing | 50个 | 3行 | 150行 |

**估算总计**：2115行，80-100KB

---

## 三、根本原因

### 3.1 单文件无法支撑复杂系统

**问题**：每个设定类型都用单文件存储所有内容。

| 设定类型 | 当前设计 | 问题 |
|---------|---------|------|
| 世界观 | worldbuilding.yaml 包含所有势力、地点、物品 | 势力/地点/物品都是独立实体，各有档案 |
| 人物 | characters.yaml 包含所有人物 | 每个人物是独立实体，有完整档案 |
| 大纲 | outline.yaml 包含所有节拍 | 每个节拍是独立事件，有详细描述 |

**后果**：
- 文件膨胀：outline.yaml 已 49KB，完整填写会达 100KB
- 难以维护：修改单个势力/人物/节拍，需编辑整个文件
- 难以检索：找单个势力档案，需读整个世界观
- 难以扩展：新增势力/人物，文件持续膨胀

### 3.2 Schema 设计未考虑模块化

**当前 Schema**：定义单文件的顶级字段，不定义子模块。

```yaml
# worldbuilding.schema.yaml
factions: []   # 只定义列表，不定义单个势力结构
locations: []  # 只定义列表，不定义单个地点结构
```

**缺失**：
- 无 `faction.schema.yaml`：单个势力档案结构
- 无 `location.schema.yaml`：单个地点档案结构
- 无 `character.schema.yaml`：单个人物档案结构
- 无 `beat.schema.yaml`：单个节拍结构

---

## 四、影响范围

### 4.1 Skills 工作流受阻

| Skill | 问题 |
|-------|------|
| generate-outline | Agent 需一次性生成 200+节拍，容易出错/遗漏 |
| revise-setting | 修订单个势力/人物，需编辑整个文件，容易误改其他内容 |
| nm 素材检索 | 素材库按"单个势力/人物"组织，无法直接对应到设定文件 |

### 4.2 完善度检查受限

**当前检查**：检查单文件是否存在非空。

```python
check_completeness(project_id, 'worldbuilding')
# 只检查 factions 列表是否非空，无法检查每个势力是否完善
```

**缺失能力**：
- 无法检查单个势力是否填写完整
- 无法检查单个人物档案是否达标
- 无法区分"势力列表存在" vs "每个势力有完整档案"

### 4.3 与素材库协作受限

**素材库结构**（novel-material）：

```
data/novels/nm_novel_xxx/
├── outlines/act_1.yaml   # 每幕独立文件
├── characters/char_001.yaml  # 每个人物独立文件
```

**无法对应**：素材库模块化，本项目单文件，无法直接映射。

---

## 五、数据统计

### 5.1 Schema 复杂度统计

| Schema | 行数 | 可扩展列表数 | 嵌套层数 |
|--------|------|------------|---------|
| worldbuilding.schema.yaml | 91 | 5（factions, locations, history, artifacts, terminology）| 2-3层 |
| characters.schema.yaml | 88 | 1（characters，但每个人物有4个子列表）| 3-4层 |
| outline.schema.yaml | 81 | 3（acts, plotlines, hooks）| 4层（act→sequence→beat）|
| completeness.schema.yaml | 207 | - | - |

### 5.2 单文件膨胀数据

| 文件 | 当前行数 | 填写后估算行数 | 增长倍数 |
|------|---------|--------------|---------|
| outline.yaml | 795 | 2115 | 2.7倍 |
| worldbuilding.yaml | 14 | 800-1450 | 57-103倍 |
| characters.yaml | 1 | 400-800 | 400-800倍 |

---

## 六、诊断结论

**核心问题**：设定文件结构无法支撑复杂系统的规模和演进需求。

| 问题类型 | 具体问题 |
|---------|---------|
| 结构问题 | 单文件存储多个独立实体，无法模块化 |
| 规模问题 | 典型小说规模（100+节拍、20+人物、10+势力）会使文件膨胀到 KB 级 |
| 维护问题 | 修改单个实体需编辑整个文件，容易误改 |
| 扩展问题 | 新增实体持续膨胀文件，无上限 |
| 协作问题 | 与素材库模块化结构不对应 |

**影响**：
- Skills 无法高效生成（一次性生成200+节拍易出错）
- 完善度检查无法细化（只检查列表存在，不检查单个实体完善）
- 素材检索无法对应（素材库模块化 vs 本项目单文件）

---

## 七、重构方向

### 7.1 模块化目录结构

**世界观模块化**：

```
settings/worldbuilding/
├── power_system.yaml      # 力量体系（单文件）
├── factions/              # 势力目录
│   ├── _index.yaml        # 势力列表（name + path）
│   ├── faction_001.yaml   # 单个势力档案
│   └── faction_002.yaml
├── locations/             # 地点目录
│   ├── _index.yaml
│   ├── location_001.yaml
│   └── location_002.yaml
├── lore/                  # 背景知识
│   ├── history.yaml       # 历史事件（列表）
│   ├── artifacts.yaml     # 重要物品（列表）
│   └── terminology.yaml   # 术语词典（列表）
└── rules.yaml             # 核心规则
```

**人物模块化**：

```
settings/characters/
├── protagonist.yaml       # 主角档案（单文件）
├── antagonist.yaml        # 反派档案（单文件）
├── supporting/            # 配角目录
│   ├── _index.yaml
│   ├── char_001.yaml
│   └── char_002.yaml
├── minor/                 # 龙套目录
│   ├── _index.yaml
│   └── char_xxx.yaml
└── relationships.yaml     # 关系网络（单文件）
```

**大纲模块化**：

```
settings/outline/
├── premise.yaml           # 核心设定
├── acts/                  # 幕目录
│   ├── act_1.yaml         # 第1幕（含序列+节拍）
│   ├── act_2.yaml
│   └── act_3.yaml
├── hooks.yaml             # 伏笔-回收
└── pacing.yaml            # 节奏曲线
```

### 7.2 模块化 Schema

新增子模块 Schema：

| Schema | 说明 |
|--------|------|
| faction.schema.yaml | 单个势力档案结构 |
| location.schema.yaml | 单个地点档案结构 |
| character.schema.yaml | 单个人物档案结构 |
| act.schema.yaml | 单幕结构（含序列+节拍）|

### 7.3 完善度检查细化

**当前检查**：
```python
check_completeness(project_id, 'worldbuilding')
# 只检查 worldbuilding.yaml 是否非空
```

**模块化检查**：
```python
check_completeness(project_id, 'worldbuilding')
# 检查：
# - power_system.yaml 是否存在且完善
# - factions/_index.yaml 是否列出至少3个势力
# - 每个势力档案是否完善（name, type, description）
# - locations/_index.yaml 是否列出至少1个地点
# - rules.yaml 是否存在
```

---

## 八、重构目标

| 目标 | 说明 |
|------|------|
| 模块化 | 每个独立实体（势力/人物/节拍）有独立文件 |
| 可扩展 | 新增实体只需添加文件，不膨胀主文件 |
| 可维护 | 修改单个实体只编辑单个文件 |
| 可检索 | 查单个档案只读单个文件 |
| 可对应 | 与素材库模块化结构对应 |

---

## 附：相关文件

- data/schemas/worldbuilding.schema.yaml（91行）— 单文件结构定义
- data/schemas/characters.schema.yaml（88行）— 单文件结构定义
- data/schemas/outline.schema.yaml（81行）— 单文件结构定义
- novels/nv_20260518_b4ze/settings/outline.yaml（795行，49KB）— 已膨胀案例