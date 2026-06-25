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
