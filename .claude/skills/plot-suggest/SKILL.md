---
name: plot-suggest
description: AI生成情节建议，支持卡点突破、钩子设计、悲剧/BE、爽点升级与关系推进。用于用户卡文、需要反转或想让剧情更有冲击力时。
when_to_use: 用户卡文，或想设计反转、钩子、悲剧/BE、爽点升级、关系推进
argument-hint: "[问题描述]"
arguments: problem
---

# 任务

根据当前进度和设定，AI生成情节建议。

## 前置检查

1. 读取 `.current.yaml` 获取 `current_path`

## 输入参数

- `$0+` (problem): 卡点描述或需求

示例：
- `/plot-suggest 第10章卡住了`
- `/plot-suggest 张三和赵六的关系怎么发展`
- `/plot-suggest 需要一个反转情节`
- `/plot-suggest 想写一个重逢即死的BE`
- `/plot-suggest 这一卷的钩子和爽点都不够`

## 执行步骤

### 1. 收集上下文

读取以下文件了解项目状态：
- `{current_path}/plot/outline.md` - 当前进度
- `{current_path}/characters/*.yaml` - 角色设定
- `{current_path}/worldbuilding/setting.md` - 世界观
- `{current_path}/timeline/main.yaml` - 时间线
- `{current_path}/.novel/state.yaml` - 项目信息

### 2. 分析需求

根据用户描述，识别需求类型：
- 卡点突破
- 关系发展
- 情节转折
- 冲突设计
- 钩子设计
- 悲剧 / BE
- 爽点升级 / 反派升级

### 3. 素材库案例检索（可选）

如果 `../novel-material/data/material.db` 存在，根据需求类型检索相似案例：

```bash
# 卡点/转折 → 找类似结构的场景
python ../novel-material/scripts/search.py scene \
  --plot-function {对应功能，如 转折 / 高潮 / 钩子} \
  --conflict {对应冲突类型} --limit 5

# 关系推进 → 找类似关系动态
python ../novel-material/scripts/search.py scene \
  --relationship {对应关系} --interaction {对应互动} --limit 5

# 悲剧/BE → 找催泪技法
python ../novel-material/scripts/search.py scene \
  --reader-effect 催泪 --emotion 悲伤 --limit 5
```

将检索到的案例摘要作为「参考案例」附在建议中——借机制和节奏，不借表达。

如果素材库不可用，跳过此步骤。

### 4. 生成建议

提供2-3个可选方案，每个方案包含：
- 情节概述
- 推进作用
- 冲突点
- 代价 / 误判 / 信息差
- 钩子 / 伏笔机会

生成时优先使用以下原则：
- 用户要催泪或 BE 时，优先考虑“差一步”“错位等待”“临终误判”“反差脆弱”
- 用户要爽点时，优先考虑“信息差 + 明确代价 + 反制风险”，避免纯平推开挂
- 用户要钩子时，优先考虑“谎言”“口误”“巧合”“异常意象”，避免硬塞反转
- 老套路可借，但要换立场、顺序、代价或结果，避免直接套模板

## 输出格式

```
💡 情节建议

当前进度：{{progress}}
角色状态：{{character_status}}

---

## 方案A：{{标题}}

{{情节概述}}

- 推进：{{如何推进故事}}
- 冲突：{{冲突点}}
- 代价：{{代价、误判或信息差}}
- 钩子：{{可埋的钩子或伏笔}}

## 方案B：{{标题}}

{{情节概述}}

- 推进：{{如何推进故事}}
- 冲突：{{冲突点}}
- 代价：{{代价、误判或信息差}}
- 钩子：{{可埋的钩子或伏笔}}

---

🎯 建议：{{推荐方案及理由}}

选择方案：/plot-add [章节] [内容]
```

## 注意事项

- 建议要符合已有设定
- 提供多个选项
- 说明优劣
- 优先借“机制”和“节奏”，不要照搬外部表达或桥段表层