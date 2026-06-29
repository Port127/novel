---
name: worldbuilding
description: 世界观设计。与 Agent 交互讨论力量体系、社会结构、基础规则。
---

# 世界观设计

交互式设计小说世界观，包括力量体系、社会结构、基础规则。

---

## 前置依赖

- 品类已选择（`settings/scout_report.yaml` 存在）

---

## 工作流程

### 1. 确认项目

运行 `novel list`，选择项目。

### 2. 品类适配

读取 `settings/scout_report.yaml`，基于品类推荐世界观框架：

| 品类 | 推荐框架 |
|------|---------|
| 玄幻 | 修炼等级体系、宗门势力、天材地宝 |
| 都市 | 社会阶层、商业规则、隐藏势力 |
| 系统文 | 系统规则、任务机制、奖励体系 |

### 3. 交互讨论

与用户逐步讨论：

**力量体系**：
- 等级划分
- 升级条件
- 战力表现

**社会结构**：
- 主要势力
- 势力关系
- 社会规则

**基础规则**：
- 世界运行的核心规则
- 禁忌/限制

### 4. 生成文件

Agent 直接生成 `settings/worldbuilding.yaml` 单文件，包含：
- school_info（学校信息）
- era_context（时代背景）
- university_life（大学生活）
- social_context（社会背景）
- foreknowledge_advantages（先知优势）

### 5. 展示与调整

展示世界观概览。询问是否调整。

---

## 输出文件

- `settings/worldbuilding.yaml`

## 参考

- 模板: `templates/default/settings/`
