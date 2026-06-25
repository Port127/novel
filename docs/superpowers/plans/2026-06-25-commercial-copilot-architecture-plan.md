# Commercial Copilot Architecture V2 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有架构升级为"商业化变现引擎"，实现付费卡点设计、套路模板库、品类画像适配、成本硬约束和存稿应急机制。

**Architecture:** 基于 `BaseCommercialSkill` 抽象基类构建所有创作 Skill，每个 Skill 实现 `evaluate()` 和 `fix()` 接口。通过 `GenreProfile` 配置品类参数，`TropeTemplate` 存储叙事模板。`DailyUpdateWorkflow` 作为编排层集成 Token 预算控制和存稿管理。

**Tech Stack:** Python 3.12, pydantic v2, async OpenAI client, pytest-asyncio

---

## 阶段划分

| 阶段 | 优先级 | 核心交付 |
|------|--------|---------|
| Phase 1 | P0 生存红线 | BaseSkill、AntiAiPolish、AuditHooks、DailyWorkflow、DesignPaywall |
| Phase 2 | P1 破局增效 | ForgeGoldenChapters、ScoutTopic、DesignCharacter |
| Phase 3 | P2 长线保障 | AskArchitect、AnalyzeStats、FleshOutChapter、CheckLogic |
| Phase 4 | 横切关注 | GenreProfile、TropeTemplate、CommercialGates |

---

# Phase 1: P0 生存红线

## Task 1: 基础工程底座 — BaseCommercialSkill 与类型定义

**Files:**
- Create: `src/novel/core/skills/base.py`
- Create: `tests/core/skills/test_base.py`
- Modify: `src/novel/core/skills/__init__.py`

- [ ] **Step 1: 创建测试 — BaseCommercialSkill 接口与 Verdict 类型**

```python
# tests/core/skills/test_base.py
import pytest
from pydantic import BaseModel
from novel.core.skills.base import (
    BaseCommercialSkill,
    CommercialVerdict,
    SkillResult,
    TokenUsage,
)

class MockSkill(BaseCommercialSkill):
    name = "mock_skill"
    
    async def evaluate(self, text: str, context: dict | None = None) -> CommercialVerdict:
        passed = "good" in text.lower()
        return CommercialVerdict(
            passed=passed,
            diagnostics=[] if passed else ["缺少 'good' 关键词"],
            layer_scores={"mock": 80.0 if passed else 40.0},
        )
    
    async def fix(self, text: str, verdict: CommercialVerdict) -> SkillResult:
        if verdict.passed:
            return SkillResult(text=text, token_usage=TokenUsage(prompt_tokens=0, completion_tokens=0))
        fixed = text + " good"
        return SkillResult(
            text=fixed,
            token_usage=TokenUsage(prompt_tokens=10, completion_tokens=5),
        )

@pytest.mark.asyncio
async def test_verdict_passed():
    skill = MockSkill()
    verdict = await skill.evaluate("this is good text")
    assert verdict.passed is True
    assert verdict.diagnostics == []
    assert verdict.layer_scores["mock"] == 80.0

@pytest.mark.asyncio
async def test_verdict_failed():
    skill = MockSkill()
    verdict = await skill.evaluate("this is bad text")
    assert verdict.passed is False
    assert "缺少 'good' 关键词" in verdict.diagnostics
    assert verdict.layer_scores["mock"] == 40.0

@pytest.mark.asyncio
async def test_fix_returns_skill_result():
    skill = MockSkill()
    verdict = await skill.evaluate("bad text")
    result = await skill.fix("bad text", verdict)
    assert isinstance(result, SkillResult)
    assert "good" in result.text
    assert result.token_usage.prompt_tokens == 10
    assert result.token_usage.completion_tokens == 5

def test_token_usage_cost_calculation():
    usage = TokenUsage(prompt_tokens=1000, completion_tokens=500, model="gpt-4o-mini")
    assert usage.estimated_cost > 0
    assert usage.total_tokens == 1500
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/core/skills/test_base.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'novel.core.skills.base'`

- [ ] **Step 3: 实现 BaseCommercialSkill 基类**

```python
# src/novel/core/skills/base.py
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Literal

# 模型定价表 (每 1K token，单位：美元)
MODEL_PRICING = {
    "gpt-4o": {"prompt": 0.005, "completion": 0.015},
    "gpt-4o-mini": {"prompt": 0.00015, "completion": 0.0006},
    "gpt-3.5-turbo": {"prompt": 0.0005, "completion": 0.0015},
}

class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    model: str = "gpt-4o-mini"
    
    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens
    
    @property
    def estimated_cost(self) -> float:
        pricing = MODEL_PRICING.get(self.model, MODEL_PRICING["gpt-4o-mini"])
        prompt_cost = (self.prompt_tokens / 1000) * pricing["prompt"]
        completion_cost = (self.completion_tokens / 1000) * pricing["completion"]
        return round(prompt_cost + completion_cost, 6)

class CommercialVerdict(BaseModel):
    passed: bool
    diagnostics: list[str] = Field(default_factory=list)
    layer_scores: dict[str, float] = Field(default_factory=dict)
    severity: Literal["info", "warning", "critical"] = "info"

class SkillResult(BaseModel):
    text: str
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    metadata: dict = Field(default_factory=dict)

class BaseCommercialSkill(ABC):
    name: str = "unnamed_skill"
    
    @abstractmethod
    async def evaluate(self, text: str, context: dict | None = None) -> CommercialVerdict:
        """评估文本质量，返回结构化判定结果"""
        ...
    
    @abstractmethod
    async def fix(self, text: str, verdict: CommercialVerdict) -> SkillResult:
        """根据判定结果修复文本，返回修复后的文本和 token 消耗"""
        ...
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/core/skills/test_base.py -v
```

Expected: 4 passed

- [ ] **Step 5: 更新 __init__.py 并 commit**

```python
# src/novel/core/skills/__init__.py
from .base import BaseCommercialSkill, CommercialVerdict, SkillResult, TokenUsage
from .pipeline import Skill, run_skill_pipeline

__all__ = [
    "BaseCommercialSkill",
    "CommercialVerdict",
    "SkillResult",
    "TokenUsage",
    "Skill",
    "run_skill_pipeline",
]
```

```bash
git add src/novel/core/skills/base.py src/novel/core/skills/__init__.py tests/core/skills/test_base.py
git commit -m "feat(core): add BaseCommercialSkill with TokenUsage cost tracking

- Introduce CommercialVerdict for structured quality judgments
- Add SkillResult with token usage and cost estimation
- Support multi-model pricing table (gpt-4o, gpt-4o-mini, gpt-3.5-turbo)"
```

---

## Task 2: AntiAiPolish Skill — 五层去 AI 味模型

**Files:**
- Create: `src/novel/core/skills/anti_ai_polish.py`
- Create: `tests/core/skills/test_anti_ai_polish.py`
- Create: `references/anti_ai_rules.md`

- [ ] **Step 1: 创建禁词表和规则文档**

```markdown
# references/anti_ai_rules.md
# Anti-AI 味检测规则

## Layer 1: 词汇层禁词表
以下词汇在网文中属于典型 AI 高频词，应尽量避免或替换：

### 一级禁词（必须替换）
- 不禁、宛如、映射、然而、似乎、仿佛、渐渐、缓缓
- 目光如炬、眼神深邃、嘴角微扬、眉头紧锁

### 二级禁词（建议替换）
- 不禁想到、不由自主、心中暗道、暗自思忖
- 一股莫名的、一种说不出的

## Layer 2: 句式层规则
- 连续 3 个以上四字成语/短语排比 → 判定为"句式过于对仗"
- 连续 2 个以上"XX了XX"结构 → 判定为"模板化表达"
- 单句超过 40 字 → 建议拆分为短句

## Layer 3: 段落层规则
- 段落以"总而言之"、"综上所述"、"这一天"等总结性词语结尾 → 判定为"强行升华"
- 段落结构为"总-分-总" → 建议改为"分-总"或直接删除总结句

## Layer 4: 叙事层规则
- 同一段落内出现 2 个以上不同角色的内心独白 → 判定为"视角混乱"
- 对话占比低于 20% → 建议增加口语化对话

## Layer 5: 情感层规则
- 情绪词为"失落、难过、开心、生气"等温和词 → 判定为"情绪平淡"
- 要求替换为"杀意、憋屈、狂喜、暴怒"等尖锐情绪
```

- [ ] **Step 2: 创建测试 — 五层拦截逻辑**

```python
# tests/core/skills/test_anti_ai_polish.py
import pytest
from novel.core.skills.anti_ai_polish import AntiAiPolishSkill, PolishAnalysis

@pytest.fixture
def skill():
    return AntiAiPolishSkill()

@pytest.mark.asyncio
async def test_layer1_vocab_violations(skill):
    """词汇层：检测一级禁词"""
    text = "李明不禁皱起眉头，宛如神魔降世。然而，这一切映射着他内心的挣扎。"
    verdict = await skill.evaluate(text)
    assert verdict.passed is False
    assert "不禁" in verdict.diagnostics[0] or "vocab" in verdict.layer_scores
    assert verdict.layer_scores["vocab"] < 60

@pytest.mark.asyncio
async def test_layer2_syntax_patterns(skill):
    """句式层：检测连续排比和四字成语堆砌"""
    text = "剑气纵横交错，光芒摧枯拉朽，威势惊天动地，气息排山倒海，声势浩大无比。"
    verdict = await skill.evaluate(text)
    assert verdict.layer_scores["syntax"] < 60
    assert any("句式" in d or "排比" in d for d in verdict.diagnostics)

@pytest.mark.asyncio
async def test_layer3_forced_summary(skill):
    """段落层：检测强行总结升华"""
    text = "经过一番激战，他终于击败了对手。这一战让他明白了力量的真谛，也让他看到了自己的不足。总而言之，今天的修炼让他收获颇丰。"
    verdict = await skill.evaluate(text)
    assert verdict.layer_scores["paragraph"] < 60
    assert any("总结" in d or "升华" in d for d in verdict.diagnostics)

@pytest.mark.asyncio
async def test_layer5_emotion_intensity(skill):
    """情感层：检测情绪平淡"""
    text = "王长老拿走属于他的丹药，他心中感到一阵失落，决定以后更加努力修炼。"
    verdict = await skill.evaluate(text)
    assert verdict.layer_scores["emotion"] < 60
    assert any("情绪" in d or "平淡" in d for d in verdict.diagnostics)

@pytest.mark.asyncio
async def test_clean_text_passes(skill):
    """干净的网文文本应该通过"""
    text = ""妈的！"陈凡一拳砸在桌上，'你敢动我妹妹，老子今天跟你拼了！'他双眼血红，像一头发疯的野兽冲了上去。"
    verdict = await skill.evaluate(text)
    # 允许有小问题，但整体应该通过
    assert verdict.layer_scores.get("vocab", 100) >= 60
    assert verdict.layer_scores.get("emotion", 100) >= 60

def test_polish_analysis_schema():
    """验证结构化输出 Schema"""
    analysis = PolishAnalysis(
        vocab_violations=["不禁", "宛如"],
        syntax_score=45,
        has_forced_summary=True,
        emotion_intensity="平淡",
    )
    assert len(analysis.vocab_violations) == 2
    assert analysis.syntax_score == 45
```

- [ ] **Step 3: 运行测试确认失败**

```bash
pytest tests/core/skills/test_anti_ai_polish.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'novel.core.skills.anti_ai_polish'`

- [ ] **Step 4: 实现 AntiAiPolishSkill**

```python
# src/novel/core/skills/anti_ai_polish.py
import re
from pydantic import BaseModel, Field
from novel.core.skills.base import BaseCommercialSkill, CommercialVerdict, SkillResult, TokenUsage
from novel.core.llm.structured import generate_structured

# 一级禁词表
LEVEL1_BANNED_WORDS = [
    "不禁", "宛如", "映射", "然而", "似乎", "仿佛", "渐渐", "缓缓",
    "目光如炬", "眼神深邃", "嘴角微扬", "眉头紧锁",
]

# 总结性词语（段落层）
SUMMARY_PATTERNS = [
    r"总而言之", r"综上所述", r"这一天.*收获", r"明白了.*真谛",
]

# 温和情绪词（情感层）
WEAK_EMOTIONS = ["失落", "难过", "开心", "生气", "伤心", "高兴"]

class PolishAnalysis(BaseModel):
    vocab_violations: list[str] = Field(default_factory=list, description="触发的禁词列表")
    syntax_score: int = Field(default=100, description="句式白话/简短程度 0-100")
    has_forced_summary: bool = Field(default=False, description="是否强行总结升华")
    emotion_intensity: str = Field(default="尖锐", description="情绪强度：平淡/讲理/尖锐")

class AntiAiPolishSkill(BaseCommercialSkill):
    name = "anti_ai_polish"
    
    async def evaluate(self, text: str, context: dict | None = None) -> CommercialVerdict:
        diagnostics = []
        layer_scores = {}
        
        # Layer 1: 词汇层
        vocab_violations = [w for w in LEVEL1_BANNED_WORDS if w in text]
        vocab_score = 100 - len(vocab_violations) * 15
        layer_scores["vocab"] = max(0, vocab_score)
        if vocab_violations:
            diagnostics.append(f"词汇层：检测到禁词 {vocab_violations}")
        
        # Layer 2: 句式层（简单规则：四字成语连续出现）
        four_char_pattern = re.findall(r"[，,][^，,]{4}[，,]", text)
        if len(four_char_pattern) >= 3:
            layer_scores["syntax"] = 40
            diagnostics.append("句式层：连续四字短语排比过多")
        else:
            layer_scores["syntax"] = 80
        
        # Layer 3: 段落层
        has_summary = any(re.search(p, text) for p in SUMMARY_PATTERNS)
        layer_scores["paragraph"] = 40 if has_summary else 80
        if has_summary:
            diagnostics.append("段落层：检测到强行总结升华")
        
        # Layer 4: 叙事层（简化：检查对话占比）
        dialogue_ratio = len(re.findall(r"["「](.*?)["」]", text)) / max(len(text), 1)
        layer_scores["narrative"] = 60 if dialogue_ratio < 0.2 else 80
        
        # Layer 5: 情感层
        has_weak_emotion = any(w in text for w in WEAK_EMOTIONS)
        layer_scores["emotion"] = 40 if has_weak_emotion else 80
        if has_weak_emotion:
            diagnostics.append("情感层：情绪平淡，建议使用更尖锐的情绪词")
        
        # 综合判定
        avg_score = sum(layer_scores.values()) / len(layer_scores)
        passed = avg_score >= 60 and not vocab_violations
        
        return CommercialVerdict(
            passed=passed,
            diagnostics=diagnostics,
            layer_scores=layer_scores,
            severity="critical" if vocab_violations else "warning",
        )
    
    async def fix(self, text: str, verdict: CommercialVerdict) -> SkillResult:
        if verdict.passed:
            return SkillResult(text=text, token_usage=TokenUsage())
        
        # 实际实现中这里会调用 LLM 进行改写
        # 当前最小实现：仅做词汇替换
        fixed_text = text
        for word in ["不禁", "宛如", "然而", "仿佛"]:
            fixed_text = fixed_text.replace(word, "")
        
        return SkillResult(
            text=fixed_text,
            token_usage=TokenUsage(prompt_tokens=len(text), completion_tokens=len(fixed_text), model="gpt-4o-mini"),
        )
```

- [ ] **Step 5: 运行测试确认通过**

```bash
pytest tests/core/skills/test_anti_ai_polish.py -v
```

Expected: 6 passed

- [ ] **Step 6: Commit**

```bash
git add src/novel/core/skills/anti_ai_polish.py tests/core/skills/test_anti_ai_polish.py references/anti_ai_rules.md
git commit -m "feat(skills): add AntiAiPolishSkill with 5-layer detection model

- Layer 1: Vocabulary (banned AI words like 不禁, 宛如, 然而)
- Layer 2: Syntax (detect consecutive 4-char patterns)
- Layer 3: Paragraph (detect forced summaries)
- Layer 4: Narrative (dialogue ratio check)
- Layer 5: Emotion (detect weak emotions like 失落, 难过)
- Add anti_ai_rules.md reference document"
```

---

## Task 3: AuditHooks Skill — 章末钩子 + 标题审查

**Files:**
- Create: `src/novel/core/skills/audit_hooks.py`
- Create: `tests/core/skills/test_audit_hooks.py`

- [ ] **Step 1: 创建测试**

```python
# tests/core/skills/test_audit_hooks.py
import pytest
from novel.core.skills.audit_hooks import AuditHooksSkill, HookAnalysis

@pytest.fixture
def skill():
    return AuditHooksSkill()

@pytest.mark.asyncio
async def test_bland_chapter_ending_fails(skill):
    """平淡结尾应该失败"""
    text = "天亮了，大家收拾行李准备明天继续赶路。夜色渐深，众人各自回房休息，一夜无话。"
    verdict = await skill.evaluate(text)
    assert verdict.passed is False
    assert any("平淡" in d or "钩子" in d for d in verdict.diagnostics)

@pytest.mark.asyncio
async def test_suspenseful_ending_passes(skill):
    """致命悬念结尾应该通过"""
    text = "就在大门关闭的刹那，一口带血的飞剑'当'地一声钉在门栓上，剑柄上，还挂着半截属于他妹妹的玉佩！陈凡瞳孔骤缩，那是他亲手给妹妹戴上的！"
    verdict = await skill.evaluate(text)
    assert verdict.passed is True

@pytest.mark.asyncio
async def test_conflict_density_warning(skill):
    """2000字无冲突应该触发警告"""
    # 生成一段 2500 字的平淡文本
    bland_text = "他走在路上，看着风景，想着心事。" * 100  # ~1500 字
    verdict = await skill.evaluate(bland_text)
    assert any("冲突" in d or "密度" in d for d in verdict.diagnostics)

@pytest.mark.asyncio
async def test_chapter_title_detection(skill):
    """章节标题应该包含悬念或冲突"""
    good_titles = ["他竟是……", "谁在背后操纵？", "一刀斩破苍穹"]
    bad_titles = ["第三章", "修炼", "离开"]
    
    for title in good_titles:
        analysis = await skill.analyze_title(title)
        assert analysis.clickbait_score >= 60, f"好标题 {title} 应该得分 >= 60"
    
    for title in bad_titles:
        analysis = await skill.analyze_title(title)
        assert analysis.clickbait_score < 60, f"差标题 {title} 应该得分 < 60"

def test_hook_analysis_schema():
    """验证钩子分析 Schema"""
    analysis = HookAnalysis(
        hook_type="crisis",
        suspense_level=9,
        clickbait_score=85,
        suggested_titles=["他竟是……", "背后的黑手"],
    )
    assert analysis.hook_type == "crisis"
    assert analysis.suspense_level == 9
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/core/skills/test_audit_hooks.py -v
```

Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: 实现 AuditHooksSkill**

```python
# src/novel/core/skills/audit_hooks.py
import re
from pydantic import BaseModel, Field
from novel.core.skills.base import BaseCommercialSkill, CommercialVerdict, SkillResult, TokenUsage

# 悬念关键词
SUSPENSE_KEYWORDS = [
    "竟是", "没想到", "突然", "刹那间", "瞳孔骤缩", "震惊",
    "难道", "不可能", "怎么可能", "背后", "秘密", "真相",
    "！", "？", "……",
]

# 冲突关键词
CONFLICT_KEYWORDS = [
    "杀", "战", "怒", "吼", "拳", "剑", "血", "死",
    "冲突", "对抗", "危机", "险境", "绝境",
]

# 标题悬念模式
TITLE_PATTERNS = [
    r"[…？！]",  # 省略号、问号、感叹号
    r"竟", r"难道", r"谁", r"何", r"怎",  # 疑问词
    r"秘密", r"真相", r"背后", r"黑手",  # 悬念词
]

class HookAnalysis(BaseModel):
    hook_type: str = Field(description="钩子类型：crisis/reversal/mystery")
    suspense_level: int = Field(ge=1, le=10, description="悬念强度 1-10")
    clickbait_score: int = Field(ge=0, le=100, description="标题点击吸引力 0-100")
    suggested_titles: list[str] = Field(default_factory=list)

class AuditHooksSkill(BaseCommercialSkill):
    name = "audit_hooks"
    
    async def evaluate(self, text: str, context: dict | None = None) -> CommercialVerdict:
        diagnostics = []
        layer_scores = {}
        
        # 检测最后 800 字的钩子
        ending_text = text[-800:] if len(text) > 800 else text
        suspense_count = sum(1 for kw in SUSPENSE_KEYWORDS if kw in ending_text)
        suspense_score = min(100, suspense_count * 15)
        layer_scores["hook"] = suspense_score
        
        if suspense_score < 60:
            diagnostics.append(f"章末钩子：平淡结尾，悬念强度仅 {suspense_score}/100")
        
        # 检测全文冲突密度（每 1000 字窗口）
        conflict_density = self._calculate_conflict_density(text)
        layer_scores["conflict_density"] = conflict_density
        
        if conflict_density < 40:
            diagnostics.append(f"冲突密度：全文冲突密度偏低 ({conflict_density}/100)，建议增加波澜")
        
        # 综合判定
        avg_score = sum(layer_scores.values()) / len(layer_scores)
        passed = avg_score >= 60
        
        return CommercialVerdict(
            passed=passed,
            diagnostics=diagnostics,
            layer_scores=layer_scores,
            severity="critical" if suspense_score < 40 else "warning",
        )
    
    async def analyze_title(self, title: str) -> HookAnalysis:
        """分析章节标题的点击吸引力"""
        pattern_matches = sum(1 for p in TITLE_PATTERNS if re.search(p, title))
        clickbait_score = min(100, pattern_matches * 30)
        
        # 生成建议标题（简化版，实际需要 LLM）
        suggested = []
        if clickbait_score < 60:
            suggested = ["他竟是……", "背后的真相"]
        
        return HookAnalysis(
            hook_type="mystery" if "？" in title or "?" in title else "crisis",
            suspense_level=min(10, pattern_matches * 3),
            clickbait_score=clickbait_score,
            suggested_titles=suggested,
        )
    
    async def fix(self, text: str, verdict: CommercialVerdict) -> SkillResult:
        # 实际实现中会调用 LLM 重写结尾
        return SkillResult(text=text, token_usage=TokenUsage())
    
    def _calculate_conflict_density(self, text: str) -> int:
        """计算每 1000 字的冲突密度"""
        if len(text) < 1000:
            return 50
        
        window_size = 1000
        conflict_scores = []
        
        for i in range(0, len(text), window_size):
            window = text[i:i+window_size]
            conflict_count = sum(1 for kw in CONFLICT_KEYWORDS if kw in window)
            conflict_scores.append(min(100, conflict_count * 20))
        
        return sum(conflict_scores) // len(conflict_scores) if conflict_scores else 0
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/core/skills/test_audit_hooks.py -v
```

Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add src/novel/core/skills/audit_hooks.py tests/core/skills/test_audit_hooks.py
git commit -m "feat(skills): add AuditHooksSkill for chapter ending and title analysis

- Detect suspense hooks in last 800 characters
- Calculate conflict density per 1000-word window
- Analyze chapter title clickbait potential
- Support 3 hook types: crisis, reversal, mystery"
```

---

## Task 4: DailyUpdateWorkflow — 日更管家（含成本控制、存稿管理和应急协议）

**Files:**
- Create: `src/novel/core/workflow/daily_manager.py`
- Create: `src/novel/core/workflow/cost_tracker.py`
- Create: `src/novel/core/workflow/manuscript_store.py`
- Create: `tests/core/workflow/test_daily_manager.py`
- Create: `tests/core/workflow/test_cost_tracker.py`
- Create: `tests/core/workflow/test_manuscript_store.py`

- [ ] **Step 1: 创建 ManuscriptStore 测试 — 三级存稿分类**

```python
# tests/core/workflow/test_manuscript_store.py
import pytest
from novel.core.workflow.manuscript_store import ManuscriptStore, ManuscriptTier

def test_manuscript_tier_classification():
    store = ManuscriptStore()
    
    # Add manuscripts at different tiers
    store.add("chapter_101", tier=ManuscriptTier.REFINED)
    store.add("chapter_102", tier=ManuscriptTier.DRAFT)
    store.add("chapter_103", tier=ManuscriptTier.OUTLINE)
    
    assert store.count(ManuscriptTier.REFINED) == 1
    assert store.count(ManuscriptTier.DRAFT) == 1
    assert store.count(ManuscriptTier.OUTLINE) == 1
    assert store.total_count == 3

def test_consume_priority():
    """发布时优先消耗精修稿"""
    store = ManuscriptStore()
    store.add("chapter_101", tier=ManuscriptTier.REFINED)
    store.add("chapter_102", tier=ManuscriptTier.DRAFT)
    
    # Should consume refined first
    consumed = store.consume_next()
    assert consumed == "chapter_101"
    assert store.count(ManuscriptTier.REFINED) == 0
    
    # Then draft
    consumed = store.consume_next()
    assert consumed == "chapter_102"

def test_empty_store_returns_none():
    store = ManuscriptStore()
    assert store.consume_next() is None
```

- [ ] **Step 2: 创建 CostTracker 测试 — 单次调用上限**

```python
# tests/core/workflow/test_cost_tracker.py
import pytest
from novel.core.workflow.cost_tracker import CostTracker, BudgetExceededError, TokenLimitExceededError
from novel.core.skills.base import TokenUsage

def test_cost_tracker_accumulates_usage():
    tracker = CostTracker(daily_budget=15.0)
    
    usage1 = TokenUsage(prompt_tokens=1000, completion_tokens=500, model="gpt-4o-mini")
    tracker.record(usage1)
    
    usage2 = TokenUsage(prompt_tokens=2000, completion_tokens=1000, model="gpt-4o-mini")
    tracker.record(usage2)
    
    assert tracker.total_tokens == 4500
    assert tracker.total_cost > 0
    assert tracker.total_cost < 15.0

def test_cost_tracker_triggers_warning():
    tracker = CostTracker(daily_budget=0.001)
    
    usage = TokenUsage(prompt_tokens=10000, completion_tokens=5000, model="gpt-4o")
    tracker.record(usage)
    
    assert tracker.is_warning_triggered
    assert tracker.remaining_budget < 0

def test_cost_tracker_raises_on_exceed():
    tracker = CostTracker(daily_budget=0.001, hard_limit=True)
    
    usage = TokenUsage(prompt_tokens=10000, completion_tokens=5000, model="gpt-4o")
    
    with pytest.raises(BudgetExceededError):
        tracker.record(usage)

def test_token_limit_per_call():
    """单次调用 token 上限检测"""
    tracker = CostTracker()
    
    # gpt-4o-mini 上限 4000 tokens
    cheap_usage = TokenUsage(prompt_tokens=3500, completion_tokens=3500, model="gpt-4o-mini")
    with pytest.raises(TokenLimitExceededError):
        tracker.record(cheap_usage)
    
    # gpt-4o 上限 8000 tokens
    expensive_usage = TokenUsage(prompt_tokens=7500, completion_tokens=7500, model="gpt-4o")
    with pytest.raises(TokenLimitExceededError):
        tracker.record(expensive_usage)

def test_token_limit_within_bounds():
    """token 在上限内应正常通过"""
    tracker = CostTracker()
    
    usage = TokenUsage(prompt_tokens=2000, completion_tokens=1000, model="gpt-4o-mini")
    tracker.record(usage)  # Should not raise
    assert tracker.total_tokens == 3000
```

- [ ] **Step 3: 创建 DailyManager 测试 — 含应急协议和请假建议**

```python
# tests/core/workflow/test_daily_manager.py
import pytest
from novel.core.workflow.daily_manager import DailyUpdateManager, StockWarning
from novel.core.workflow.cost_tracker import CostTracker

def test_stock_warning_yellow():
    manager = DailyUpdateManager(
        written_chapters=105,
        published_chapters=98,
        mode="fine",
    )
    status = manager.check_reserves()
    assert status.level == "yellow"
    assert status.reserve_count == 7
    assert status.is_warning

def test_stock_warning_red():
    manager = DailyUpdateManager(
        written_chapters=103,
        published_chapters=99,
        mode="fine",
    )
    status = manager.check_reserves()
    assert status.level == "red"
    assert status.reserve_count == 4

def test_stock_warning_normal():
    manager = DailyUpdateManager(
        written_chapters=120,
        published_chapters=100,
        mode="fine",
    )
    status = manager.check_reserves()
    assert status.level == "green"
    assert not status.is_warning

def test_fast_mode_skills():
    manager = DailyUpdateManager(written_chapters=110, published_chapters=100, mode="fast")
    skills = manager.get_skill_pipeline()
    assert "flesh_out_chapter" in skills
    assert "anti_ai_polish" in skills
    assert len(skills) == 2  # Fast mode only uses 2 skills

def test_fine_mode_skills():
    manager = DailyUpdateManager(written_chapters=110, published_chapters=100, mode="fine")
    skills = manager.get_skill_pipeline()
    assert len(skills) >= 4  # Fine mode uses full pipeline

def test_emergency_mode_activation():
    manager = DailyUpdateManager(
        written_chapters=104,
        published_chapters=100,
        mode="fine",
    )
    # Reserve = 4, should trigger red alert
    status = manager.check_reserves()
    assert status.level == "red"
    
    # System should suggest switching to fast mode
    recommended_mode = manager.get_recommended_mode()
    assert recommended_mode == "fast"

def test_leave_suggestion_on_low_quality():
    """连续低质量应该建议请假"""
    manager = DailyUpdateManager(written_chapters=110, published_chapters=100, mode="fine")
    
    # Simulate 3 consecutive low-quality chapters
    manager.record_quality_score(45.0)
    manager.record_quality_score(50.0)
    manager.record_quality_score(55.0)
    
    assert manager.should_suggest_leave() is True

def test_no_leave_suggestion_on_normal_quality():
    """正常质量不应建议请假"""
    manager = DailyUpdateManager(written_chapters=110, published_chapters=100, mode="fine")
    
    manager.record_quality_score(75.0)
    manager.record_quality_score(80.0)
    
    assert manager.should_suggest_leave() is False
```

- [ ] **Step 3: 运行测试确认失败**

```bash
pytest tests/core/workflow/ -v
```

Expected: FAIL

- [ ] **Step 4: 实现 CostTracker**

```python
# src/novel/core/workflow/cost_tracker.py
from datetime import date
from novel.core.skills.base import TokenUsage

class BudgetExceededError(Exception):
    pass

class CostTracker:
    def __init__(self, daily_budget: float = 15.0, hard_limit: bool = False):
        self.daily_budget = daily_budget
        self.hard_limit = hard_limit
        self._total_cost = 0.0
        self._total_tokens = 0
        self._date = date.today()
    
    def record(self, usage: TokenUsage) -> None:
        self._total_cost += usage.estimated_cost
        self._total_tokens += usage.total_tokens
        
        if self.hard_limit and self._total_cost > self.daily_budget:
            raise BudgetExceededError(
                f"Daily budget exceeded: ${self._total_cost:.4f} > ${self.daily_budget:.4f}"
            )
    
    @property
    def total_cost(self) -> float:
        return round(self._total_cost, 6)
    
    @property
    def total_tokens(self) -> int:
        return self._total_tokens
    
    @property
    def remaining_budget(self) -> float:
        return self.daily_budget - self._total_cost
    
    @property
    def is_warning_triggered(self) -> bool:
        return self._total_cost >= self.daily_budget * 0.8
```

- [ ] **Step 5: 实现 DailyUpdateManager**

```python
# src/novel/core/workflow/daily_manager.py
from pydantic import BaseModel
from typing import Literal
from novel.core.workflow.cost_tracker import CostTracker

class ReserveStatus(BaseModel):
    level: Literal["green", "yellow", "red"]
    reserve_count: int
    
    @property
    def is_warning(self) -> bool:
        return self.level in ("yellow", "red")

class DailyUpdateManager:
    def __init__(
        self,
        written_chapters: int,
        published_chapters: int,
        mode: Literal["fast", "fine"] = "fine",
        daily_budget: float = 15.0,
    ):
        self.written_chapters = written_chapters
        self.published_chapters = published_chapters
        self.mode = mode
        self.cost_tracker = CostTracker(daily_budget=daily_budget)
    
    def check_reserves(self) -> ReserveStatus:
        reserve = self.written_chapters - self.published_chapters
        
        if reserve >= 10:
            return ReserveStatus(level="green", reserve_count=reserve)
        elif reserve >= 6:
            return ReserveStatus(level="yellow", reserve_count=reserve)
        else:
            return ReserveStatus(level="red", reserve_count=reserve)
    
    def get_skill_pipeline(self) -> list[str]:
        status = self.check_reserves()
        
        # Emergency: force fast mode
        if status.level == "red":
            return ["flesh_out_chapter", "anti_ai_polish"]
        
        if self.mode == "fast":
            return ["flesh_out_chapter", "anti_ai_polish"]
        else:  # fine mode
            return [
                "flesh_out_chapter",
                "check_logic",
                "anti_ai_polish",
                "audit_hooks",
            ]
    
    def get_recommended_mode(self) -> Literal["fast", "fine"]:
        status = self.check_reserves()
        if status.level == "red":
            return "fast"
        return self.mode
```

- [ ] **Step 6: 运行测试确认通过**

```bash
pytest tests/core/workflow/ -v
```

Expected: 13 passed

- [ ] **Step 7: 实现 ManuscriptStore — 三级存稿分类**

```python
# src/novel/core/workflow/manuscript_store.py
from enum import Enum
from collections import deque

class ManuscriptTier(str, Enum):
    REFINED = "refined"   # 已通过 anti-ai-polish，可直接发布
    DRAFT = "draft"       # 已扩写但未精修
    OUTLINE = "outline"   # 仅有节拍表，需完整扩写

class ManuscriptStore:
    def __init__(self):
        self._store = {tier: deque() for tier in ManuscriptTier}
    
    def add(self, chapter_id: str, tier: ManuscriptTier) -> None:
        self._store[tier].append(chapter_id)
    
    def count(self, tier: ManuscriptTier) -> int:
        return len(self._store[tier])
    
    @property
    def total_count(self) -> int:
        return sum(len(q) for q in self._store.values())
    
    def consume_next(self) -> str | None:
        """发布时优先消耗精修稿，其次粗稿，最后大纲稿"""
        for tier in [ManuscriptTier.REFINED, ManuscriptTier.DRAFT, ManuscriptTier.OUTLINE]:
            if self._store[tier]:
                return self._store[tier].popleft()
        return None
```

- [ ] **Step 8: 更新 CostTracker — 加入单次调用上限**

```python
# src/novel/core/workflow/cost_tracker.py
from datetime import date
from novel.core.skills.base import TokenUsage

class BudgetExceededError(Exception):
    pass

class TokenLimitExceededError(Exception):
    pass

# 每模型单次调用 token 上限（prompt + completion）
TOKEN_LIMITS_PER_CALL = {
    "cheap": 4000,      # gpt-4o-mini, gpt-3.5-turbo
    "mid": 6000,        # gpt-4o-mini with higher limits
    "expensive": 8000,  # gpt-4o
}

# 模型分级映射
MODEL_TIER = {
    "gpt-4o": "expensive",
    "gpt-4o-mini": "cheap",
    "gpt-3.5-turbo": "cheap",
}

class CostTracker:
    def __init__(self, daily_budget: float = 15.0, hard_limit: bool = False):
        self.daily_budget = daily_budget
        self.hard_limit = hard_limit
        self._total_cost = 0.0
        self._total_tokens = 0
        self._date = date.today()
    
    def record(self, usage: TokenUsage) -> None:
        # 检查单次调用上限
        tier = MODEL_TIER.get(usage.model, "cheap")
        limit = TOKEN_LIMITS_PER_CALL[tier]
        if usage.total_tokens > limit:
            raise TokenLimitExceededError(
                f"Single call exceeded {tier} tier limit: "
                f"{usage.total_tokens} > {limit} tokens (model: {usage.model})"
            )
        
        self._total_cost += usage.estimated_cost
        self._total_tokens += usage.total_tokens
        
        if self.hard_limit and self._total_cost > self.daily_budget:
            raise BudgetExceededError(
                f"Daily budget exceeded: ${self._total_cost:.4f} > ${self.daily_budget:.4f}"
            )
    
    @property
    def total_cost(self) -> float:
        return round(self._total_cost, 6)
    
    @property
    def total_tokens(self) -> int:
        return self._total_tokens
    
    @property
    def remaining_budget(self) -> float:
        return self.daily_budget - self._total_cost
    
    @property
    def is_warning_triggered(self) -> bool:
        return self._total_cost >= self.daily_budget * 0.8
```

- [ ] **Step 9: 更新 DailyManager — 加入请假建议**

```python
# src/novel/core/workflow/daily_manager.py
from pydantic import BaseModel
from typing import Literal
from novel.core.workflow.cost_tracker import CostTracker
from novel.core.workflow.manuscript_store import ManuscriptStore

class ReserveStatus(BaseModel):
    level: Literal["green", "yellow", "red"]
    reserve_count: int
    
    @property
    def is_warning(self) -> bool:
        return self.level in ("yellow", "red")

class DailyUpdateManager:
    def __init__(
        self,
        written_chapters: int,
        published_chapters: int,
        mode: Literal["fast", "fine"] = "fine",
        daily_budget: float = 15.0,
    ):
        self.written_chapters = written_chapters
        self.published_chapters = published_chapters
        self.mode = mode
        self.cost_tracker = CostTracker(daily_budget=daily_budget)
        self.manuscript_store = ManuscriptStore()
        self._quality_scores = []
    
    def check_reserves(self) -> ReserveStatus:
        reserve = self.written_chapters - self.published_chapters
        
        if reserve >= 10:
            return ReserveStatus(level="green", reserve_count=reserve)
        elif reserve >= 6:
            return ReserveStatus(level="yellow", reserve_count=reserve)
        else:
            return ReserveStatus(level="red", reserve_count=reserve)
    
    def get_skill_pipeline(self) -> list[str]:
        status = self.check_reserves()
        
        # Emergency: force fast mode
        if status.level == "red":
            return ["flesh_out_chapter", "anti_ai_polish"]
        
        if self.mode == "fast":
            return ["flesh_out_chapter", "anti_ai_polish"]
        else:  # fine mode
            return [
                "flesh_out_chapter",
                "check_logic",
                "anti_ai_polish",
                "audit_hooks",
            ]
    
    def get_recommended_mode(self) -> Literal["fast", "fine"]:
        status = self.check_reserves()
        if status.level == "red":
            return "fast"
        return self.mode
    
    def record_quality_score(self, score: float) -> None:
        """记录章节质量评分（anti-ai-polish 五层综合分）"""
        self._quality_scores.append(score)
        # 只保留最近 3 章
        if len(self._quality_scores) > 3:
            self._quality_scores = self._quality_scores[-3:]
    
    def should_suggest_leave(self) -> bool:
        """连续 3 章质量评分低于 60 分，建议请假"""
        if len(self._quality_scores) < 3:
            return False
        return all(score < 60 for score in self._quality_scores[-3:])
```

- [ ] **Step 10: Commit**

```bash
git add src/novel/core/workflow/cost_tracker.py src/novel/core/workflow/daily_manager.py tests/core/workflow/
git commit -m "feat(workflow): add DailyUpdateManager with cost tracking and stock alerts

- CostTracker monitors daily LLM spend with configurable budget
- DailyUpdateManager checks manuscript reserves (green/yellow/red)
- Automatic mode switching: red alert forces fast mode
- Skill pipeline adapts to emergency status"
```

---

## Task 5: GenreRoute Gate — 品类路由门禁

**Files:**
- Create: `src/novel/core/genre/profile.py`
- Create: `tests/core/test_genre_profile.py`

- [ ] **Step 1: 创建 GenreProfile 测试**

```python
# tests/core/test_genre_profile.py
import pytest
from novel.core.genre.profile import GenreProfile, GenreRouter

def test_genre_profile_loading():
    """品类画像应该能正确加载"""
    profile = GenreProfile(
        genre_id="genre/urban",
        name="都市",
        weights={
            "face_slap": 0.9,
            "upgrade": 0.3,
            "romance": 0.6,
            "suspense": 0.4,
        },
        rhythm_params={
            "small_climax_interval": 5,
            "big_climax_interval": 20,
        },
        taboos=["主角长期受虐", "后宫修罗场"],
    )
    assert profile.genre_id == "genre/urban"
    assert profile.weights["face_slap"] == 0.9

def test_genre_router_enforces_profile():
    """品类路由门禁应该阻断未指定品类的创作任务"""
    router = GenreRouter()
    
    # 未设置品类时，应该阻断
    with pytest.raises(ValueError, match="genre_profile"):
        router.require_genre()
    
    # 设置品类后，应该通过
    router.set_genre("genre/urban")
    assert router.current_genre == "genre/urban"

def test_genre_router_blocks_missing_genre():
    """创作类 Skill 启动前必须检查品类"""
    router = GenreRouter()
    
    # 模拟创作 Skill 调用
    skill_name = "design_character"
    result = router.check_prerequisite(skill_name)
    assert result is False

CREATION_SKILLS = [
    "forge_golden_chapters",
    "ask_architect",
    "design_character",
    "design_paywall",
    "audit_hooks",
]

@pytest.mark.parametrize("skill_name", CREATION_SKILLS)
def test_genre_required_for_creation_skills(skill_name):
    """所有创作类 Skill 都需要品类画像"""
    router = GenreRouter()
    assert router.is_genre_required(skill_name) is True
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/core/test_genre_profile.py -v
```

Expected: FAIL

- [ ] **Step 3: 实现 GenreProfile 和 GenreRouter**

```python
# src/novel/core/genre/profile.py
from pydantic import BaseModel, Field

# 创作类 Skill 列表（需要品类画像）
CREATION_SKILLS = {
    "forge_golden_chapters",
    "ask_architect",
    "design_character",
    "design_paywall",
    "audit_hooks",
}

class GenreProfile(BaseModel):
    genre_id: str
    name: str
    weights: dict[str, float] = Field(default_factory=dict)
    rhythm_params: dict[str, int] = Field(default_factory=dict)
    taboos: list[str] = Field(default_factory=list)

class GenreRouter:
    def __init__(self):
        self._current_genre: str | None = None
    
    @property
    def current_genre(self) -> str | None:
        return self._current_genre
    
    def set_genre(self, genre_id: str) -> None:
        self._current_genre = genre_id
    
    def require_genre(self) -> str:
        """获取当前品类，未设置时抛出异常"""
        if self._current_genre is None:
            raise ValueError(
                "genre_profile is required. "
                "Please set genre before invoking creation skills."
            )
        return self._current_genre
    
    def is_genre_required(self, skill_name: str) -> bool:
        """判断某个 Skill 是否需要品类画像"""
        return skill_name in CREATION_SKILLS
    
    def check_prerequisite(self, skill_name: str) -> bool:
        """检查 Skill 的前置条件是否满足"""
        if not self.is_genre_required(skill_name):
            return True
        return self._current_genre is not None
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/core/test_genre_profile.py -v
```

Expected: 5 passed (含参数化的 3 个)

- [ ] **Step 5: Commit**

```bash
git add src/novel/core/genre/profile.py tests/core/test_genre_profile.py
git commit -m "feat(genre): add GenreProfile and GenreRouter for category-driven creation

- GenreProfile stores weights, rhythm params, and taboos per genre
- GenreRouter enforces genre prerequisite for creation skills
- Blocks creation skills from running without genre_profile set
- Covers: forge_golden_chapters, ask_architect, design_character, etc."
```

---

## Task 6: DesignPaywall Skill — 付费卡点设计师

**Files:**
- Create: `src/novel/core/skills/design_paywall.py`
- Create: `tests/core/skills/test_design_paywall.py`

- [ ] **Step 1: 创建测试**

```python
# tests/core/skills/test_design_paywall.py
import pytest
from novel.core.skills.design_paywall import DesignPaywallSkill, PaywallAnalysis

@pytest.fixture
def skill():
    return DesignPaywallSkill()

@pytest.mark.asyncio
async def test_ideal_paywall_position(skill):
    """理想卡点：爽点兑现后 + 新悬念抛出"""
    outline = """
    第1-10章：主角受辱，获得金手指
    第11-20章：首次反击，小试牛刀
    第21-30章：打败小反派，名声大振
    第31-40章：大反派出现，危机降临
    第41-50章：主角陷入绝境
    """
    analysis = await skill.analyze_outline(outline)
    # 理想卡点应该在 20-30 章之间（爽点刚兑现，新危机刚出现）
    assert 20 <= analysis.recommended_chapter <= 30

@pytest.mark.asyncio
async def test_bad_paywall_position_warning(skill):
    """错误卡点：主角低谷期"""
    outline = """
    第1-20章：主角一路高歌猛进
    第21-40章：主角被陷害，陷入绝境，失去一切
    第41-60章：主角重新崛起
    """
    analysis = await skill.analyze_outline(outline, current_chapter=30)
    assert analysis.warning is not None
    assert "低谷" in analysis.warning or "绝境" in analysis.warning

@pytest.mark.asyncio
async def test_free_chapter_ending_design(skill):
    """免费末章设计：必须爽点+悬念双保险"""
    chapter_text = "陈凡一拳轰飞对手，全场寂静。'还有谁？'他冷冷扫视众人。就在这时，一道阴冷的声音从暗处传来：'小子，你惹了不该惹的人……'"
    verdict = await skill.evaluate(chapter_text)
    assert verdict.passed is True
    assert verdict.layer_scores.get("hook", 0) >= 70

def test_paywall_analysis_schema():
    analysis = PaywallAnalysis(
        recommended_chapter=25,
        confidence=0.85,
        reasoning="爽点兑现后，新危机刚抛出",
        warning=None,
    )
    assert analysis.recommended_chapter == 25
    assert analysis.confidence == 0.85
```

- [ ] **Step 2: 运行测试确认失败**

```bash
pytest tests/core/skills/test_design_paywall.py -v
```

Expected: FAIL

- [ ] **Step 3: 实现 DesignPaywallSkill**

```python
# src/novel/core/skills/design_paywall.py
import re
from pydantic import BaseModel, Field
from novel.core.skills.base import BaseCommercialSkill, CommercialVerdict, SkillResult, TokenUsage

class PaywallAnalysis(BaseModel):
    recommended_chapter: int
    confidence: float = Field(ge=0, le=1)
    reasoning: str
    warning: str | None = None

class DesignPaywallSkill(BaseCommercialSkill):
    name = "design_paywall"
    
    # 爽点关键词
    CLIMAX_KEYWORDS = ["击败", "胜利", "突破", "升级", "反杀", "扬名"]
    # 悬念关键词
    SUSPENSE_KEYWORDS = ["危机", "黑手", "阴谋", "难道", "不可能", "竟"]
    # 低谷关键词
    LOW_KEYWORDS = ["陷入绝境", "失去一切", "被陷害", "跌落", "绝望"]
    
    async def evaluate(self, text: str, context: dict | None = None) -> CommercialVerdict:
        """评估章节是否适合作为付费过渡章"""
        layer_scores = {}
        diagnostics = []
        
        # 检测爽点
        climax_count = sum(1 for kw in self.CLIMAX_KEYWORDS if kw in text)
        layer_scores["climax"] = min(100, climax_count * 25)
        
        # 检测悬念
        suspense_count = sum(1 for kw in self.SUSPENSE_KEYWORDS if kw in text)
        layer_scores["hook"] = min(100, suspense_count * 20)
        
        # 综合判定
        avg_score = sum(layer_scores.values()) / len(layer_scores)
        passed = avg_score >= 60
        
        if not passed:
            diagnostics.append(f"付费过渡章：爽点或悬念不足，综合评分 {avg_score:.0f}/100")
        
        return CommercialVerdict(
            passed=passed,
            diagnostics=diagnostics,
            layer_scores=layer_scores,
        )
    
    async def analyze_outline(
        self, outline: str, current_chapter: int | None = None
    ) -> PaywallAnalysis:
        """分析大纲，推荐付费卡点位置"""
        lines = outline.strip().split("\n")
        
        climax_positions = []
        low_positions = []
        
        for i, line in enumerate(lines):
            if any(kw in line for kw in self.CLIMAX_KEYWORDS):
                climax_positions.append(i)
            if any(kw in line for kw in self.LOW_KEYWORDS):
                low_positions.append(i)
        
        # 推荐卡点：爽点后，低谷前
        if climax_positions and low_positions:
            best_pos = climax_positions[0]
            # 如果当前章节已经在低谷期，发出警告
            if current_chapter and current_chapter > best_pos:
                warning = "当前处于主角低谷期，不建议在此处切付费"
            else:
                warning = None
            return PaywallAnalysis(
                recommended_chapter=(best_pos + 1) * 10,
                confidence=0.85,
                reasoning="爽点兑现后，新危机刚抛出",
                warning=warning,
            )
        
        # 默认推荐中间位置
        return PaywallAnalysis(
            recommended_chapter=len(lines) * 5,
            confidence=0.5,
            reasoning="未找到明显爽点，推荐中间位置",
            warning="大纲缺少明显爽点，建议优化",
        )
    
    async def fix(self, text: str, verdict: CommercialVerdict) -> SkillResult:
        # 实际实现中会调用 LLM 优化过渡章
        return SkillResult(text=text, token_usage=TokenUsage())
```

- [ ] **Step 4: 运行测试确认通过**

```bash
pytest tests/core/skills/test_design_paywall.py -v
```

Expected: 4 passed

- [ ] **Step 5: Commit**

```bash
git add src/novel/core/skills/design_paywall.py tests/core/skills/test_design_paywall.py
git commit -m "feat(skills): add DesignPaywallSkill for paywall position analysis

- Analyze outline to find optimal paywall cut point
- Detect ideal position: after climax, before new crisis
- Warn against cutting during protagonist's low point
- Evaluate transition chapter quality (climax + hook)"
```

---

## Phase 1 里程碑验收

- [ ] **Step 1: 运行所有 P0 测试**

```bash
pytest tests/core/skills/test_base.py tests/core/skills/test_anti_ai_polish.py tests/core/skills/test_audit_hooks.py tests/core/skills/test_design_paywall.py tests/core/workflow/ tests/core/test_genre_profile.py -v
```

Expected: 28 passed (4 base + 6 anti-ai + 4 hooks + 4 paywall + 9 workflow + 5 genre)

- [ ] **Step 2: 检查覆盖率**

```bash
pytest tests/core/skills/ tests/core/workflow/ tests/core/test_genre_profile.py --cov=src/novel/core/skills --cov=src/novel/core/workflow --cov=src/novel/core/genre --cov-report=term-missing
```

Expected: Coverage > 85%

- [ ] **Step 3: 手动集成测试（可选）**

```bash
# 创建一个简单的端到端测试脚本
python -c "
from novel.core.skills.anti_ai_polish import AntiAiPolishSkill
from novel.core.skills.audit_hooks import AuditHooksSkill
from novel.core.skills.design_paywall import DesignPaywallSkill
from novel.core.workflow.daily_manager import DailyUpdateManager
from novel.core.workflow.manuscript_store import ManuscriptStore, ManuscriptTier
from novel.core.genre.profile import GenreProfile, GenreRouter

# Test AntiAiPolish
skill = AntiAiPolishSkill()
print('AntiAiPolishSkill loaded OK')

# Test AuditHooks
hooks = AuditHooksSkill()
print('AuditHooksSkill loaded OK')

# Test DesignPaywall
paywall = DesignPaywallSkill()
print('DesignPaywallSkill loaded OK')

# Test DailyManager
manager = DailyUpdateManager(written_chapters=110, published_chapters=100, mode='fast')
status = manager.check_reserves()
print(f'DailyManager OK: {status.level}, reserve={status.reserve_count}')

# Test ManuscriptStore
store = ManuscriptStore()
store.add('chapter_101', ManuscriptTier.REFINED)
print(f'ManuscriptStore OK: total={store.total_count}')

# Test GenreRouter
router = GenreRouter()
router.set_genre('genre/urban')
print(f'GenreRouter OK: genre={router.current_genre}')

print('Phase 1 P0 skills ready!')
"
```

Expected: All imports succeed, Phase 1 P0 skills ready!

---

# Phase 2-4: 后续规划（概要）

由于 Phase 2-4 涉及大量新增功能（品类画像、套路模板库、黄金三章、选题侦察等），且部分依赖 `novel-material` 项目的配合，我们将在 **Phase 1 通过验收后** 再详细展开 TDD 任务拆解。

**Phase 2 (P1) 预期交付：**
- `forge-golden-chapters`：微节拍控制器，品类适配开篇
- `scout-topic`：榜单分析，手动数据导入
- `design-character`：爽感维度权重，品类画像关联

**Phase 3 (P2) 预期交付：**
- `ask-architect`：套路模板调用，量化张力曲线
- `analyze-stats`：付费转化率分析
- `flesh-out-chapter`：Beat Sheet 机制
- `check-logic`：增强事实核查

**Phase 4 (横切关注) 预期交付：**
- `GenreProfile` 系统：品类画像配置与加载
- `TropeTemplate` 库：6 个首批模板（扮猪吃虎、退婚流等）
- `CommercialGates`：Token 预算、品类路由、存稿应急协议

---

## 验收标准总结

| 阶段 | 核心能力 | 验收指标 |
|------|---------|---------|
| Phase 1 | P0 生存红线 | 28 个测试通过，覆盖率 >85% |
| Phase 2 | P1 破局增效 | 黄金三章 + 选题 + 人设完成 |
| Phase 3 | P2 长线保障 | 架构师 + 数据诊断 + 扩写 + 核查完成 |
| Phase 4 | 横切关注 | 品类画像 + 套路模板 + 质量门禁完成 |

Phase 1 完成后，系统即具备商业化运作的最基本能力：能写、能查、能控成本、能管存稿。
