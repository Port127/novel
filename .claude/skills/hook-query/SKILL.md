---
name: hook-query
description: 查询伏笔/钩子状态，支持按等级、状态、截止时间筛选，输出列表和时间轴。
when_to_use: 用户想知道当前有哪些未回收的伏笔、哪些即将过期、或查看钩子全景
argument-hint: "[--level major] [--status planted] [--near ch015]"
arguments: ""
---

# 任务

查询 `plot/outline.yaml` 的 `foreshadowing` 列表，按条件筛选并可视化输出。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/plot/outline.yaml`
3. 读取 `{current_path}/chapters/index.yaml`（用于判断当前进度）

## 输入参数

所有参数可选，不带参数则输出全部钩子概览。

- `--level`: 筛选等级，`major` / `minor` / `micro`
- `--status`: 筛选状态，`planted` / `pending` / `recovered` / `abandoned`
- `--near [章节ID]`: 查找截止在该章节前后 5 章内的钩子
- `--overdue`: 只看已过截止但未回收的钩子
- `--chapter [章节ID]`: 查看某章埋设或回收的所有钩子
- `--timeline`: 输出时间轴可视化

## 执行步骤

### 1. 加载并筛选

从 `outline.yaml` 加载 `foreshadowing` 列表，按参数筛选。

### 2. 自动状态刷新

在输出前，根据当前写作进度自动判断 status 是否需要更新提示（不修改文件）：

- 已 `planted` 且当前章节已超过 `recovery_deadline.value` → 标记为"逾期"
- 已 `planted` 且当前章节距 `recovery_deadline.value` 不超过 3 章 → 标记为"即将到期"

### 3. 输出结果

## 输出格式

### 列表模式（默认）

```
🪝 钩子追踪（共 {{total}} 条，筛选后 {{count}} 条）

📊 统计：major {{N}} | minor {{N}} | micro {{N}}
📊 状态：planted {{N}} | pending {{N}} | recovered {{N}} | abandoned {{N}}

---

[f001] 赵宋手背的疤痕 ⭐ major
  📖 埋设：ch003 | 回收：TBD
  ⏰ 截止：ch015（还剩 5 章）
  📝 {{plant_description}}

[f002] 室友的异常电话 minor
  📖 埋设：ch005 | 回收：TBD
  ⏰ 截止：无
  📝 {{plant_description}}

[f003] 桌上的凉茶 micro ✅ recovered
  📖 埋设：ch002 | 回收：ch008
  📝 {{payoff_description}}
```

### 时间轴模式（--timeline）

```
🪝 钩子时间轴

ch001  ch003  ch005  ch008  ch010  ch012  ch015  ch020
  |      |      |      |      |      |      |      |
  |    [f001]━━━━━━━━━━━━━━━━━━━━━━━▶ ⏰ ch015
  |      |    [f002]━━━━━━━━━━━━━━━━━━━━━━━━━▶ ...
  |    [f003]━━━━━━[✅]
  |      |      |      |      |      |      |      |

━━━ = planted/pending    [✅] = recovered    ⏰ = deadline
当前进度：ch012 ◀
```

### 逾期模式（--overdue）

```
⚠️ 逾期未回收钩子（{{count}} 条）

[f001] 赵宋手背的疤痕 ⭐ major — 已超期 3 章！
  ⏰ 截止：ch015（硬截止）
  💡 建议：/hook-resolve f001 --recover ch018 或 --extend ch020

[f005] 某角色的暗示 minor — 已超期 1 章
  ⏰ 截止：ch010（软截止）
  💡 建议：/hook-resolve f005 --extend ch015 [原因]
```

## 注意事项

- 查询是只读操作，不修改任何文件
- 自动状态刷新只在输出中标注，不写回 `outline.yaml`
- 时间轴模式用章节号做 X 轴，ASCII 可视化
- 如果 `foreshadowing` 列表为空，提示"暂无登记的钩子，使用 `/hook-add` 开始追踪"
