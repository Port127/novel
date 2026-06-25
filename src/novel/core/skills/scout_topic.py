from typing import Any
from pydantic import BaseModel, Field
from novel.core.skills.base import BaseCommercialSkill, CommercialVerdict, SkillResult, TokenUsage

class MarketData(BaseModel):
    genre: str
    tag_combinations: list[str]
    competition_level: float = Field(ge=0, le=1, description="竞争程度")
    potential_score: float = Field(ge=0, le=1, description="潜力评分")
    saturation_score: float = Field(ge=0, le=1, description="饱和度")
    recommended_window: str

class TopicAnalysis(BaseModel):
    market_data: MarketData
    recommendation_score: float = Field(ge=0, le=1)
    recommendation_reason: str
    risks: list[str]
    passed: bool

class ScoutTopicSkill(BaseCommercialSkill):
    """选题侦察兵 - 分析市场数据，推荐高潜力选题"""
    
    name = "scout_topic"
    
    async def evaluate(self, text: str, context: dict | None = None) -> CommercialVerdict:
        """评估选题文本（此技能主要用于分析，evaluate 返回通过）"""
        return CommercialVerdict(
            passed=True,
            diagnostics=["选题侦察兵主要用于市场分析，文本评估始终通过"],
            layer_scores={"relevance": 100.0},
            severity="info"
        )
    
    async def fix(self, text: str, verdict: CommercialVerdict) -> SkillResult:
        """修复文本（此技能不修改文本）"""
        return SkillResult(text=text, token_usage=TokenUsage())
    
    async def analyze_market(self, genre: str, ranking_data: list[dict]) -> MarketData | None:
        """分析市场数据"""
        if not ranking_data:
            return None
        
        # 提取所有标签
        all_tags = []
        for book in ranking_data:
            all_tags.extend(book.get("tags", []))
        
        # 统计标签频率
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # 取前5个高频标签作为标签组合
        tag_combinations = sorted(tag_counts.keys(), key=lambda t: tag_counts[t], reverse=True)[:5]
        
        # 计算竞争度（基于榜单书籍数量和读者数）
        total_readers = sum(book.get("readers", 0) for book in ranking_data)
        avg_readers = total_readers / len(ranking_data) if ranking_data else 0
        competition_level = min(1.0, len(ranking_data) / 10)  # 10本书以上认为高竞争
        
        # 计算潜力值（基于读者数和标签多样性）
        potential_score = min(1.0, avg_readers / 100000)  # 10万读者为满分
        if len(tag_combinations) >= 3:
            potential_score = min(1.0, potential_score + 0.2)
        
        # 计算饱和度（基于标签集中度）
        top_tag_ratio = tag_counts.get(tag_combinations[0], 0) / len(all_tags) if all_tags else 0
        saturation_score = min(1.0, top_tag_ratio * 2)
        
        # 推荐窗口
        if competition_level < 0.5 and potential_score > 0.7:
            recommended_window = "3-6个月"
        elif competition_level < 0.7:
            recommended_window = "6-12个月"
        else:
            recommended_window = "12个月以上"
        
        return MarketData(
            genre=genre,
            tag_combinations=tag_combinations,
            competition_level=competition_level,
            potential_score=potential_score,
            saturation_score=saturation_score,
            recommended_window=recommended_window
        )
    
    async def recommend_topic(self, market_data: MarketData) -> TopicAnalysis:
        """基于市场数据推荐选题"""
        # 计算推荐分数
        recommendation_score = (
            market_data.potential_score * 0.5 +
            (1 - market_data.competition_level) * 0.3 +
            (1 - market_data.saturation_score) * 0.2
        )
        
        # 判断是否通过（推荐分数 > 0.7）
        passed = recommendation_score > 0.7
        
        # 生成推荐原因
        if passed:
            if market_data.competition_level < 0.5:
                recommendation_reason = "低竞争高潜力，适合切入"
            else:
                recommendation_reason = "市场潜力大，需要差异化策略"
        else:
            if market_data.competition_level > 0.7:
                recommendation_reason = "竞争过于激烈，饱和度较高"
            else:
                recommendation_reason = "潜力不足或竞争中等，需谨慎评估"
        
        # 识别风险
        risks = []
        if market_data.saturation_score > 0.7:
            risks.append("市场饱和度高，难以脱颖而出")
        if market_data.competition_level > 0.7:
            risks.append("竞争激烈，需要快速建立差异化")
        if market_data.potential_score < 0.5:
            risks.append("市场潜力有限，增长空间小")
        
        return TopicAnalysis(
            market_data=market_data,
            recommendation_score=recommendation_score,
            recommendation_reason=recommendation_reason,
            risks=risks,
            passed=passed
        )
