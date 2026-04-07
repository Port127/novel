---
name: worldbuilding-review
description: 审查世界观设定是否自洽、真实、可支撑剧情，并识别规则缺口、设定堆积、资源分配失衡与代价缺失。用于用户想优化世界观、补足设定支撑，或在推进大纲前做一次设定体检。
when_to_use: 用户已有世界观草稿，想补强规则、势力、地理、真实感或设定与剧情的咬合度
argument-hint: "[优化重点]"
arguments: focus
---

# 任务

对现有世界观进行结构化审查，并给出能直接反馈到 `worldbuilding/setting.md` 与 `worldbuilding/worldbuilding.yaml` 的优化建议。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`
2. 读取 `{current_path}/worldbuilding/setting.md`
3. 若存在，读取 `{current_path}/worldbuilding/worldbuilding.yaml`
4. 若存在，读取 `{current_path}/worldbuilding/entries/*.yaml`（设定集条目）
5. 读取 `{current_path}/plot/outline.md`，检查设定是否服务主线剧情
6. 若存在，读取 `{current_path}/timeline/main.yaml`
7. 若存在，读取 `{current_path}/ingestion_brief.md`（对照素材消化摘要中的规则缺口）

## 输入参数

- `$0+` (focus): 可选优化重点，如“力量体系不清”“势力关系混乱”“设定很多但不好用”

## 执行步骤

### 1. 提取核心设定

识别以下内容：

- 时代背景与故事常态
- 世界规则与禁忌
- 力量体系 / 科技体系 / 社会规则
- 主要势力、地理、历史与术语
- 生活层细节，如物价、风俗、职业习惯、地方奇闻

### 2. 审查设定质量

重点检查：

- 核心规则是否说得清、能被角色实际使用
- 力量 / 金手指 / 技术体系是否有明确代价、限制或失手风险
- 重要冲突是否有设定支撑
- 主要地点与势力是否足够承载剧情推进
- 历史与世界规则是否会与时间线冲突
- 是否存在大量“展示型设定”但没有剧情用途
- 是否缺少让世界显得真实的生活层纹理
- 地图与资源分配是否合理，避免小地图里堆满顶级人物、顶级势力和顶级机缘

### 3. 审查设定依赖与生命周期

如果存在 `entries/*.yaml` 条目，额外检查：

- **依赖完整性**：`setting_links` 中引用的目标设定是否存在，是否已废弃
- **循环依赖**：A depends_on B, B depends_on A 的循环
- **孤立设定**：没有任何 `plot_links`、`character_links` 或 `setting_links` 的条目——可能是僵尸设定
- **tentative 堆积**：大量 tentative 条目未提升为 confirmed，提示用户清理
- **deprecated 残留**：已废弃但仍被其他 confirmed 设定引用的条目

### 4. 审查设定与剧情咬合度

重点检查：

- 大纲关键事件是否依赖尚未定义的规则
- 主角目标与世界阻力是否匹配
- 反派/势力行为是否有规则基础
- 世界观是否自然制造冲突与代价
- 设定是否能自然提供信息差、压迫感或局势升级空间

### 5. 输出优化动作

给出 3-6 条按优先级排序的动作，要求：

- 区分“必须补的规则”和“可后补的细节”
- 指明建议写入 `setting.md` 还是 `worldbuilding.yaml`
- 优先补能直接支撑剧情的设定
- 若真实感不足，优先补可被角色实际感知的生活细节
- 若体系过强无趣，优先补代价、限制与反制手段

## 输出格式

```
🌍 世界观审查

当前判断：{{overall_status}}
关注重点：{{focus}}

✅ 已成形
- ...

⚠️ 主要问题
- ...

📊 设定集健康度
- 条目总数：{{total}}（confirmed: {{confirmed}} / tentative: {{tentative}} / deprecated: {{deprecated}}）
- 孤立设定：{{orphan_count}} 条
- 依赖问题：{{dependency_issues}}

🔧 优化动作（按优先级）
1. ...
2. ...
3. ...

建议下一步：
- /setting-edit [设定] --status confirmed   提升已验证的设定
- /pipeline-outline-polish {{focus}}
- /consistency-check
```

## 注意事项

- 优先补“对剧情有约束力”的规则，不堆百科式设定
- 设定建议要说明它服务哪段剧情或哪类冲突
- 若需要重写世界基本规则，先给变更预览再执行
- 不只追求高概念，也要补让读者信服的日常纹理与资源分配逻辑
- 建议每次 review 后提示用户将已验证的 tentative 设定提升为 confirmed
