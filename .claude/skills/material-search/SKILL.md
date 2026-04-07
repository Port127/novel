---
name: material-search
description: 素材库桥接——检索、融合参考素材，管理素材引用
when_to_use: 用户想找参考场景、将参考融合到写作中、或管理项目的素材引用
argument-hint: "[需求描述] | apply [场景ID] [模式] | link [素材ID] | list"
arguments: query
---

# 任务

在 `../novel-material` 素材库中检索参考素材，或管理当前项目的素材引用。

## 前置检查

1. 确认 `../novel-material/` 目录存在
2. 读取 `.current.yaml` 获取 `current_path`
3. 读取 `{current_path}/.novel/materials.yaml`（如不存在则自动创建）
4. 如果素材库不存在，提示：`素材库未找到（预期路径：../novel-material）。请确认目录结构。`

## 输入参数

- `$0+` (query): 自然语言需求描述，或子命令

### 子命令

| 子命令 | 用途 | 示例 |
|--------|------|------|
| （默认） | 检索参考场景/人物/技法 | `/material-search 恋人在雨中告别` |
| `apply` | 将参考场景融合到当前项目 | `/material-search apply ch0042_s03 draft ch005` |
| `link` | 将素材关联到当前项目 | `/material-search link nm_novel_20260405_zhbk` |
| `unlink` | 取消素材与当前项目的关联 | `/material-search unlink nm_novel_20260405_zhbk` |
| `list` | 列出当前项目已关联的素材 | `/material-search list` |
| `available` | 列出素材库中所有可用素材 | `/material-search available` |

### 检索示例

- `/material-search 恋人在雨中告别` → 场景检索
- `/material-search 弱者反杀强者的对决` → 场景检索（标签映射）
- `/material-search 催泪但不煽情的技法` → 技法检索
- `/material-search 都市异能中的小团体互动` → 场景+人物检索

## 执行步骤

### 1. 解析需求 → 标签组合

读取 `../novel-material/data/tags.yaml` 获取合法标签维度，将自然语言映射为标签条件。

| 需求信号 | 映射维度 |
|----------|---------|
| 场景描述 | `--scene-type` + `--setting` |
| 情感需求 | `--emotion` + `--reader-effect` |
| 人物关系 | `--relationship` + `--interaction` |
| 冲突类型 | `--conflict` + `--stakes` |
| 技法/风格 | `--technique` + `--dialogue-type` |
| 角色名 | `--character` |
| 限定小说 | `--material` |

### 2. 调用检索脚本

```bash
python ../novel-material/scripts/search.py scene \
  --scene-type {映射值} --emotion {映射值} --limit 10
```

支持的子命令：
- `scene` — 多维标签检索场景
- `character` — 检索人物原型（`--archetype`, `--name`, `--role`）
- `text` — 全文搜索 summary（`--query`）

脚本自动处理 AND 交集；无结果时自动放宽为 OR 并按匹配度排序。

### 3. 补充详情（可选）

对 Top-3 结果，如果用户需要更多细节，读取对应的场景 YAML：
`../novel-material/data/novels/{material_id}/scenes/{scene_id}.yaml`

### 4. 关联当前项目

检查检索结果与当前项目的关联：
- 读取 `.current.yaml` 获取 `current_path`
- 对照当前项目的大纲、角色、设定，标注参考价值

---

## 素材融合（apply）

将检索到的参考场景融合到当前项目中。不是照搬——是提取机制、结构、节奏、技法，适配到你自己的故事里。

### 用法

```bash
/material-search apply {scene_id} {mode} [{target}]
```

- `scene_id`: 参考场景 ID（从检索结果中获取，如 `ch0042_s03`）
- `mode`: 融合模式（见下表）
- `target`: 融合目标（可选，如章节 ID、大纲节点等）

如果 `scene_id` 来自上一次检索结果，可直接用序号代替：`/material-search apply #1 draft ch005`

### 融合模式

| mode | 做什么 | target | 写入位置 |
|------|--------|--------|---------|
| `draft` | 提取技法和场景结构，融入章节初稿 | 章节 ID | `chapters/{id}.md` 写作备忘 |
| `plot` | 提取冲突结构、转折模式、钩子设计 | 大纲节点或章节范围 | `plot/outline.md` 批注 |
| `setting` | 提取世界观构建方法、规则设计模式 | 设定条目名或类别 | `worldbuilding/entries/` 参考 |
| `rhythm` | 分析节奏曲线（张力升降、场景切换频率） | 章节范围或季 | 节奏分析报告 |
| `character` | 提取人物塑造技法（弧线、缺陷设计、对白区分） | 角色名 | 角色卡批注 |

### 执行步骤

#### 1. 读取参考场景完整数据

从 `../novel-material/data/novels/{material_id}/scenes/{scene_id}.yaml` 读取场景全量信息：
- `summary`、`title`、`chapter`
- 全部 22 维标签（scene_type, conflict, emotion, technique, pacing...）
- `psychology`（角色心理字段）
- `plot_threads`（情节线索）

如果需要更大上下文，同时读取该场景前后相邻场景。

#### 2. 读取当前项目对应上下文

根据 `mode` 和 `target` 读取项目文件：

| mode | 读取 |
|------|------|
| `draft` | 目标章节大纲、角色档案、前后章节 |
| `plot` | `outline.md` + `outline.yaml` 中对应节点 |
| `setting` | `worldbuilding/entries/` 中相关条目 + `setting.md` |
| `rhythm` | 目标范围内所有章节的大纲节点和张力标记 |
| `character` | 目标角色的 `.yaml` 档案 |

#### 3. 生成融合建议

**核心原则：借机制，不借表达。借骨架，不借皮肉。**

针对每种 mode 输出不同维度的分析：

**draft 模式：**
- 参考场景的**开场技法**（如何建立情境和悬念）→ 本章可借鉴的开场策略
- 参考场景的**冲突升级节奏**（几次转折、代价如何递增）→ 本章的冲突设计
- 参考场景的**对白技法**（信息差、潜台词、权力动态）→ 本章对白参考
- 参考场景的**收尾钩子**（悬念类型、情绪落点）→ 本章尾钩

**plot 模式：**
- 参考场景的**冲突类型**和**stakes** → 本项目同类型冲突的升级路径
- 参考场景的**plot_function**（转折/高潮/伏笔）→ 大纲对应位置的功能对齐
- 参考场景的**信息差结构**（谁知道什么、谁被蒙在鼓里）→ 当前剧情的信息差设计

**setting 模式：**
- 参考场景的**世界观规则如何在场景中生效**（不是静态设定，是动态表现）→ 当前设定如何在剧情中体现
- 参考场景的**环境叙事**（设定如何通过环境而非解说呈现）→ 设定呈现技法

**rhythm 模式：**
- 参考场景在原作中的**节奏位置**（紧跟高潮？喘息段？）→ 对比当前项目同位置的节奏
- 参考场景的**张力曲线**（tension 值、pacing 标签）→ 当前章节范围的张力曲线建议
- 参考场景的**场景类型交替模式**（对决→日常→密谋→...）→ 场景类型编排建议

**character 模式：**
- 参考人物的**致命缺陷如何在场景中外化**→ 当前角色的缺陷表现建议
- 参考人物的**对白风格**（句式、用词、信息密度）→ 当前角色的对白区分建议
- 参考人物的**character_moment 类型分布**→ 当前角色的弧线节奏建议

#### 4. 用户确认 → 写入

将融合建议呈现给用户，用户确认后：

- `draft` → 将技法参考写入章节文件的「写作备忘」区域，标注来源
- `plot` → 将结构建议写入 `outline.md` 对应节点的批注
- `setting` → 在对应设定条目的 `plot_links` 中补充表现方式参考
- `rhythm` → 输出节奏分析报告（不写入文件，供用户参考）
- `character` → 将塑造建议写入角色卡的 `notes` 字段

所有写入内容都标注 `[参考来源: {novel_name} — {scene_title}]`，方便追溯。

#### 5. 自动登记借鉴（可选）

如果用户确认采纳了融合建议，提示是否登记到 `inspiration_log.yaml`：

```
💡 是否登记借鉴来源？
   /inspiration-log {target_chapter} {material_id} 借鉴了{scene_title}的{融合维度}
```

### apply 输出格式

```
🔗 素材融合分析

📚 参考：{novel_name} — {scene_title}
🎯 融合目标：{mode} → {target}

---

## 参考场景摘要
> {summary}
🏷️ 关键标签：{scene_type} / {conflict} / {emotion} / {technique}

## 融合建议

### 1. {建议维度}
**参考场景做法：** {参考场景如何处理}
**你的项目适配：** {具体的适配建议}

### 2. {建议维度}
**参考场景做法：** {参考场景如何处理}
**你的项目适配：** {具体的适配建议}

### 3. {建议维度}
...

---

⚠️ 适配注意：{与当前项目设定/角色不兼容的部分}

确认采纳？采纳后将写入 {目标文件}
💡 登记借鉴：/inspiration-log {chapter} {material_id} {说明}
```

---

## 素材引用管理（link / unlink / list / available）

### link — 关联素材到当前项目

1. 读取 `../novel-material/data/index.yaml`，校验素材 ID 存在
2. 读取 `../novel-material/data/novels/{material_id}/meta.yaml`，获取素材名称、作者、状态、场景数
3. 检查 `{current_path}/.novel/materials.yaml` 的 `referenced_materials` 中是否已有该 ID
4. 如果已存在，提示并跳过
5. 追加到 `referenced_materials`：

```yaml
- id: {material_id}
  name: {素材名称}
  author: {作者}
  status: {素材状态}
  relevance: ""  # 留空，让用户补充或 AI 根据项目自动推断
  scenes_available: {场景数}
```

6. 提示用户补充 `relevance`（可选）

**输出：**
```
✅ 素材已关联

📚 {name}（{material_id}）
🎬 可用场景：{scenes_available}
📁 已写入：.novel/materials.yaml

💡 检索该素材场景：/material-search --material {material_id} {需求}
```

### unlink — 取消素材关联

1. 检查 `{current_path}/.novel/materials.yaml` 的 `referenced_materials` 中是否存在该 ID
2. 如果不存在，提示并跳过
3. 检查 `{current_path}/compliance/inspiration_log.yaml` 中是否有引用该素材 ID 的借鉴记录
4. 如果有借鉴记录，**警告但不阻止**：`⚠️ 该素材在 inspiration_log 中有 {N} 条借鉴记录。取消关联不会删除借鉴记录。`
5. 从 `referenced_materials` 列表中移除该条目

**输出：**
```
✅ 素材已取消关联

📚 {name}（{material_id}）
📁 已更新：.novel/materials.yaml
```

### list — 列出当前项目已关联的素材

读取 `{current_path}/.novel/materials.yaml`，展示所有 `referenced_materials`。

**输出：**
```
📋 当前项目关联素材（{count} 部）

| # | 素材 | 作者 | 状态 | 场景数 | 关联说明 |
|---|------|------|------|--------|---------|
| 1 | {name} | {author} | {status} | {scenes} | {relevance} |
| ... |

💡 关联新素材：/material-search link {id}
💡 查看可用素材：/material-search available
```

### available — 列出素材库中所有可用素材

读取 `../novel-material/data/index.yaml`，列出所有素材，标注哪些已关联到当前项目。

**输出：**
```
📋 素材库可用素材（{total} 部）

| # | 素材 | 作者 | 状态 | 已关联 |
|---|------|------|------|--------|
| 1 | {name} | {author} | {status} | ✅/— |
| ... |

💡 关联素材：/material-search link {id}
```

---

## 检索输出格式

```
🔍 检索条件：{解析后的标签组合}
🗄️ 素材库：../novel-material（{N} 部小说，{M} 个场景）

---

## 匹配 1 ⭐⭐⭐⭐⭐
📚 来源：{novel_name}（{material_id}）
🎬 场景：{scene_title}（{scene_id}）
📖 章节：{chapter}
> {summary}
🏷️ 匹配标签：{matched_tags}
💡 参考价值：{与当前项目的关联说明}

---

## 匹配 2 ⭐⭐⭐⭐
...

---

📊 共找到 {count} 个匹配场景
💡 融合到写作：/material-search apply {scene_id} draft|plot|setting|rhythm|character {target}
💡 更精确检索：/material-search {补充条件}
💡 记录借鉴：/inspiration-log {章节ID} {material_id} {借鉴说明}
```

## 注意事项

- 本 skill 是 `../novel-material` 的轻量桥接，不复制数据到本项目
- 检索路径固定为 `../novel-material/scripts/search.py`，与素材库约定一致
- `link`/`unlink` 只操作 `materials.yaml` 引用列表，不影响素材库本身
- `unlink` 不会删除已有的借鉴记录（`inspiration_log.yaml`）
- 如果需要记录借鉴来源，使用 `/inspiration-log` 登记素材 ID
- SQLite 不可用时，回退读取 `../novel-material/data/novels/*/scenes_index.yaml`
