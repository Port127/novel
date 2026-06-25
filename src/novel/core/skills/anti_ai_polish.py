import re
from pydantic import BaseModel, Field
from novel.core.skills.base import BaseCommercialSkill, CommercialVerdict, SkillResult, TokenUsage

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
        
        # Layer 2: 句式层（检测连续四字/六字短语排比）
        # 将文本按标点拆分，统计 4-6 字纯中文短语的连续出现次数
        segments = re.split(r'[，,。！？；:]', text)
        chinese_4_6_count = sum(
            1 for s in segments
            if s and len(s) >= 4 and len(s) <= 6 and re.match(r'^[\u4e00-\u9fff]+$', s)
        )
        if chinese_4_6_count >= 3:
            layer_scores["syntax"] = 40
            diagnostics.append("句式层：连续短语排比过多，句式单调")
        else:
            layer_scores["syntax"] = 80
        
        # Layer 3: 段落层
        has_summary = any(re.search(p, text) for p in SUMMARY_PATTERNS)
        layer_scores["paragraph"] = 40 if has_summary else 80
        if has_summary:
            diagnostics.append("段落层：检测到强行总结升华")
        
        # Layer 4: 叙事层（简化：检查对话占比）
        dialogue_ratio = len(re.findall(r"[\u201c\u300c](.*?)[\u201d\u300d]", text)) / max(len(text), 1)
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
