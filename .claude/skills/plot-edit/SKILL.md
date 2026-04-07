---
name: plot-edit
description: 编辑已有大纲节点，支持修改内容、调整顺序、合并拆分，内置影响分析防止破坏已写章节。
when_to_use: 用户想修改一个大纲节点的内容、位置或结构，而不是添加新节点
argument-hint: "[节点标识] [修改内容]"
arguments: node changes
---

# 任务

编辑 `plot/outline.md` 和 `plot/outline.yaml` 中的已有大纲节点。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/plot/outline.md`
3. 读取 `{current_path}/plot/outline.yaml`（若存在）
4. 读取 `{current_path}/chapters/index.yaml`（用于影响分析）

## 输入参数

- `$0` (node): 节点标识（如 `第5章`、`inciting`、`act1_climax`）
- `$1+` (changes): 修改内容描述

支持的修改格式：
- `/plot-edit 第5章 事件改为：主角发现旧友已投敌`
- `/plot-edit inciting 冲突升级：增加误杀元素`
- `/plot-edit midpoint --move-after act1_climax`
- `/plot-edit 第3章 --merge 第4章`
- `/plot-edit act2_trials --split 两个独立试炼`

## 执行步骤

### 1. 定位节点

在 `outline.md` 和 `outline.yaml` 中定位目标节点：
- 按节点 ID 匹配（如 `inciting`、`midpoint`）
- 按章节号匹配（如 `第5章`）
- 按标题模糊匹配

若找不到，列出现有节点供用户选择。

### 2. 影响分析

**检查该节点是否关联已写章节：**

a) 从 `chapters/index.yaml` 中查找与此节点关联的章节
b) 检查关联章节的状态

| 章节状态 | 允许修改大纲 | 处理方式 |
|---------|------------|---------|
| `idea` / `outline` | 是 | 直接修改 |
| `draft` | 是，但需提示 | 提示用户该章已在写 |
| `revise` / `final` | 需确认 | 影响分析 + 确认 |
| `published` | 需强制确认 | 影响分析 + 双重确认 |

如果关联章节处于 `revise` 以上状态：

```
⚠️ 大纲修改影响分析

📖 节点：{{node_id}} — {{node_title}}

关联章节：
  - {{chapter_id}}（状态：{{status}}）
  - {{chapter_id}}（状态：{{status}}）

修改内容：{{changes}}

⚠️ 以上章节已进入 {{status}} 状态，修改大纲可能导致：
  - 章节内容与大纲不一致
  - 伏笔/钩子安排失效
  - 角色行为逻辑断裂

建议：先完成已写章节的收束，再调整大纲。
确认仍要修改？(Y/N)
```

### 3. 执行变更

**内容修改：**
- 更新 `outline.md` 中对应节点的文本
- 更新 `outline.yaml` 中对应节点的结构化数据（summary、status 等）

**位置调整（--move-after / --move-before）：**
- 在 `outline.md` 中移动节点文本块
- 在 `outline.yaml` 中调整节点顺序
- 检查移动后时间线是否仍然合理

**合并（--merge）：**
- 将两个节点合并为一个
- 更新 `outline.md` 和 `outline.yaml`
- 更新 `plot_index.yaml`（若有条目）

**拆分（--split）：**
- 将一个节点拆分为多个
- 自动分配新 ID
- 更新所有相关文件

### 4. 更新关联

- 更新 `plot/plot_index.yaml`（若存在条目）
- 如果修改影响了 `foreshadowing`（伏笔），更新 `outline.yaml` 的 `foreshadowing` 部分
- 如果修改影响了 `pacing_curve`，更新对应条目

### 5. 更新状态

更新 `{current_path}/.novel/state.yaml`：
- `plot.chapters`：大纲节点计数（若有增减）
- `project.updated`：今天日期

## 输出格式

```
✅ 大纲节点已更新

📖 节点：{{node_id}} — {{node_title}}
📝 修改内容：
   - {{变更描述}}

📄 已更新：
   - plot/outline.md
   - plot/outline.yaml

{{如有关联章节：}}
⚠️ 关联章节提醒：
   - {{chapter_id}}（{{status}}）— 建议重新检查一致性

下一步：
   /plot-review                     审查修改后的大纲
   /consistency-check               检查修改是否引入矛盾
   /plot-edit [节点]               继续编辑其他节点
```

## 注意事项

- 修改已有节点比添加新节点风险更高，始终做影响分析
- `published` 状态的关联章节需要双重确认
- 合并/拆分操作不可逆，执行前向用户展示预览
- 调整节点顺序时自动检查时间线逻辑
- 大段内容修改建议引导用户直接编辑 `outline.md` 文件
