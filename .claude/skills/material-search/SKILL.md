---
name: material-search
description: 在素材库中检索参考素材（场景/大纲/角色弧光/节奏模式）
when_to_use: 用户想找参考场景、参考大纲结构、参考角色弧光或参考叙事节奏
argument-hint: "[需求描述] | outline [描述] | character-arc [描述] | rhythm [描述]"
arguments: query
---

# 任务

在 `../novel-material` 素材库中检索参考素材。搜索完成后，用 `/material-apply` 融合到项目，用 `/material-manage` 管理素材关联。

## 前置检查

1. 确认 `../novel-material/` 目录存在
2. 读取 `.current.yaml` 获取 `current_path`
3. 如果素材库不存在，提示：`素材库未找到（预期路径：../novel-material）。请确认目录结构。`

## 输入参数

- `$0+` (query): 自然语言需求描述，或子命令

### 四种检索维度

| 子命令 | 检索什么 | 数据源 | 示例 |
|--------|---------|--------|------|
| （默认） | 场景/人物/技法 | 场景 YAML | `/material-search 恋人在雨中告别` |
| `outline` | 大纲结构 | `outline.yaml` | `/material-search outline 废物逆袭的三幕结构` |
| `character-arc` | 角色弧光 | `characters.yaml` | `/material-search character-arc 导师牺牲线` |
| `rhythm` | 叙事节奏模式 | 场景 pacing/tension | `/material-search rhythm 开篇快节奏案件推进` |

### 检索示例

**场景级（默认）：**
- `/material-search 恋人在雨中告别`
- `/material-search 弱者反杀强者的对决`
- `/material-search 催泪但不煽情的技法`

**大纲级：**
- `/material-search outline 从废物到强者的逆袭结构`
- `/material-search outline 中点反转 导师死亡`

**角色弧光级：**
- `/material-search character-arc 导师牺牲线`
- `/material-search character-arc 反派洗白弧`
- `/material-search character-arc 许七安`

**节奏级：**
- `/material-search rhythm 开篇快节奏案件推进`
- `/material-search rhythm 高潮前的蓄力段`
- `/material-search rhythm --material nm_novel_xxx 第二卷`

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

### 2. 调用检索（按子命令分路）

#### 2a. 默认（场景检索）

```bash
python ../novel-material/scripts/search.py scene \
  --scene-type {映射值} --emotion {映射值} --limit 10
```

脚本子命令：`scene`（标签检索）、`character`（人物原型）、`text`（全文搜索）。
无结果时自动放宽为 OR 并按匹配度排序。

#### 2b. outline（大纲检索）

读取各小说 `../novel-material/data/novels/{material_id}/outline.yaml`：
- 从 `premise`、`theme`、`tone` 匹配故事基调
- 从 `structure[].arc`、`key_event`、`turning_point` 匹配结构骨架
- 从 `structure[].pacing_note` 匹配节奏特征

指定 `--material` 时只读取该小说。

#### 2c. character-arc（角色弧光检索）

读取各小说 `../novel-material/data/novels/{material_id}/characters.yaml`：
- 按 `archetype` 匹配角色类型
- 按 `psychology`（fatal_flaw / obsession / tragedy_trigger）匹配深层特征
- 按 `arc[].stage` 匹配弧光模式
- 按角色名直接搜索

#### 2d. rhythm（节奏模式检索）

从场景数据聚合节奏信息：
- 提取 `pacing`、`tension`、`plot_stage`、`plot_function` 字段
- 按章节顺序排列，绘制张力曲线
- 识别节奏模式：加速段、喘息段、蓄力段、爆发段

指定卷/章节范围时只分析该范围。

### 3. 补充详情（可选）

Top-3 结果如需更多细节：
- 场景级：读取 `scenes/{scene_id}.yaml`
- 大纲级：读取完整 `outline.yaml`
- 角色级：读取 `characters.yaml` 中该角色条目
- 节奏级：读取该范围内所有场景的 pacing/tension

### 4. 关联当前项目

对照当前项目的大纲、角色、设定，标注参考价值。

## 输出格式

**场景级：**
```
检索条件：{标签组合}

匹配 1
来源：{novel_name}（{material_id}）
场景：{scene_title}（{scene_id}）
> {summary}
匹配标签：{matched_tags}
参考价值：{关联说明}

共找到 {count} 个匹配
  融合：/material-apply {scene_id} draft|plot|setting|character {target}
```

**大纲级：**
```
大纲检索：{需求}

匹配 1
来源：{novel_name}（{material_id}）
  题材：{premise}
  结构骨架：
  第一卷「{title}」— {arc}  转折：{turning_point}
  第二卷「{title}」— {arc}  转折：{turning_point}
  ...

  与你的项目对比：{...}
  融合大纲：/material-apply {material_id} outline
```

**角色弧光级：**
```
角色弧光检索：{需求}

匹配 1
来源：{novel_name} — {character_name}
  定位：{role} / {archetype}
  核心驱动：{obsession}
  致命缺陷：{fatal_flaw}

  弧光轨迹：
  起点（ch{N}）：{state}
  转折（ch{N}）：{state}  触发：{trigger}
  终点（ch{N}）：{state}

  融合弧光：/material-apply {character_name} arc {你的角色名}
```

**节奏级：**
```
节奏模式检索：{需求}

来源：{novel_name}（{material_id}）

张力曲线：
ch001 ██░░░░░░░░  tension=2  [铺垫] 减速
ch002 ████░░░░░░  tension=4  [升级] 加速
ch003 ████████░░  tension=8  [高潮] 爆发
...

节奏模式摘要：{开局/中段/高潮前/高潮后}
场景编排：{对决→日常→密谋→对决}

  融合节奏：/material-apply {material_id} rhythm-pattern {章节范围}
```

## 注意事项

- 本 skill 只负责搜索，融合用 `/material-apply`，管理用 `/material-manage`
- 检索路径固定为 `../novel-material/scripts/search.py`
- SQLite 不可用时，回退读取 `scenes_index.yaml`
