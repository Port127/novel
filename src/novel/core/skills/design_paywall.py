from pydantic import BaseModel
from novel.core.skills.base import BaseCommercialSkill, CommercialVerdict, SkillResult, TokenUsage

class PaywallAnalysis(BaseModel):
    recommended_chapter: int
    confidence: float
    reasoning: str
    warning: str | None = None

class DesignPaywallSkill(BaseCommercialSkill):
    """付费卡点设计师：分析大纲，推荐最优付费切割点"""
    
    name = "design_paywall"
    
    # 爽点关键词
    CLIMAX_KEYWORDS = ["击败", "胜利", "突破", "升级", "反杀", "扬名", "名声大振", "轰飞", "高歌猛进"]
    # 悬念关键词
    SUSPENSE_KEYWORDS = ["危机", "黑手", "阴谋", "难道", "不可能", "竟", "惹了不该惹的人", "不该惹的人"]
    # 低谷关键词
    LOW_KEYWORDS = ["陷入绝境", "失去一切", "被陷害", "跌落", "绝望"]
    
    async def evaluate(self, text: str, context: dict | None = None) -> CommercialVerdict:
        """评估章节是否适合作为付费过渡章"""
        layer_scores = {}
        diagnostics = []
        
        # 检测爽点
        climax_count = sum(1 for kw in self.CLIMAX_KEYWORDS if kw in text)
        layer_scores["climax"] = min(100, climax_count * 50)
        
        # 检测悬念
        suspense_count = sum(1 for kw in self.SUSPENSE_KEYWORDS if kw in text)
        layer_scores["hook"] = min(100, suspense_count * 40)
        
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
        """根据诊断结果提供修复建议"""
        # 当前版本仅提供诊断，不自动修复
        return SkillResult(text=text, token_usage=TokenUsage())
