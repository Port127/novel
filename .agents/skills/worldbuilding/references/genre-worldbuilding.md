# 品类×世界观适配矩阵

> **用途**：Phase 1 根据品类加载对应框架。

---

## 玄幻修仙

### 必需要素
- **power_system**：修炼等级（练气→筑基→金丹→元婴→化神...）、功法分类、战斗表现
- **factions**：宗门/家族/势力（≥3 个）、势力关系、地盘划分
- **locations**：秘境、城市、宗门所在地

### 设计重点
- 力量等级必须清晰，不能后期崩坏
- 升级条件要明确（资源/悟性/机缘）
- 宗门层级（外门/内门/核心/长老/掌门）

### 模板
```yaml
power_system:
  name: 修仙体系
  type: 修炼
  ranks:
    - name: 练气期
      capabilities: 基础法术
      breakthrough: 灵石+悟性
    - name: 筑基期
      capabilities: 御剑飞行
      breakthrough: 筑基丹
  rules: 灵气浓度影响修炼速度
  limitations: 渡劫失败会陨落
```

---

## 都市言情

### 必需要素
- **era_details**：时代背景（2009/2015/现代...）、社会特征、科技水平
- **locations**：城市、学校、公司、标志性地点
- **social_rules**：社交规则、阶层差异、行业规则

### 设计重点
- 时代细节要准确（物价、科技、流行文化）
- 地点要有真实感（可虚构但要有原型）
- 社交规则要符合现实逻辑

### 模板
```yaml
era_details:
  year: 2009
  characteristics:
    - 智能手机刚普及
    - 微博兴起
    - 房价开始上涨
locations:
  - name: 合工大
    type: 大学
    description: 主场景，校园日常
```

---

## 系统文

### 必需要素
- **system_rules**：系统名称、激活条件、功能
- **quest_mechanics**：任务类型、奖励机制、惩罚机制
- **reward_system**：奖励分类、升级曲线

### 设计重点
- 系统规则要自洽（为什么有系统？限制是什么？）
- 任务设计要有层次感（日常/主线/隐藏）
- 奖励要有吸引力但不能太无敌

### 模板
```yaml
system_rules:
  name: 全能系统
  activation: 意外触发
  functions: [任务发布, 奖励发放, 技能兑换]
quest_mechanics:
  daily_quests: 简单任务，稳定奖励
  main_quests: 推动剧情，高奖励
  hidden_quests: 触发条件特殊，稀有奖励
reward_system:
  currency: 积分
  exchange: 技能/道具/属性点
```

---

## 悬疑推理

### 必需要素
- **crime_rules**：犯罪类型、作案手法、破案逻辑
- **investigation_procedures**：调查流程、证据链、推理方法
- **suspect_pool**：嫌疑人列表、动机、不在场证明

### 设计重点
- 推理逻辑要严密
- 证据链要完整
- 嫌疑人动机要合理

---

## 品类适配检查清单

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 品类识别正确 | 已根据 scout_report.yaml 选择框架 |
| 2 | 必需要素完整 | required 中的元素都已设计 |
| 3 | 自洽性 | 各要素之间没有矛盾 |
| 4 | 服务于剧情 | 设定能支撑后续剧情发展 |
