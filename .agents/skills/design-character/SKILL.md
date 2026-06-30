---
name: design-character
description: 人设设计。与 Agent 交互设计主角、反派、配角，含爽感维度评估。
---

# design-character（人设设计）

> **用途**：设计小说人物，包括主角、反派、配角，并评估爽感维度。
> **前置条件**：`settings/scout_report.yaml` 存在（品类已确定）。
> **输出文件**：`settings/characters.yaml`

---

## 核心原则

1. **品类适配**：不同品类需要不同角色类型（玄幻需要反派，言情需要恋爱对象）。
2. **弧线驱动**：主角必须有清晰的起点→终点弧线，弧线上有关键转折点。
3. **反派即剧情**：反派的恶心程度决定打脸的爽感上限。
4. **爽感可量化**：打脸指数、CP感、反派恶心度——三维评估人设质量。
5. **关系成网**：角色不是孤立的，关系网络决定剧情张力。
6. **差异化至上**：遮住名字能分出谁在说话，差异化失败 = 角色设计失败。
7. **动机可推导**：角色的重大决策必须能从动机链推导，不能为剧情服务而失真。
8. **弱点让角色可信**：没有弱点的完美主角不可信，弱点让成长有意义。

---

## Phase 定义

### Phase 1：品类适配

**入口条件**：scout_report.yaml 存在
**目标**：根据品类加载对应角色框架，确定需要设计的角色类型

**步骤**：
1. 读取 `scout_report.yaml` 的 `genre` 和 `required_elements.characters`
2. 读取 `references/character-basics.md`，加载品类对应角色框架
3. 展示该品类需要设计的角色类型
4. 确认设计范围

**出口条件**：角色类型列表确定
**加载 References**：`character-basics.md`

**品类框架示例**：

| 品类 | 必需角色 | 可选角色 | 设计重点 |
|------|---------|---------|---------|
| 玄幻 | protagonist, villain | supporting_cast, rival, master | 主角逆袭弧线、反派层级 |
| 都市 | protagonist, love_interest | rival, best_friend | CP感、社会身份差 |
| 系统 | protagonist, supporting_cast | villain, system_npc | 系统交互、配角功能 |
| 言情 | protagonist, love_interest | rival, best_friend | 双弧线、CP化学反应 |
| 悬疑 | protagonist, antagonist | suspect_pool | 信息差、动机链 |

---

### Phase 2：主角设计

**入口条件**：角色类型已确认
**目标**：设计主角完整人设

**步骤**：
1. 读取 `references/protagonist-arc.md`
2. **三层标签反差人设**（参考 `references/character-basics.md`）：
   - **身份标签**（别人怎么看）：高冷学霸 / 街头混混 / 世家公子
   - **表现标签**（日常行为）：毒舌 / 话痨 / 沉默寡言
   - **内核标签**（关键时刻暴露）：自卑 / 偏执 / 善良
   - 层间反差即角色立体感
3. **九维深化**（参考 `references/character-design-methods.md`）：
   - 逐一填写九维人设框架，确保每维度都有具体内容
4. **动机链建立**（参考 `references/character-basics.md`）：
   - **起因**：角色经历了什么（必须具体、有画面、有情感冲击）
   - **意图**：表面意图与真实意图的区分
   - **约束**：外部约束（实力/资源/强敌）+ 内部约束（性格/道德/情感）
   - **风险**：失败代价 + 成功代价 + 道德代价
5. **语言风格档案**（7 维度，参考 `references/dialogue-mastery.md`）：
   - 口癖和惯用语、说话节奏、信息偏好、立场固定、身份影响措辞、性格影响语气、进度影响态度
   - **验证标准**：遮住名字后能分出谁在说话
6. **人物弧线设计**（参考 `references/protagonist-arc.md`）：
   - 起点状态 → 终点状态 → 关键转折点
   - 成长三阶段：小我 → 自我 → 他我
   - 情绪公式：满足 → 打击 → 怀疑 → 心痛 → 觉醒
7. 写入 characters.yaml 的 protagonist 条目

**出口条件**：主角人设完整（三层标签 + 九维 + 动机链 + 语言档案 + 弧线均已填写）
**加载 References**：`protagonist-arc.md`、`character-basics.md`、`character-design-methods.md`

#### Agent 调用：character-designer（可选增强）

如果项目已部署 character-designer agent（检查 `.agents/agents/character-designer.md` 是否存在），
可读取该文件内容，拼接以下参数后 spawn Agent 辅助主角深度设计：

- 项目根目录：{当前项目绝对路径}
- 任务类型：创作
- 查询参数：辅助主角三层标签设计、九维深化、语言风格档案建立
- 相关文件路径：settings/characters.yaml

如 agent 不可用，跳过此步，由主线程直接完成。

---

### Phase 3：反派设计

**入口条件**：`required_elements.characters` 包含 `villain` 或 `antagonist`
**目标**：设计反派完整人设

**步骤**：
1. 读取 `references/villain-design.md`
2. **反派层级设计**（按剧情需要逐层建立）：

| 层级 | 出场章节 | 功能 | 设计重点 |
|------|---------|------|---------|
| **小反派** | 1-5 章 | 制造即时冲突，被打脸提供爽感 | 恶心度要高，被打脸要爽 |
| **中等反派** | 10-30 章 | 有自己逻辑的对手 | 需要主角付出代价才能击败 |
| **大弧Boss** | 贯穿整卷 | 核心威胁 | 动机复杂，与主角有镜像关系 |
| **最终Boss** | 全书终极 | 终极阻碍 | 代表全书核心冲突的化身 |

3. **反派建立四要素**（参考 `references/villain-design.md`）：
   - **动机**：为什么与主角对立（必须有合理逻辑，不能为恶而恶）
   - **手段**：怎么对付主角（越恶心越好：羞辱/背叛/夺走/威胁）
   - **恶心度设计**：具体恶行（不是抽象"坏"），读者代入愤怒值 ≥ 7/10
   - **弱点**：最终被打败的原因（必须合理，不能强行降智）
4. **镜像关系设计**：
   - 大弧Boss 和最终Boss 应与主角形成镜像对照
   - 同一起点、不同选择、相反结局
5. **反派弧线**：
   - 反派的动机是否有层次（表面动机 vs 真实动机）
   - 反派是否有自己的成长/变化（不是静态的恶）
6. 写入 characters.yaml 的 antagonist 条目

**出口条件**：反派人设完整（动机 + 手段 + 恶心度 ≥ 7/10 + 弱点 + 镜像关系）
**加载 References**：`villain-design.md`

#### Agent 调用：character-designer（可选增强）

如果项目已部署 character-designer agent（检查 `.agents/agents/character-designer.md` 是否存在），
可读取该文件内容，拼接以下参数后 spawn Agent 辅助反派设计：

- 项目根目录：{当前项目绝对路径}
- 任务类型：创作
- 查询参数：辅助反派设计、镜像关系建立、恶心度优化
- 相关文件路径：settings/characters.yaml

如 agent 不可用，跳过此步，由主线程直接完成。

---

### Phase 4：配角与关系网络

**入口条件**：主角和反派已设计
**目标**：设计配角和关系网络

**步骤**：
1. 读取 `references/relationship-network.md`
2. **配角设计流程**：
   - 确定配角功能列表（导师/盟友/情报源/牺牲品/镜像对照/竞争者）
   - 每个配角必须有明确功能（推动剧情/衬托主角/提供信息），没有功能的不出场
   - 配角卡：角色功能 + 与主角关系 + 核心特质（1-2 个）+ 标志性特征 + 退场方式
3. **关系网络建立**（参考 `references/character-relations.md`）：

**四种关系类型**：

| 类型 | 功能 | 例子 | 设计要点 |
|------|------|------|---------|
| **冲突型** | 制造张力推动情节 | 宿敌、竞争对手 | 冲突必须有合理逻辑 |
| **联盟型** | 提供助力制造羁绊 | 战友、师徒 | 联盟内部可以有分歧 |
| **亲密型** | 制造软肋提供情感支点 | 恋人、家人、兄弟 | 亲密关系必须有考验 |
| **权威型** | 制造压力限制行动 | 师父、老板、监管者 | 权威可以是正面或负面 |

4. **好感度体系**（参考 `references/character-relations.md`「好感度体系」）：
   - 为亲密型和联盟型关系建立好感度阶段
   - 阶段示例：陌生 → 初识 → 熟悉 → 信任 → 亲密 → 生死之交
   - 每个阶段有对应的互动尺度和行为边界
5. **关系弧线设计**：
   - 每个重要关系至少经历一次考验
   - 关系必须有变化弧线（不能从头到尾一个状态）
   - 避免铁板一块（同盟内部可以有分歧，对立之中可以有惺惺相惜）
   - 关系变化必须有铺垫事件，不能"突然就成了好朋友"
6. 写入 characters.yaml 的 supporting/minor 条目
7. 绘制关系网络图（文字描述）

**出口条件**：配角 ≥ 3 个，关系网络已建立（四种类型 + 好感度 + 弧线）
**加载 References**：`relationship-network.md`、`character-relations.md`

---

### Phase 5：爽感评估与落盘

**入口条件**：所有必需角色已设计
**目标**：评估爽感三维，生成 characters.yaml 并验证

**步骤**：
1. 读取 `references/cool-factor-guide.md`
2. 评估三维爽感：
   - 打脸指数（face-slap index）
   - CP感（chemistry）
   - 反派恶心度（disgust level）
3. 如任一维度 < 6/10，给出调整建议
4. 汇总所有人设，展示给用户确认
5. 写入 `settings/characters.yaml`
6. 运行 `scripts/check-characters.js` 验证
7. 清理 `_progress.md`

**出口条件**：characters.yaml 已生成，爽感三维均 ≥ 6/10，通过完整性检查
**加载 References**：`cool-factor-guide.md`

---

## 质量门禁

### 角色设计质量检查

- **品类感知检查**：读取 `scout_report.yaml` 的 `required_elements.characters`，检查必需角色类型是否齐全
- **深度检查**：主角/反派必须有 psychology + arc；配角至少需要 traits + description
- **爽感检查**：打脸指数/CP感/恶心度 三维均需 ≥ 6/10
- **差异化检查**：遮住名字能分出谁在说话（语言风格档案 7 维度验证）
- **动机链检查**：角色的重大决策是否能从动机链推导
- **关系检查**：每个重要关系是否有考验、有弧线、不突然变化
- check-characters.js 自动执行以上检查

---

## 断点恢复

**状态文件**：`_progress.md`
**格式**：同 scout-topic
**恢复逻辑**：跳到最后一个 in_progress 的 Phase

---

## 输出文件

- `settings/characters.yaml`：人物设定

---

## References 索引

| Phase | References | 用途 |
|-------|-----------|------|
| 1 | character-basics.md | 基础角色设计方法论 + 品类适配 |
| 2 | protagonist-arc.md, character-basics.md, character-design-methods.md | 主角设计（三层标签 + 九维深化 + 动机链 + 语言档案 + 弧线） |
| 3 | villain-design.md | 反派设计（层级 + 四要素 + 镜像关系） |
| 4 | relationship-network.md, character-relations.md | 配角 + 关系网络（四种类型 + 好感度 + 弧线） |
| 5 | cool-factor-guide.md | 爽感三维评估 |

---

## 下一步

characters.yaml 生成后，可进入：
- `/design-outline`：大纲设计（人设驱动剧情）
- `/design-chapters`：章节设计

---

## 角色设计常见错误速查

| 错误类型 | 表现 | 修正方法 | 参考 |
|---------|------|---------|------|
| 纸片人 | 角色只有身份标签，无内核反差 | 用三层标签法补齐反差 | character-basics.md |
| 动机模糊 | 角色的重大决策无法从动机推导 | 重新建立动机链（起因→意图→约束→风险） | character-basics.md |
| 千人一面 | 遮住名字分不出谁在说话 | 用 7 维度语言档案差异化 | dialogue-mastery.md |
| 反派降智 | 反派为恶而恶，动机不合理 | 重新设计反派动机和镜像关系 | villain-design.md |
| 关系突变 | "突然就成了好朋友" | 补充铺垫事件和好感度阶段 | character-relations.md |
| 完美主角 | 主角无弱点，不可信 | 添加致命弱点和道德困境 | protagonist-arc.md |
| 配角空转 | 配角无功能，出场无意义 | 删除或重新定义功能 | relationship-network.md |
| 好感度失控 | 互动尺度不匹配关系阶段 | 按好感度体系调整互动边界 | character-relations.md |

---

## 角色档案输出格式

```yaml
# characters.yaml 示例结构
protagonist:
  name: 角色名
  gender: 性别
  role: protagonist
  identity_tags: [身份标签1, 身份标签2]
  appearance_tags: [表现标签1, 表现标签2]
  core_tags: [内核标签1, 内核标签2]
  appearance: 外貌特征
  personality: [trait1, trait2, trait3]
  psychology:
    flaw: 致命弱点
    obsession: 执念
    soft_spot: 软肋
    misjudgment: 误判
  motivation_chain:
    cause: 起因（具体事件）
    surface_intent: 表面意图
    true_intent: 真实意图
    constraints: [外部约束, 内部约束]
    risks:
      failure_cost: 失败代价
      success_cost: 成功代价
      moral_cost: 道德代价
  arc:
    start_state: 起点状态
    end_state: 终点状态
    turning_points: [转折点1, 转折点2]
  language_profile:
    catchphrase: 口头禅
    speech_rhythm: 说话节奏
    info_preference: 信息偏好
    stance: 立场角度
    identity_influence: 身份影响措辞
    personality_influence: 性格影响语气
    progress_influence: 进度影响态度

antagonists:
  - name: 反派名
    level: 小反派/中等反派/大弧Boss/最终Boss
    chapters: [出场章节, 退场章节]
    motivation: 动机
    methods: [手段1, 手段2]
    disgust_level: 8  # 1-10
    weakness: 弱点
    mirror_relation: 与主角的镜像关系

supporting_cast:
  - name: 配角名
    function: 导师/盟友/情报源/牺牲品/镜像对照
    relation_to_protagonist: 与主角关系
    core_traits: [trait1, trait2]
    signature: 标志性特征
    exit: 退场方式

relationships:
  - type: 冲突型/联盟型/亲密型/权威型
    characters: [角色A, 角色B]
    affinity_stages: [陌生, 初识, 熟悉, 信任]
    arc: 关系弧线描述
    test_event: 考验事件
```
