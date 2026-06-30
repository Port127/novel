---
name: design-character
description: 人设设计。与 Agent 交互设计主角、反派、配角，含爽感维度评估。
---

# design-character（人设设计）

> **用途**：设计小说人物，包括主角、反派、配角，并评估爽感维度。
> **前置条件**：`{project_dir}/settings/scout_report.yaml` 和 `worldbuilding.yaml` 存在。
> **输出文件**：`{project_dir}/settings/characters.yaml`

---

## 核心原则 (Core Principles)

1. **防暴走与启发式交互 (UX)**：严禁一次性执行多个 Phase 或连发开放式提问。每个 Phase 结束前必须停下等待用户。提问时必须基于上下文提供 **2-3 个具体预设方案 (Option A/B/C)** 供用户选择或微调。
2. **多智能体编排 (Orchestration)**：在涉及重度脑暴或深度执行的 Phase 中，主 Agent 必须使用 `invoke_subagent` 唤醒 `character-designer` 来负责具体的交互与生成，主 Agent 仅负责流程统筹与最终落盘。
3. **商业与品类对齐 (Commercial Alignment)**：必须基于 `scout_report.yaml` 中的品类要素进行设计（如玄幻需反派，言情需恋爱对象）。刻意制造差异化，遮住名字能分出谁在说话。
4. **素材库联动 (Ecosystem)**：当需要寻找人设灵感或建立动机链时，主动使用 `/nm search character` 或 `/nm search insight` 查询上游素材库。
5. **实时进度保存 (State Persistence)**：进入任何一个新的 Phase，必须立即更新根目录下的 `_progress.md` 文件。
6. **弧线驱动与弱点可信**：主角和反派必须有清晰的起点→终点弧线，弱点让角色可信，没有弱点的完美角色不可信。
7. **爽感可量化**：打脸指数、CP感、反派恶心度——三维评估人设质量。

---

## Phase 定义 (Phase State Machine)

> **【架构强制要求】**：
> 1. 生成任何结构化数据前，**必须使用 `view_file` 强制读取 `data/schemas/characters.schema.yaml`**。
> 2. 严禁按己意图捏造不在 Schema 中的顶级字段。
> 3. Reference 文件应当按需在具体的 Phase 中加载，不要在 Phase 1 一次性全读完。

### Phase 1：准备与上下文对齐

**入口条件**：`scout_report.yaml` 和 `worldbuilding.yaml` 存在
**目标**：拉取基础上下文，确认本技能的操作范围

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 1。
2. **强制读取 Schema**：使用 `view_file` 读取本次目标输出对应的 `data/schemas/characters.schema.yaml`。
3. 读取 `{project_dir}/settings/scout_report.yaml` 的 `genre` 和 `required_elements.characters`。
4. 读取 `{project_dir}/settings/worldbuilding.yaml`，理解世界观、力量体系和社会结构。
5. （按需）读取 `references/character-basics.md` 加载品类角色框架。
6. 综合以上信息，向用户展示该品类需要设计的角色类型范围，并提供 **2-3 个关于主角初步设定的方向 (Option A/B/C)** 供用户选择。

**出口条件**：操作范围已与用户确认，主角大方向已定。

> [!IMPORTANT]
> **【系统红线】**：在完成 Phase 1 后，**必须停止调用工具并向用户展示当前设计范围**。只有在获得用户明确确认后，才允许进入 Phase 2！

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
7. 提供主角设计的 **2-3 个具体变体方案 (Option A/B/C)** 让用户挑选或微调。
8. 依据用户反馈在内存中暂存 protagonist 条目。

**出口条件**：主角人设已设计并获用户确认。
**加载 References**：`protagonist-arc.md`、`character-basics.md`、`character-design-methods.md`、`dialogue-mastery.md`

> [!IMPORTANT]
> **【系统红线】**：在完成 Phase 2 的每轮提问后，**必须停止调用工具并等待用户回复**。获得明确 Accept 后，更新 `_progress.md` 的 `current_phase` 为 3，才允许进入 Phase 3！

#### Agent 调用：character-designer（可选增强）

如果需要深度设计，请使用 `invoke_subagent` 工具唤醒 `character-designer` 子代理（前提是 `.agents/agents/character-designer.md` 存在）。
**调用参数示例**：
- `TypeName`: `character-designer`
- `Prompt`: "项目根目录：{当前项目绝对路径}。任务：辅助主角三层标签设计、九维深化、语言风格档案建立。请读取 settings/characters.yaml 并给出建议。"
*(如 agent 不可用，则降级由主线程直接完成。)*

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
6. 提供反派设计的 **2-3 个具体设定变体 (Option A/B/C)** 供用户挑选或微调。
7. 依据用户反馈在内存中暂存 antagonist 条目。

**出口条件**：反派人设已获用户确认（包含 Schema 要求的所有强制字段）。
**加载 References**：`villain-design.md`

> [!IMPORTANT]
> **【系统红线】**：在完成 Phase 3 的每轮提问后，**必须停止调用工具并等待用户回复**。获得明确 Accept 后，更新 `_progress.md` 的 `current_phase` 为 4，才允许进入 Phase 4！

#### Agent 调用：character-designer（可选增强）

使用 `invoke_subagent` 工具唤醒 `character-designer` 子代理。
**调用参数示例**：
- `TypeName`: `character-designer`
- `Prompt`: "项目根目录：{当前项目绝对路径}。任务：辅助反派设计、补充心理维度(psychology)与人物弧线(arc)、镜像关系建立、恶心度优化。"
*(如 agent 不可用，由主线程完成。)*

---

### Phase 4：配角与关系网络

**入口条件**：主角和反派已设计
**目标**：设计配角和关系网络

**步骤**：
1. 读取 `references/character-relations.md`
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
6. 提供配角与关系网络的 **2-3 种编排方案 (Option A/B/C)** 供用户挑选。
7. 依据用户反馈暂存 supporting 条目与 relationships 条目。

**出口条件**：配角网络与关系弧线已获用户确认。
**加载 References**：`character-relations.md`

> [!IMPORTANT]
> **【系统红线】**：在完成 Phase 4 的每轮提问后，**必须停止调用工具并等待用户回复**。获得明确 Accept 后，更新 `_progress.md` 的 `current_phase` 为 5，才允许进入 Phase 5！

---

### Phase 5：落盘验证 (Quality Gate)

**入口条件**：所有必需角色已设计
**目标**：评估爽感三维，写入硬盘并通过自动化门禁检查

**步骤**：
1. **进度更新**：更新 `_progress.md` 的 `current_phase` 为 5。
2. （按需）读取 `references/cool-factor-guide.md` 评估三维爽感（打脸指数、CP感、反派恶心度）。如 < 6/10 则调整。
3. **最终检查**：汇总内存中的所有设定，检查是否严格符合 `characters.schema.yaml`。
4. **写入文件**：按照 Schema 严格写入 `{project_dir}/settings/characters.yaml`（使用 `characters: []` 数组结构）。
5. **门禁校验**：运行 `node .agents/skills/design-character/scripts/check-characters.js {project_dir}/settings/scout_report.yaml {project_dir}/settings/characters.yaml` 进行验证。
6. 根据脚本输出的 `[blocking]` 或 `[advisory]` 决定是否重做。如有阻断性错误，**必须阻断流程并修正**。
7. 验证通过后清理 `_progress.md` 文件，宣告本技能完成。

**出口条件**：`characters.yaml` 已合规生成并写入硬盘，爽感三维达标。
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

## 断点恢复 (Recovery)

**状态文件**：`_progress.md`（位于项目根目录）

**格式范例**：
```markdown
# design-character Progress
- current_phase: <1-5>
- status: in_progress | completed
- last_updated: <timestamp>
```

**恢复逻辑**：
- 启动时检查 `_progress.md`。
- 若状态非 completed，主动询问用户是否继续中断的进度，跳到对应的 current_phase。

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
| 4 | character-relations.md | 配角 + 关系网络（四种类型 + 好感度 + 弧线） |
| 5 | cool-factor-guide.md | 爽感三维评估 |

---

## 下一步 (Next Steps)

本技能完成后，推荐执行的操作或进入的下一步 Skill：
- `/design-outline`：基于现有人设进行大纲与故事结构设计。
- `/paywall-design`：如果是付费导向，可以提前思考付费卡点的分布。

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
| 配角空转 | 配角无功能，出场无意义 | 删除或重新定义功能 | character-relations.md |
| 好感度失控 | 互动尺度不匹配关系阶段 | 按好感度体系调整互动边界 | character-relations.md |

---

## 角色档案输出格式 (严格遵循 Schema)

```yaml
# characters.yaml 示例结构（必须是 characters: 的列表结构）
characters:
  # === 主角 ===
  - name: 角色名
    role: protagonist
    archetype: 废柴逆袭
    description: 一句话核心描述
    traits: [trait1, trait2, trait3]
    # 下方字段为 protagonist 独有深化
    identity_tags: [身份标签1, 身份标签2]
    appearance_tags: [表现标签1, 表现标签2]
    core_tags: [内核标签1, 内核标签2]
    appearance:
      age: 年龄段
      gender: 性别
      features: [外貌特征1, 外貌特征2]
      typical_clothing: 典型着装
    psychology:
      fatal_flaw: 致命弱点
      obsession: 执念
      soft_spot: 软肋
      misbelief: 误判
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
      type: 成长弧线
      start: 起点状态
      end: 终点状态
      stages:
        - stage: 阶段1
          state: 状态1
          chapter: 章节号
    language_profile:
      catchphrase: 口头禅
      speech_rhythm: 说话节奏
      # ... 其他 7 维度
    # === 关系网络（必须嵌套在角色内部）===
    relationships:
      - to: 角色B
        type: 冲突型
        description: 宿敌关系描述
        importance: primary
    # === 阵营归属（可选联动 worldbuilding）===
    faction_affiliations:
      - faction: 势力名称
        role: 在势力中的角色
        period: 归属时期

  # === 反派 ===
  - name: 反派名
    role: antagonist
    archetype: 反派
    description: 一句话核心描述
    traits: [手段毒辣, 隐忍]
    # 反派也必须有 psychology 和 arc（Schema要求）
    psychology:
      fatal_flaw: 傲慢
      obsession: 统治世界
    arc:
      type: 悲剧弧线
      start: 巅峰
      end: 陨落
    level: 最终Boss
    chapters: [出场章节, 退场章节]
    motivation: 动机
    methods: [手段1, 手段2]
    disgust_level: 8
    weakness: 弱点
    mirror_relation: 与主角的镜像关系

  # === 配角 ===
  - name: 配角名
    role: supporting
    archetype: 导师型
    description: 隐藏在戒指里的老爷爷
    traits: [护短, 嘴毒]
    function: 导师/盟友
    relation_to_protagonist: 与主角关系
    signature: 标志性特征
```
