# 重构计划：模板系统 + Pipeline 流程

> 创建日期：26-05-19
> 关联问题：[issues-settings-modularization](26-05-19-issues-settings-modularization.md)
> 规模要求：800章 × 4000字 = 320万字
> 核心需求：模板初始化 + Pipeline 组织

---

## 执行原则

1. **模板优先**：新项目通过模板初始化，不硬编码结构
2. **Pipeline 组织**：Skills 按流程编排，而非散落调用
3. **先建后删**：新建模板系统 → 改 project.py → 删除旧硬编码
4. **清理旧项目**：nv_20260518_b4ze 保持现状，新项目用模板

---

## 批次规划

```
批次1：创建模板系统
       ↓ templates/ 目录 + 模块化模板
批次2：改 project.py 初始化
       ↓ 从模板复制而非硬编码
批次3：定义 Pipeline 流程
       ↓ 流程文档 + create-novel skill 改为流程引导
批次4：更新 Skills 文档
       ↓ 统一 pipeline 入口说明
批次5：清理旧硬编码
       ↓ 删除 project.py 内的硬编码设定
```

**依赖关系**：
- 批次1 → 批次2（模板存在才能复制）
- 批次2 → 批次3（项目结构正确才能定义流程）
- 批次3 → 批次4（流程定义后才能更新 Skills）
- 批次4 → 批次5（Skills 更新后才能清理旧代码）

---

## 批次1：创建模板系统

### 目标

创建 templates/ 目录，定义模块化项目模板。

### 步骤1：创建模板目录

**新建目录**：
```bash
mkdir -p templates/default/settings/worldbuilding/factions
mkdir -p templates/default/settings/worldbuilding/locations
mkdir -p templates/default/settings/worldbuilding/lore
mkdir -p templates/default/settings/characters/protagonist
mkdir -p templates/default/settings/characters/antagonist
mkdir -p templates/default/settings/characters/supporting
mkdir -p templates/default/settings/characters/minor
mkdir -p templates/default/settings/outline/acts
mkdir -p templates/default/settings/chapters
mkdir -p templates/default/content/chapters
```

### 步骤2：创建模板文件

**worldbuilding/power_system.yaml 模板**：
```yaml
# 力量体系模板
name: ""                          # [R] 体系名称
type: ""                          # [R] 体系类型（灵气/魔法/斗气/科技/超能力/异能/无）

levels:                           # [R] 等级划分（至少3级）
  - name: ""
    description: ""
    capabilities: []
  - name: ""
    description: ""
    capabilities: []

rules: []                         # [O] 核心规则
  # 每个规则：
  # - rule: 规则内容
  # - implications: 规则影响

limitations: []                   # [O] 限制条件
```

**worldbuilding/factions/_index.yaml 模板**：
```yaml
# 势力索引模板
factions: []                      # 势力列表（创建时填充）
  # 每个势力：
  # - faction_id: faction_001
  # - name: 势力名称
  # - path: faction_001.yaml

completeness: 0%
min_required: 3                   # 最少势力数
```

**worldbuilding/factions/faction_template.yaml**：
```yaml
# 单势力档案模板
faction_id: ""                    # [R] 势力ID
name: ""                          # [R] 势力名称
type: ""                          # [R] 势力类型（宗门/王朝/公司/家族/军团/教会/帮派/组织）
stance: ""                        # [R] 立场（正派/中立/反派/不确定）
description: ""                   # [R] 势力描述

territory: ""                     # [O] 势力范围
key_figures: []                   # [O] 关键人物
history: []                       # [O] 势力历史
goals: []                         # [O] 势力目标
conflicts: []                     # [O] 与其他势力的冲突
```

**characters/protagonist/protagonist.yaml 模板**：
```yaml
# 主角档案模板
name: ""                          # [R] 姓名
archetype: ""                     # [R] 人物原型（废柴逆袭/天才型/导师型/其他）
description: ""                   # [R] 核心描述

traits: []                        # [R] 性格特征（至少2个）

psychology:                       # [R] 心理维度
  fatal_flaw: ""                  # [R] 关键缺陷
  obsession: ""                   # [R] 执念
  soft_spot: ""                   # [R] 软肋
  misbelief: ""                   # [R] 误判

arc:                              # [R] 人物弧线
  type: ""                        # [R] 弧线类型（成长/堕落/悲剧/探索/扁平）
  start: ""                       # [R] 起点状态
  end: ""                         # [R] 终点状态
  stages: []                      # [O] 弧线阶段

appearance:                       # [O] 外貌描述
  age: ""
  gender: ""
  features: []

faction_affiliations: []          # [O] 阵营归属
key_events: []                    # [O] 关键事件
```

**characters/relationships.yaml 模板**：
```yaml
# 关系网络模板
relationships: []
  # 每个关系：
  # - from: 人物A
  # - to: 人物B
  # - type: 关系类型（血缘/师徒/敌对/合作/暧昧）
  # - description: 关系描述
  # - importance: 重要程度（primary/secondary/minor）
  # - start_chapter: 关系开始章节
```

**outline/premise.yaml 模板**：
```yaml
# 核心设定模板
premise_statement: ""             # [R] 核心前提（一句话概括，≥50字）
themes: []                        # [R] 主题标签（至少2个）
tones: []                         # [O] 基调标签

target_chapters: 800              # [R] 目标章数
target_words_per_chapter: 4000    # [R] 目标单章字数
```

**outline/acts/_index.yaml 模板**：
```yaml
# 幕索引模板
acts: []                          # 幕列表（创建时填充）
  # 每幕：
  # - act_number: 1
  # - path: act_1.yaml

completeness: 0%
min_required: 3                   # 最少幕数
```

**outline/acts/act_template.yaml**：
```yaml
# 单幕结构模板
act_number: 1                     # [R] 幕编号
name: ""                          # [R] 幕名称

chapter_range:                    # [R] 章节范围
  start: 1
  end: 100

arc: ""                           # [R] 本幕叙事弧线

sequences: []                     # [R] 序列列表（至少2个）
  # 每个序列：
  # - sequence_number: 1
  # - name: 序列名称
  # - chapter_range: {start, end}
  # - description: 序列描述
  # - beats: []                   # 节拍列表（至少5个）
  #   每个节拍：
  #   - beat_number: 1
  #   - chapter: 所在章节
  #   - title: 节拍名称
  #   - description: 节拍描述（≥30字）
  #   - tension: 张力值（1-5）
  #   - characters_appear: []

turning_point:                    # [O] 转折点
  chapter: 100
  type: ""                        # 转折类型
  description: ""
```

**outline/hooks.yaml 模板**：
```yaml
# 伏笔-回收模板
hooks: []
  # 每个伏笔：
  # - hook_id: H001
  # - hook_type: 伏笔类型（道具/人物/悬念/信息/情感）
  # - planted_chapter: 埋设章节
  # - detail: 伏笔描述
  # - harvested_chapter: 回收章节（可选）
  # - resolution: 回收方式（可选）
```

**outline/pacing.yaml 模板**：
```yaml
# 节奏曲线模板
pacing_curve: []
  # 每个节点：
  # - chapter: 章节号
  # - tension: 张力值（1-5）
  # - label: 节点标签（开局/转折/高潮/收束）
```

**chapters/_index.yaml 模板**：
```yaml
# 章节索引模板
total_chapters: 800               # 目标章数
chapters: []                      # 章节列表（创建时填充）

stats:
  planned: 0
  draft: 0
  written: 0
  revised: 0
  total_words: 0

completeness: 0%
```

**chapters/chapter_template.yaml**：
```yaml
# 单章档案模板
chapter: 1                        # [R] 章节号
title: ""                         # [R] 章节标题
summary: ""                       # [R] 章节摘要（≥50字）

word_count_target: 4000           # [R] 目标字数
word_count_actual: 0              # [O] 实际字数

tension_level: 3                  # [R] 张力值（1-5）
status: planned                   # [R] 状态（planned/draft/written/revised）

characters_appear: []             # [R] 出场人物
key_event: ""                     # [O] 关键事件
setting: []                       # [O] 场景地点

emotional_tone: []                # [O] 情绪基调
chapter_functions: []             # [O] 章节功能
technique: []                     # [O] 写作技法

notes: ""                         # [O] 写作备注
draft_path: ""                    # [O] 草稿路径
content_path: ""                  # [O] 正文路径
```

**project.yaml 模板**：
```yaml
project_id: ""                    # 创建时生成
name: ""                          # [R] 项目名称
author: ""                        # [R] 作者
genre: ""                         # [R] 类型
status: planning                  # 项目状态

created: ""                       # 创建时生成
updated: ""                       # 创建时生成

target:
  chapters: 800                   # 目标章数
  words_per_chapter: 4000         # 单章字数
  total_words: 3200000            # 总字数

stats:
  chapters_written: 0
  chapters_planned: 0
  words_total: 0

pipeline_status:                  # Pipeline 状态
  current_stage: 0                # 当前阶段（0=初始化）
  completed_stages: []            # 已完成阶段

references: []

ai_config:
  model: gpt-4o-mini
  style_guide: ""
  auto_save: true
```

### 步骤3：创建模板元信息

**templates/default/template.yaml**：
```yaml
# 模板元信息
template_name: default
template_version: 1.0
description: 默认小说项目模板（800章 × 4000字规模）

structure:
  settings:
    - worldbuilding/
    - characters/
    - outline/
    - chapters/
  content:
    - chapters/

pipeline:                         # 该模板对应的 Pipeline
  stages:
    - 1-worldbuilding
    - 2-characters
    - 3-outline
    - 4-chapter-planning
    - 5-writing
```

### 步骤4：验证模板创建

**验证命令**：
```bash
find templates/default -type d | wc -l
# 预期：至少15个目录

find templates/default -name "*.yaml" | wc -l
# 预期：至少20个模板文件
```

---

## 批次2：改 project.py 初始化

### 目标

project.py create 从模板复制，而非硬编码结构。

### 步骤1：修改 create_project 函数

**改动文件**：`scripts/project.py`

**改前**（第30-128行）：
```python
def create_project(name: str, genre: str = "修仙", author: str = "匿名") -> str:
    """创建新写作项目。"""
    project_id = generate_project_id()
    project_dir = NOVELS_DIR / project_id

    # 创建目录结构（硬编码）
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "settings").mkdir(exist_ok=True)
    ...
    
    # 创建设定文件（硬编码内容）
    (settings_dir / "worldbuilding.yaml").write_text(...)
```

**改后**：
```python
TEMPLATES_DIR = _ROOT / "templates"

def create_project(name: str, genre: str = "修仙", author: str = "匿名", template: str = "default") -> str:
    """从模板创建新写作项目。"""
    project_id = generate_project_id()
    project_dir = NOVELS_DIR / project_id
    
    # 检查模板是否存在
    template_dir = TEMPLATES_DIR / template
    if not template_dir.exists():
        print(f"❌ 模板不存在: {template}")
        print(f"可用模板: {list_available_templates()}")
        return None
    
    # 从模板复制整个目录结构
    shutil.copytree(template_dir, project_dir)
    
    # 更新 project.yaml（填充项目信息）
    project_yaml_path = project_dir / "project.yaml"
    today = datetime.now().strftime("%Y-%m-%d")
    
    with open(project_yaml_path, encoding="utf-8") as f:
        project_data = yaml.safe_load(f)
    
    project_data["project_id"] = project_id
    project_data["name"] = name
    project_data["author"] = author
    project_data["genre"] = genre
    project_data["created"] = today
    project_data["updated"] = today
    
    with open(project_yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(project_data, f, allow_unicode=True, default_flow_style=False)
    
    print(f"✅ 项目创建成功: {project_id}")
    print(f"   模板: {template}")
    print(f"   目录: {project_dir}")
    print(f"   名称: {name}")
    print(f"   类型: {genre}")
    print()
    print("Pipeline 流程:")
    print("   1. 阶段1 - 世界观设定")
    print("   2. 阶段2 - 人物设定")
    print("   3. 阶段3 - 大纲设定")
    print("   4. 阶段4 - 章节规划")
    print("   5. 阶段5 - 正文写作")
    print()
    print("下一步:")
    print("   使用 /create-novel 开始 Pipeline 流程")
    
    return project_id

def list_available_templates() -> list:
    """列出可用模板。"""
    if not TEMPLATES_DIR.exists():
        return []
    
    templates = []
    for template_dir in TEMPLATES_DIR.iterdir():
        if template_dir.is_dir():
            template_yaml = template_dir / "template.yaml"
            if template_yaml.exists():
                with open(template_yaml, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                templates.append({
                    "name": template_dir.name,
                    "description": data.get("description", ""),
                    "version": data.get("template_version", "1.0")
                })
    
    return templates
```

### 步骤2：更新 CLI 参数

**改动文件**：`scripts/project.py`

**改前**（第243-264行）：
```python
if command == "create":
    if len(sys.argv) < 3:
        print("用法: python scripts/project.py create <项目名> [--genre <类型>] [--author <作者>]")
        sys.exit(1)

    name = sys.argv[2]
    genre = "修仙"
    author = "匿名"
    ...
```

**改后**：
```python
if command == "create":
    if len(sys.argv) < 3:
        print("用法: python scripts/project.py create <项目名> [--genre <类型>] [--author <作者>] [--template <模板>]")
        print("可用模板:")
        for t in list_available_templates():
            print(f"  - {t['name']}: {t['description']}")
        sys.exit(1)

    name = sys.argv[2]
    genre = "修仙"
    author = "匿名"
    template = "default"

    # 解析可选参数
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--genre" and i + 1 < len(sys.argv):
            genre = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--author" and i + 1 < len(sys.argv):
            author = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--template" and i + 1 < len(sys.argv):
            template = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    create_project(name, genre, author, template)
```

### 步骤3：添加依赖导入

**改动文件**：`scripts/project.py`

**改前**（第1-20行）：
```python
import sys
import shutil
from pathlib import Path
from datetime import datetime
import random
import string
```

**改后**：
```python
import sys
import shutil
from pathlib import Path
from datetime import datetime
import random
import string
import yaml
```

### 步骤4：验证 project.py

**验证命令**：
```bash
python scripts/project.py create "测试小说" --genre 都市 --template default
# 预期：从模板复制，创建模块化目录结构

ls novels/nv_xxx/settings/
# 预期：worldbuilding/, characters/, outline/, chapters/（模块化目录）
```

---

## 批次3：定义 Pipeline 流程

### 目标

创建 Pipeline 文档，组织 Skills 的执行顺序。

### 步骤1：创建 Pipeline 文档

**新建文件**：`docs/PIPELINE.md`

**内容**：
```markdown
# Novel V2 Pipeline 流程

> Pipeline 是 Skills 的执行流程，确保创作按正确顺序进行。

---

## Pipeline 阶段

| 阶段 | 名称 | Skills | 输出 | 完善度阈值 |
|------|------|--------|------|-----------|
| 1 | 世界观设定 | nm + Agent 交互 | worldbuilding/ 目录 | 80% |
| 2 | 人物设定 | generate-character | characters/ 目录 | 70% |
| 3 | 大纲设定 | generate-outline | outline/ 目录 | 85% |
| 4 | 章节规划 | generate-chapter | chapters/ 目录 | 100%（每章）|
| 5 | 正文写作 | write-chapter | content/chapters/ | - |

---

## Pipeline 入口

**推荐使用 `/create-novel`**，它会：
1. 检查当前项目状态
2. 判断处于哪个阶段
3. 引导用户完成当前阶段
4. 自动进入下一阶段

---

## 各阶段详情

### 阶段 1：世界观设定

**目标**：建立小说世界的基础设定。

**Skills 组合**：
1. `/nm` — 检索同类题材素材参考
2. Agent 交互讨论 — 确认力量体系、势力、地点
3. 直接生成 — 写入 worldbuilding/ 目录各文件

**输出**：
- `worldbuilding/power_system.yaml` — 力量体系
- `worldbuilding/factions/faction_*.yaml` — 势力档案（≥3个）
- `worldbuilding/locations/location_*.yaml` — 地点档案（≥1个）
- `worldbuilding/lore/*.yaml` — 背景知识（可选）

**完善度检查**：
```bash
python scripts/utils/completeness_check.py {project_id} worldbuilding --modules
```

**阈值**：
- power_system: 100%（name + levels + rules 必填）
- factions: 80%（至少3个势力，每个有完整档案）
- locations: 100%（至少1个地点）

---

### 阶段 2：人物设定

**目标**：建立小说的核心角色。

**前置依赖**：世界观完善度 ≥ 80%

**Skills 组合**：
1. `/nm` — 检索同类人物塑造参考
2. `/generate-character` — 交互生成人物档案
3. Agent 直接生成 — 写入 characters/ 目录各文件

**输出**：
- `characters/protagonist/protagonist.yaml` — 主角档案
- `characters/antagonist/antagonist_*.yaml` — 反派档案（≥1个）
- `characters/supporting/supporting_*.yaml` — 配角档案（≥3个）
- `characters/relationships.yaml` — 关系网络

**完善度检查**：
```bash
python scripts/utils/completeness_check.py {project_id} characters --modules
```

**阈值**：
- protagonist: 100%（traits + psychology + arc 必填）
- antagonist: 80%（至少1个反派，每个有完整档案）
- supporting: 70%（至少3个配角）

---

### 阶段 3：大纲设定

**目标**：规划全书结构（800章）。

**前置依赖**：世界观 ≥ 80%，人物 ≥ 70%

**Skills 组合**：
1. `/nm` — 检索同类大纲结构参考
2. `/generate-outline` — 交互生成大纲
3. Agent 直接生成 — 写入 outline/ 目录各文件

**输出**：
- `outline/premise.yaml` — 核心设定
- `outline/acts/act_*.yaml` — 各幕结构（≥3幕）
- `outline/hooks.yaml` — 伏笔-回收（可选）
- `outline/pacing.yaml` — 节奏曲线（可选）

**完善度检查**：
```bash
python scripts/utils/completeness_check.py {project_id} outline --modules
```

**阈值**：
- premise: 100%（premise_statement ≥ 50字）
- acts: 85%（至少3幕，每幕 ≥ 2序列，每序列 ≥ 5节拍）

---

### 阶段 4：章节规划

**目标**：将大纲转化为章节摘要。

**前置依赖**：大纲完善度 ≥ 85%

**Skills 组合**：
1. `/generate-chapter` — 从大纲转化章节摘要
2. Agent 直接生成 — 写入 chapters/ 目录各文件

**输出**：
- `chapters/_index.yaml` — 章节索引
- `chapters/chapter_*.yaml` — 各章档案（每章）

**完善度检查**：
```bash
python scripts/utils/completeness_check.py {project_id} chapters --target {章节号}
```

**阈值**：
- 目标章节: 100%（summary + characters_appear + tension_level 必填）

---

### 阶段 5：正文写作

**目标**：根据章节摘要生成正文（4000字/章）。

**前置依赖**：目标章节完善度 = 100%

**Skills 组合**：
1. `/write-chapter` — 确认摘要 → 生成正文 → 续写/改写
2. Agent 直接生成 — 写入 content/chapters/ 目录

**输出**：
- `content/chapters/chapter_*.md` — 章节正文

**字数要求**：
- draft: ≥ 2000字
- written: ≥ 4000字
- revised: ≥ 4000字（已润色）

---

## Pipeline 状态追踪

项目 `project.yaml` 中包含 `pipeline_status` 字段：

```yaml
pipeline_status:
  current_stage: 2                # 当前阶段
  completed_stages: [1]           # 已完成阶段
  blocked_stages: []              # 阻塞阶段（前置依赖不满足）
```

---

## 流程图

```
项目创建（project.py create）
    ↓
阶段1：世界观设定
    ↓ 完善度 ≥ 80%
阶段2：人物设定
    ↓ 完善度 ≥ 70%
阶段3：大纲设定
    ↓ 完善度 ≥ 85%
阶段4：章节规划
    ↓ 目标章节完善度 = 100%
阶段5：正文写作
    ↓
完成：导出作品
```

---

## 跳阶段处理

**禁止跳阶段**：
- 未完成阶段1 → 不能执行阶段2
- 未完成阶段2 → 不能执行阶段3
- ...

**跳阶段尝试时**：
- `/create-novel` 会阻止并提示缺失前置
- `/generate-*` Skills 会检查前置完善度

**示例**：
```
用户尝试：/generate-outline

检查结果：
  阶段1（世界观）完善度 20% ❌
  阶段2（人物）完善度 0% ❌

阻止：请先完成阶段1和阶段2
引导：是否开始世界观设定？
```
```

### 步骤2：更新 create-novel/SKILL.md

**改动文件**：`.claude/skills/create-novel/SKILL.md`

**改后内容**：
```markdown
---
name: create-novel
description: Pipeline 流程入口，引导用户按阶段完成创作
---

# Pipeline 流程入口

**核心功能**：组织 Skills 的执行顺序，确保按正确流程创作。

---

## Pipeline 阶段

| 阶段 | 名称 | 前置依赖 | 完善度阈值 |
|------|------|---------|-----------|
| 1 | 世界观设定 | 无 | 80% |
| 2 | 人物设定 | 阶段1完成 | 70% |
| 3 | 大纲设定 | 阶段1+2完成 | 85% |
| 4 | 章节规划 | 阶段3完成 | 100% |
| 5 | 正文写作 | 阶段4完成 | - |

---

## 工作流程

### 1. 检查项目状态

读取 `project.yaml` 的 `pipeline_status`：

```yaml
pipeline_status:
  current_stage: 0                # 当前阶段
  completed_stages: []            # 已完成阶段
```

### 2. 判断当前阶段

| current_stage | 说明 | 下一步 |
|---------------|------|--------|
| 0 | 初始化，无设定 | 开始阶段1 |
| 1 | 世界观进行中 | 继续或完成阶段1 |
| 2 | 人物进行中 | 继续或完成阶段2 |
| 3 | 大纲进行中 | 继续或完成阶段3 |
| 4 | 章节规划进行中 | 继续或完成阶段4 |
| 5 | 写作进行中 | 继续写作 |

### 3. 检查前置依赖

对当前阶段检查前置依赖完善度：

```bash
python scripts/utils/completeness_check.py {project_id} worldbuilding --modules
python scripts/utils/completeness_check.py {project_id} characters --modules
python scripts/utils/completeness_check.py {project_id} outline --modules
```

### 4. 引导执行当前阶段

**阶段1引导**：
```
当前阶段：阶段1 - 世界观设定
前置依赖：无

执行步骤：
  1. 使用 /nm 检索同类题材参考
  2. 与 Agent 讨论确认力量体系、势力、地点
  3. Agent 直接生成 worldbuilding/ 目录各文件

是否开始世界观设定？
``

**阶段2引导**：
```
当前阶段：阶段2 - 人物设定
前置依赖：
  - 阶段1 完善度 85% ✅

执行步骤：
  1. 使用 /nm 检索同类人物塑造参考
  2. 使用 /generate-character 交互生成人物
  3. Agent 直接生成 characters/ 目录各文件

是否开始人物设定？
``

**跳阶段阻止**：
```
当前阶段：阶段3 - 大纲设定
前置依赖检查：
  - 阶段1 完善度 20% ❌（需 ≥ 80%）
  - 阶段2 完善度 0% ❌（需 ≥ 70%）

阻止原因：前置依赖不满足
引导：请先完成阶段1和阶段2
      是否返回阶段1？
```

### 5. 更新 Pipeline 状态

阶段完成后更新 `project.yaml`：

```yaml
pipeline_status:
  current_stage: 2                # 进入下一阶段
  completed_stages: [1]           # 记录已完成
```

---

## Pipeline 文档

详见 `docs/PIPELINE.md`
```

### 步骤3：验证 Pipeline

**验证命令**：
```bash
cat docs/PIPELINE.md
# 预期：完整的 Pipeline 流程文档

cat .claude/skills/create-novel/SKILL.md
# 预期：Pipeline 阶段表格 + 流程引导
```

---

## 批次4：更新 Skills 文档

### 目标

统一 Skills 文档的 Pipeline 入口说明。

### 步骤1：更新各 Skills 文档头部

**改动文件**：`generate-outline/SKILL.md`, `generate-character/SKILL.md`, `generate-chapter/SKILL.md`, `write-chapter/SKILL.md`

**添加内容**：
```markdown
## Pipeline 位置

此 Skill 属于 Pipeline 流程的一部分：

| 阶段 | Skill |
|------|-------|
| 1 | nm + Agent 交互 |
| 2 | generate-character |
| 3 | generate-outline ← 本 Skill |
| 4 | generate-chapter |
| 5 | write-chapter |

**推荐入口**：使用 `/create-novel` 自动引导 Pipeline 流程。
```

### 步骤2：更新 nm/SKILL.md

**改动文件**：`.claude/skills/nm/SKILL.md`

**添加内容**：
```markdown
## Pipeline 位置

nm skill 可在多个阶段使用：

| 阶段 | 用途 |
|------|------|
| 1 | 检索同类题材世界观参考 |
| 2 | 检索同类人物塑造参考 |
| 3 | 检索同类大纲结构参考 |

**推荐入口**：使用 `/create-novel` 自动引导 Pipeline 流程。
```

---

## 批次5：清理旧硬编码

### 目标

删除 project.py 中的硬编码设定结构。

### 步骤1：删除硬编码内容

**改动文件**：`scripts/project.py`

**删除内容**（第68-116行，硬编码设定文件创建）：
```python
# 删除：创建空的设定文件（硬编码）
settings_dir = project_dir / "settings"
(settings_dir / "worldbuilding.yaml").write_text(...)
(settings_dir / "characters.yaml").write_text(...)
(settings_dir / "outline.yaml").write_text(...)
(settings_dir / "notes.yaml").write_text(...)

# 删除：创建章节索引（硬编码）
(project_dir / "chapters" / "_index.yaml").write_text(...)
```

**删除条件**：模板系统可用后，硬编码内容被模板复制替代。

### 步骤2：验证清理

**验证命令**：
```bash
grep "worldbuilding.yaml" scripts/project.py
# 预期：无匹配（已删除硬编码）

grep "shutil.copytree" scripts/project.py
# 预期：有匹配（使用模板复制）
```

---

## 完成检查清单

- [x] 批次1：templates/default/ 目录已创建
- [x] 批次1：模板文件已创建（≥20个）
- [x] 批次1：template.yaml 元信息已创建
- [x] 批次2：project.py 已改为从模板复制
- [x] 批次2：--template 参数已添加
- [x] 批次2：create_project 函数已更新
- [x] 批次3：docs/PIPELINE.md 已创建
- [x] 批次3：create-novel/SKILL.md 已更新（Pipeline 流程）
- [x] 批次4：各 Skills 文档已添加 Pipeline 位置说明
- [x] 批次4：nm/SKILL.md 已添加多阶段用途说明
- [x] 批次5：project.py 硬编码已删除
- [x] 批次5：验证通过（无硬编码，使用模板）

**执行完成日期**：26-05-19

---

## 附：改动文件清单

| 新建 | 路径 | 说明 |
|------|------|------|
| templates/default/ | templates/ | 默认模板目录 |
| templates/default/settings/worldbuilding/ | templates/ | 世界观模块模板 |
| templates/default/settings/characters/ | templates/ | 人物模块模板 |
| templates/default/settings/outline/ | templates/ | 大纲模块模板 |
| templates/default/settings/chapters/ | templates/ | 章节模块模板 |
| templates/default/content/chapters/ | templates/ | 正文内容模板 |
| docs/PIPELINE.md | docs/ | Pipeline 流程文档 |

| 修改 | 路径 | 改动内容 |
|------|------|---------|
| scripts/project.py | create_project 改为从模板复制 |
| scripts/project.py | CLI 添加 --template 参数 |
| create-novel/SKILL.md | Pipeline 流程入口 |
| generate-*/SKILL.md | 添加 Pipeline 位置说明 |
| nm/SKILL.md | 添加多阶段用途说明 |

| 删除 | 路径 | 删除内容 |
|------|------|---------|
| scripts/project.py | 硬编码设定文件创建（第68-116行）|