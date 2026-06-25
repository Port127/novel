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
    """低冲突密度应该触发警告"""
    # 生成一段平淡文本
    bland_text = "他走在路上，看着风景，想着心事。" * 50
    verdict = await skill.evaluate(bland_text)
    assert verdict.layer_scores["conflict_density"] < 60

@pytest.mark.asyncio
async def test_chapter_title_detection(skill):
    """章节标题应该包含悬念或冲突"""
    good_titles = ["他竟是……", "谁在背后操纵？", "一刀斩破苍穹！"]
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
    
    # 验证 suspense_level 可以为 0（无悬念标题）
    analysis_zero = HookAnalysis(
        hook_type="reversal",
        suspense_level=0,
        clickbait_score=20,
        suggested_titles=[],
    )
    assert analysis_zero.suspense_level == 0
