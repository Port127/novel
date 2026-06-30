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
      description: 基础阶段，可使用基础法术
      capabilities: [基础法术, 强身健体]
    - name: 筑基期
      description: 寿元增加，可御剑
      capabilities: [御剑飞行, 辟谷]
  rules:
    - rule: 灵气浓度决定修炼速度
      implications: 洞天福地成为宗门必争之地
  limitations:
    - limitation: 渡劫
      consequences: 失败会灰飞烟灭
```

---

## 都市言情

### 必需要素
- **core_rules**：时代铁律、社会法则、行业规矩
- **locations**：城市、学校、公司、标志性地点
- **factions**：圈子、阶层、公司派系

### 设计重点
- 时代细节要准确写入 setting_period（如物价、科技、流行文化）
- 地点要有真实感（可虚构但要有原型）
- 社交与行业规则写入 core_rules

### 模板
```yaml
setting_period: "2009年，智能手机刚普及，微博兴起，房价开始上涨"
core_rules:
  - rule: 娱乐圈潜规则
    implications: 新人必须寻找靠山，否则寸步难行
  - rule: 阶层壁垒
    implications: 寒门难出贵子，圈层极度固化
locations:
  - name: 合工大
    type: 城市
    description: 主场景，校园日常，周边有小吃街
factions:
  - name: 沪圈资本
    type: 组织
    stance: 反派
    description: 垄断娱乐圈资源的资本巨头
```

---

## 系统文

### 必需要素
- **power_system**：系统机制（把系统视作一种独特的力量体系）
- **core_rules**：系统的底层逻辑、任务与惩罚机制
- **lore**：系统起源（如有）、特殊道具

### 设计重点
- 系统底层逻辑要自洽写入 core_rules（为什么有系统？限制是什么？）
- 系统的升级与奖励机制可以写进 power_system 的 ranks 和 rules
- 奖励要有吸引力但不能太无敌

### 模板
```yaml
power_system:
  name: 全能系统
  type: 系统
  ranks:
    - name: LV1 菜鸟
      description: 开启日常任务模块
    - name: LV2 达人
      description: 开启商城模块
  rules:
    - rule: 积分通过完成任务获得
      implications: 必须不断卷任务才能维持消耗
core_rules:
  - rule: 惩罚机制
    implications: 任务失败会扣除属性点
  - rule: 权限限制
    implications: 严禁向原住民透露系统存在，违者抹杀
lore:
  artifacts:
    - name: 新手大礼包
      type: 消耗品
      description: 包含基础技能和100积分
```

---

## 悬疑推理

### 必需要素
- **core_rules**：犯罪法则、作案手法限制、破案逻辑
- **factions**：调查方（警方/侦探）、反派组织（嫌疑人池）
- **locations**：案发地点、密室

### 设计重点
- 核心规则要包含推理逻辑（例如：不存在超自然力量，所有线索必须指向物理证据）
- 嫌疑人动机要合理（放入 factions 或人物卡中）

---

## 品类适配检查清单

| # | 检查项 | 通过标准 |
|---|--------|----------|
| 1 | 品类识别正确 | 已根据 scout_report.yaml 选择框架 |
| 2 | 必需要素完整 | required 中的元素都已设计 |
| 3 | 自洽性 | 各要素之间没有矛盾 |
| 4 | 服务于剧情 | 设定能支撑后续剧情发展 |
