---
name: project-reindex
description: 重建当前项目的所有交叉索引、角色/设定反向引用和项目地图，修复漂移和遗漏。
when_to_use: 用户觉得索引可能过期、新增了大量内容后想整理、或定期维护时。
argument-hint: "[--dry-run]"
arguments: ""
---

# 任务

扫描当前项目的全部角色、设定、关系和章节数据，重建交叉索引并刷新 PROJECT_MAP.md。

> **交叉引用唯一维护者**：角色的 `cross_references` 与设定的 `character_links` 之间的双向引用统一由本 skill 维护。CRUD skill（`/character-add`、`/setting-add` 等）只写自己领域的文件，不负责跨领域同步。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 如果为空，提示：`请先使用 /novel-init 创建项目`

## 输入参数

- `--dry-run`：只报告差异，不实际修改文件

## 执行步骤

### 1. 收集全量数据

读取以下文件，构建内存中的全量数据模型：

| 数据源 | 文件 | 提取内容 |
|--------|------|---------|
| 角色 | `characters/*.yaml`（排除 `character_index.yaml`、`relations.yaml`、`relation_events.yaml`） | name、role、abilities 中的设定关联、relations |
| 设定 | `worldbuilding/entries/*.yaml`（排除 `_template.yaml`） | id、name、category、status、character_links、setting_links |
| 关系 | `characters/relations.yaml` | 所有 pair |
| 章节 | `chapters/index.yaml` + `chapters/**/*.yaml` | 章节编号、involved_characters、tags |
| 情节 | `plot/plot_index.yaml` + `plot/outline.yaml` | 情节节点、关联角色 |
| 时间线 | `timeline/main.yaml` | 事件、关联角色 |

### 2. 推导交叉引用关系

对每个角色，基于以下规则推导 `cross_references.related_settings`：

- 角色的 `abilities` 中提到的设定 id → 直接关联
- 角色的 `backstory` 中提到的设定名称 → 直接关联
- 世界观 entry 的 `character_links` 中包含该角色 → 反向关联
- 角色的 `cross_references.related_factions` 根据势力 entry 的 `character_links` 推导

对每个设定 entry，基于以下规则推导 `character_links` 补全：

- 角色的 `cross_references.related_settings` 中包含该设定 → 反向添加
- 角色的 `backstory` 或 `abilities` 中提到该设定名称 → 添加

### 3. 对比差异

将推导结果与现有文件内容对比，生成差异报告：

```
📊 交叉索引扫描报告

角色交叉索引：
  赵宋.yaml: ✅ 一致（14 settings, 5 factions）
  沈夜.yaml: ⚠️ 缺失 rule_003（新增设定未同步）
  ...

设定反向引用：
  rule_006.yaml: ✅ 一致（6 characters）
  power_001.yaml: ⚠️ 缺失 纪微（新建角色未同步）
  ...

索引文件：
  character_index.yaml: ⚠️ 缺少 [新角色名]
  worldbuilding.yaml: ✅ 一致
  ...

统计：
  角色总数: 10 → 12（+2）
  设定总数: 19 → 22（+3）
  需更新文件: 8
```

如果 `--dry-run`，到此结束，不写入。

### 4. 写入更新

对每个有差异的文件执行更新：

**角色文件更新规则**：
- 如果 `cross_references` 字段不存在 → 在 `appearance_stats:` 前插入完整块
- 如果 `cross_references` 已存在 → 仅追加缺失的条目，不删除已有条目
- `key_chapters` 和 `related_plot_nodes` 从章节和情节数据自动填充

**设定文件更新规则**：
- 仅追加缺失的 `character_links` 条目，不删除已有条目
- `setting_links` 不自动修改（依赖手动设定间关联）

**索引文件更新规则**：
- `character_index.yaml`：与 `characters/*.yaml` 文件列表对齐
- `worldbuilding.yaml` 的 `entries` 列表：与 `entries/*.yaml` 文件列表对齐
- `state.yaml`：仅刷新 `project.updated`，不维护计数字段（计数由读取方按需从源文件计算）

### 5. 刷新 PROJECT_MAP.md

重新生成 `PROJECT_MAP.md`，基于当前数据更新：
- 进度总览表
- 角色地图（核心组 + 特例）
- 世界观设定地图
- 关系网络
- 六季节奏概览
- 下一步行动

### 6. 同步 Cursor Rules（项目上下文）

如果 `{current_path}/.novel/rules/` 存在：
- 读取项目数据，用最新统计信息刷新 `context.md`
- 将更新后的 `context.md` 同步到 `.cursor/rules/novel-project-context.mdc`

## 输出格式

```
✅ 项目索引重建完成

📊 变更摘要：
   角色交叉索引更新：{{count}} 个文件
   设定反向引用更新：{{count}} 个文件
   索引文件刷新：{{list}}
   PROJECT_MAP.md：已重建
   Cursor Rules：已同步

⚠️ 需要人工确认：
   {{如有无法自动推导的关联，列出}}

下一步：
   /consistency-check    全面一致性检查
   /novel-status         查看更新后的状态
```

## 注意事项

- 只追加不删除：避免误删人工维护的精确关联
- 推导关系标注来源：自动推导的条目加 `# auto-indexed` 注释，便于区分
- 大项目（50+ 角色）时分批处理，每批完成后报告进度
- 如果角色文件中没有 `cross_references` 字段，视为首次索引，完整创建
