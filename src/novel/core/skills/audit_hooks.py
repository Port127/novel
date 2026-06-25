from pydantic import BaseModel, Field
from novel.core.skills.base import BaseCommercialSkill, CommercialVerdict, SkillResult, TokenUsage

# 悬念关键词
SUSPENSE_KEYWORDS = [
    "竟", "没想到", "突然", "刹那", "瞳孔骤缩", "震惊",
    "难道", "不可能", "怎么可能", "背后", "秘密", "真相",
]

# 冲突关键词
CONFLICT_KEYWORDS = [
    "杀", "战", "怒", "吼", "拳", "剑", "血", "死",
    "冲突", "对抗", "危机", "险境", "绝境", "爆",
]

# 标题悬念模式
TITLE_PATTERNS = [
    "……", "!", "？", "竟", "难道", "谁", "何", "怎",
    "秘密", "真相", "背后", "黑手", "！"
]

# 标题动作/冲突词
TITLE_ACTION_WORDS = [
    "斩", "杀", "破", "战", "爆", "怒", "冲", "灭",
    "逆天", "无敌", "绝世", "至尊", "巅峰",
]

class HookAnalysis(BaseModel):
    hook_type: str = Field(description="钩子类型：crisis/reversal/mystery")
    suspense_level: int = Field(ge=0, le=10, description="悬念强度 0-10")
    clickbait_score: int = Field(ge=0, le=100, description="标题点击吸引力 0-100")
    suggested_titles: list[str] = Field(default_factory=list)

class AuditHooksSkill(BaseCommercialSkill):
    name = "audit_hooks"
    
    async def evaluate(self, text: str, context: dict | None = None) -> CommercialVerdict:
        """评估章节结尾的悬念钩子和全文冲突密度"""
        diagnostics = []
        layer_scores = {}
        
        # 检测最后 800 字符的悬念钩子
        ending = text[-800:] if len(text) > 800 else text
        suspense_score = self._calculate_suspense_score(ending)
        layer_scores["hook"] = suspense_score
        
        if suspense_score < 60:
            diagnostics.append(f"章末钩子：平淡结尾，悬念强度仅 {suspense_score}/100")
        
        # 检测全文冲突密度
        conflict_density = self._calculate_conflict_density(text)
        layer_scores["conflict_density"] = conflict_density
        
        if conflict_density < 60:
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
        # 检测悬念标点模式
        pattern_matches = sum(1 for p in TITLE_PATTERNS if p in title)
        # 检测动作/冲突词
        action_matches = sum(1 for w in TITLE_ACTION_WORDS if w in title)
        
        # 综合评分：标点模式 + 动作词（动作词权重较低）
        clickbait_score = min(100, pattern_matches * 30 + action_matches * 15)
        
        # 生成建议标题
        suggested = []
        if clickbait_score < 60:
            suggested = ["他竟是……", "背后的真相"]
        
        # 判断钩子类型
        if "？" in title or "?" in title:
            hook_type = "mystery"
        elif "！" in title or "!" in title:
            hook_type = "crisis"
        else:
            hook_type = "reversal"
        
        return HookAnalysis(
            hook_type=hook_type,
            suspense_level=min(10, pattern_matches * 3 + action_matches * 2),
            clickbait_score=clickbait_score,
            suggested_titles=suggested,
        )
    
    async def fix(self, text: str, verdict: CommercialVerdict) -> SkillResult:
        """根据诊断结果提供修复建议（实际修复需要 LLM 介入）"""
        # 当前版本仅提供诊断，不自动修复
        return SkillResult(text=text, token_usage=TokenUsage())
    
    def _calculate_suspense_score(self, ending: str) -> int:
        """计算结尾的悬念强度（0-100）"""
        keyword_count = sum(1 for kw in SUSPENSE_KEYWORDS if kw in ending)
        
        # 检查是否有疑问句或感叹句结尾
        has_question = ending.strip().endswith(("？", "?"))
        has_exclamation = ending.strip().endswith(("！", "!"))
        has_ellipsis = ending.strip().endswith(("……", "..."))
        
        score = keyword_count * 15
        if has_question:
            score += 20
        if has_exclamation:
            score += 15
        if has_ellipsis:
            score += 25  # 省略号是最强的悬念标记
        
        return min(100, score)
    
    def _calculate_conflict_density(self, text: str) -> int:
        """计算全文的冲突密度（0-100）"""
        if not text:
            return 0
        
        keyword_count = sum(1 for kw in CONFLICT_KEYWORDS if kw in text)
        char_count = len(text)
        
        # 每 1000 字符的冲突关键词数
        density = (keyword_count / char_count) * 1000 if char_count > 0 else 0
        
        # 转换为 0-100 分（假设每 1000 字符 3 个冲突词为满分）
        score = min(100, int(density * 33))
        
        return score
