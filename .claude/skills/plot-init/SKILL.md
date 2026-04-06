---
name: plot-init
description: 初始化剧情大纲结构
when_to_use: 用户想要规划小说的整体结构
argument-hint: "[结构类型]"
arguments: structure
---

# 任务

初始化剧情大纲结构。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`

## 输入参数

- `$0` (structure): 结构类型，可选值：
  - `三幕式`（默认）
  - `英雄之旅`
  - `五段式`
  - `自定义`

## 执行步骤

### 1. 检查现有大纲

读取 `{current_path}/plot/outline.md`。

如果已有内容，询问是否覆盖。

### 2. 生成叙述性大纲框架

根据结构类型生成框架，写入 `{current_path}/plot/outline.md`。

### 3. 初始化结构化大纲

写入 `{current_path}/plot/outline.yaml`（若不存在）：

```yaml
premise: ""
theme: []
tone: []
structure: []
timelines: []
foreshadowing: []
pacing_curve: []
```

### 4. 初始化情节索引

写入 `{current_path}/plot/plot_index.yaml`（若不存在）：

```yaml
entries: []
```

### 5. 更新项目状态

更新 `state.yaml` 的 `plot.structure`。

## 结构模板

**三幕式：**
```markdown
# 大纲

## 第一幕：起（约25%）

### 开场
<!-- 日常世界，主角出场 -->

### 引发事件
<!-- 打破平衡的事件 -->

### 第一幕高潮
<!-- 主角踏上旅程 -->

---

## 第二幕：承转（约50%）

### 试炼
<!-- 挑战与成长 -->

### 中点
<!-- 故事中点的重大转折 -->

### 危机
<!-- 最低谷，最大挑战 -->

---

## 第三幕：合（约25%）

### 高潮
<!-- 最终对决 -->

### 结局
<!-- 新的平衡 -->
```

**英雄之旅：**
```markdown
# 大纲

## 第一阶段：启程
1. 平凡世界
2. 冒险召唤
3. 拒绝召唤
4. 遇见导师
5. 跨越第一道门槛

## 第二阶段：启蒙
6. 试炼、盟友、敌人
7. 接近最深的洞穴
8. 磨难
9. 奖赏
10. 返回之路

## 第三阶段：归来
11. 复活
12. 携带万灵药归来
```

## 输出格式

```
✅ 剧情结构初始化完成

📐 结构：$0
📄 文件：plot/outline.md

已生成框架，接下来：
   /plot-add [章节] [内容]  添加情节
   /plot-suggest [描述]     获取AI建议
```

## 注意事项

- 结构可随时调整
- 支持混合结构
- 可导入现有大纲