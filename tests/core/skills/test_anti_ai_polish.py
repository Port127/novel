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
    text = '"妈的！"陈凡一拳砸在桌上，"你敢动我妹妹，老子今天跟你拼了！"他双眼血红，像一头发疯的野兽冲了上去。'
    verdict = await skill.evaluate(text)
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
