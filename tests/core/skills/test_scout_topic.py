import pytest
from novel.core.skills.scout_topic import ScoutTopicSkill, TopicAnalysis, MarketData

@pytest.fixture
def skill():
    return ScoutTopicSkill()

def test_market_data_schema():
    """验证市场数据 Schema"""
    data = MarketData(
        genre="玄幻",
        tag_combinations=["废柴流", "系统流", "重生流"],
        competition_level=0.7,
        potential_score=0.8,
        saturation_score=0.6,
        recommended_window="3-6个月",
    )
    assert data.genre == "玄幻"
    assert len(data.tag_combinations) == 3
    assert data.competition_level == 0.7
    assert data.potential_score == 0.8

def test_topic_analysis_schema():
    """验证选题分析 Schema"""
    analysis = TopicAnalysis(
        market_data=MarketData(
            genre="都市",
            tag_combinations=["重生", "商战"],
            competition_level=0.5,
            potential_score=0.7,
            saturation_score=0.4,
            recommended_window="6-12个月",
        ),
        recommendation_score=0.75,
        recommendation_reason="低竞争高潜力，适合切入",
        risks=["需要快速建立差异化"],
        passed=True,
    )
    assert analysis.recommendation_score == 0.75
    assert analysis.passed is True

@pytest.mark.asyncio
async def test_analyze_urban_genre(skill):
    """分析都市品类市场数据"""
    ranking_data = [
        {"title": "重生之商业帝国", "tags": ["重生", "商战", "都市"], "readers": 50000},
        {"title": "都市最强战神", "tags": ["战神", "都市", "打脸"], "readers": 45000},
        {"title": "神级奶爸", "tags": ["奶爸", "都市", "温馨"], "readers": 40000},
    ]
    
    analysis = await skill.analyze_market("都市", ranking_data)
    assert analysis is not None
    assert analysis.genre == "都市"
    assert len(analysis.tag_combinations) > 0
    assert 0 <= analysis.competition_level <= 1
    assert 0 <= analysis.potential_score <= 1

@pytest.mark.asyncio
async def test_analyze_xuanhuan_genre(skill):
    """分析玄幻品类市场数据"""
    ranking_data = [
        {"title": "斗破苍穹", "tags": ["玄幻", "废柴流", "升级"], "readers": 100000},
        {"title": "武动乾坤", "tags": ["玄幻", "升级", "战斗"], "readers": 80000},
        {"title": "大主宰", "tags": ["玄幻", "升级", "热血"], "readers": 70000},
    ]
    
    analysis = await skill.analyze_market("玄幻", ranking_data)
    assert analysis is not None
    assert analysis.genre == "玄幻"
    assert "升级" in analysis.tag_combinations or "玄幻" in analysis.tag_combinations

@pytest.mark.asyncio
async def test_recommend_topic_high_potential(skill):
    """推荐高潜力选题"""
    market_data = MarketData(
        genre="系统文",
        tag_combinations=["系统", "任务", "奖励"],
        competition_level=0.3,
        potential_score=0.9,
        saturation_score=0.2,
        recommended_window="3-6个月",
    )
    
    recommendation = await skill.recommend_topic(market_data)
    assert recommendation is not None
    assert recommendation.recommendation_score >= 0.7
    assert recommendation.passed is True
    assert "潜力" in recommendation.recommendation_reason or "竞争" in recommendation.recommendation_reason

@pytest.mark.asyncio
async def test_recommend_topic_high_competition(skill):
    """高竞争市场应该谨慎推荐"""
    market_data = MarketData(
        genre="玄幻",
        tag_combinations=["升级", "废柴流"],
        competition_level=0.9,
        potential_score=0.6,
        saturation_score=0.8,
        recommended_window="12个月以上",
    )
    
    recommendation = await skill.recommend_topic(market_data)
    assert recommendation is not None
    assert recommendation.recommendation_score < 0.7
    assert recommendation.passed is False
    assert "竞争" in recommendation.recommendation_reason or "饱和" in recommendation.recommendation_reason

@pytest.mark.asyncio
async def test_empty_ranking_data(skill):
    """空榜单数据应该返回 None"""
    analysis = await skill.analyze_market("都市", [])
    assert analysis is None
