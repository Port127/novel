---
name: material-apply
description: 将参考素材融合到当前项目（场景级/大纲级/角色弧光级/节奏级）
when_to_use: 用户搜到参考素材后，想把技法、结构、弧光或节奏融合到自己的写作中
argument-hint: "[来源ID] [模式] [目标]"
arguments: source_id mode target
---

# 任务

将素材库的参考素材融合到当前项目。核心原则：**借机制不借表达，借骨架不借皮肉。**

## 前置检查

1. 确认 `../novel-material/` 目录存在
2. 读取 `.current.yaml` 获取 `current_path`

## 输入参数

```bash
/material-apply {source_id} {mode} [{target}]
```

- `source_id`: 场景 ID（如 `ch0042_s03`）、素材 ID（如 `nm_novel_xxx`）、或素材中的角色名
- `mode`: 融合模式（见下表）
- `target`: 融合目标（章节 ID、角色名等，部分模式可省略）

上一次 `/material-search` 检索结果可用序号代替：`/material-apply #1 draft ch005`

### 融合模式

**场景级（source = 场景 ID）：**

| mode | 做什么 | target | 写入位置 |
|------|--------|--------|---------|
| `draft` | 提取技法和场景结构，融入章节 | 章节 ID | `chapters/{id}.md` 写作备忘 |
| `plot` | 提取冲突结构、转折模式、钩子设计 | 大纲节点或章节范围 | `plot/outline.md` 批注 |
| `setting` | 提取世界观构建方法、规则设计模式 | 设定条目名或类别 | `worldbuilding/entries/` 参考 |
| `character` | 提取人物塑造技法（缺陷设计、对白区分） | 角色名 | 角色卡 notes |

**小说级（source = 素材 ID）：**

| mode | 做什么 | target | 写入位置 |
|------|--------|--------|---------|
| `outline` | 对比参考小说大纲结构，输出结构优化建议 | 自动 | `plot/outline.md` 批注 |
| `rhythm-pattern` | 分析参考小说节奏曲线，对比当前项目 | 章节范围（可选） | 节奏分析报告 |

**角色级（source = 素材中角色名）：**

| mode | 做什么 | target | 写入位置 |
|------|--------|--------|---------|
| `arc` | 对比参考角色弧光，输出弧光补强建议 | 当前项目角色名 | 角色卡 notes |

## 执行步骤

### 1. 读取参考数据

**场景级**（source = 场景 ID）：
从 `../novel-material/data/novels/{material_id}/scenes/{scene_id}.yaml` 读取全量标签和摘要。需要更大上下文时，同时读取前后相邻场景。

**小说级**（source = 素材 ID）：
- `outline` → 读取 `../novel-material/data/novels/{material_id}/outline.yaml`
- `rhythm-pattern` → 读取该小说全部场景的 `pacing`、`tension`、`plot_stage`、`plot_function`，按章节顺序聚合

**角色级**（source = 角色名）：
- 从 `characters.yaml` 读取角色完整数据（设定 + 心理画像 + 弧光）
- 从场景数据提取该角色出场的 `character_moment` 标签，构建弧光实证链

### 2. 读取当前项目对应上下文

| mode | 读取 |
|------|------|
| `draft` | 目标章节大纲、角色档案、前后章节 |
| `plot` | `outline.md` + `outline.yaml` 中对应节点 |
| `setting` | `worldbuilding/entries/` 相关条目 + `setting.md` |
| `character` | 目标角色的 `.yaml` 档案 |
| `outline` | `plot/outline.md` + `plot/outline.yaml` |
| `rhythm-pattern` | 目标范围内所有章节的大纲节点和张力标记 |
| `arc` | 目标角色的 `.yaml` 档案（含 `arc` 和 `current_state`） |

### 3. 生成融合建议

**draft 模式：** 开场技法 → 冲突升级节奏 → 对白技法 → 收尾钩子
**plot 模式：** 冲突类型和 stakes → plot_function 对齐 → 信息差结构
**setting 模式：** 世界观规则动态表现 → 环境叙事技法
**character 模式：** 缺陷外化 → 对白风格 → character_moment 分布

**outline 模式：** 全书结构对比 → 转折点分布 → 多线编排 → 各阶段节奏策略
**rhythm-pattern 模式：** 张力曲线对比 → 场景类型编排 → pacing 交替模式 → 高潮前蓄力模式
**arc 模式：** 弧光阶段对比 → 心理画像外化 → character_moment 分布 → 悲剧结构

### 4. 用户确认 → 写入

**场景级：**
- `draft` → 章节文件「写作备忘」区域
- `plot` → `outline.md` 对应节点批注
- `setting` → 设定条目 `plot_links` 补充
- `character` → 角色卡 `notes`

**小说级：**
- `outline` → `plot/outline.md` 批注区域
- `rhythm-pattern` → 输出报告，不写入文件

**角色级：**
- `arc` → 角色卡 `notes`

所有写入标注 `[参考来源: {novel_name} — {scene_title}]`。

### 5. 提示登记借鉴（可选）

```
是否登记借鉴来源？
   /inspiration-log {target_chapter} {material_id} 借鉴了{scene_title}的{融合维度}
```

## 输出格式

```
素材融合分析

参考：{novel_name} — {source_title}
融合目标：{mode} → {target}

参考摘要
> {summary}
关键标签：{tags}

融合建议

1. {建议维度}
   参考做法：{...}
   你的项目适配：{...}

2. {建议维度}
   ...

适配注意：{与当前项目不兼容的部分}

确认采纳？采纳后将写入 {目标文件}
```

## 注意事项

- 通常先运行 `/material-search` 找到参考，再用 `/material-apply` 融合
- 不复制数据到本项目，只提取机制和建议
- 所有写入都标注来源，方便追溯
- 融合后建议运行 `/inspiration-log` 登记
