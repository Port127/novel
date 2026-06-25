import pytest
from novel.core.skills.forge_golden_chapters import (
    ForgeGoldenChaptersSkill,
    GoldenChapterAnalysis,
    MicroBeat,
)

@pytest.fixture
def skill():
    return ForgeGoldenChaptersSkill()

def test_golden_chapter_analysis_schema():
    """验证分析 Schema"""
    beat = MicroBeat(
        beat_id="opening_hook",
        description="主角受辱，引发读者同情",
        target_words=300,
        emotion_target="压抑",
    )
    analysis = GoldenChapterAnalysis(
        chapter_number=1,
        first_conflict_at_word=250,
        has_character_setup=True,
        has_golden_finger=True,
        has_first_climax=True,
        beats=[beat],
        overall_score=85.0,
        passed=True,
    )
    assert analysis.chapter_number == 1
    assert analysis.first_conflict_at_word == 250
    assert analysis.overall_score == 85.0
    assert analysis.passed is True
    assert len(analysis.beats) == 1

def test_micro_beat_schema():
    """验证微节拍 Schema"""
    beat = MicroBeat(
        beat_id="hook",
        description="开头悬念",
        target_words=200,
        emotion_target="好奇",
    )
    assert beat.beat_id == "hook"
    assert beat.target_words == 200

@pytest.mark.asyncio
async def test_xuanhuan_template(skill):
    """玄幻品类应加载正确的开篇模板"""
    template = skill.get_genre_template("genre/xuanhuan")
    assert template is not None
    assert template.genre_id == "genre/xuanhuan"
    assert len(template.micro_beats) >= 3
    # 玄幻标准套路：废柴受辱 → 金手指觉醒 → 首次反击
    beat_ids = [b.beat_id for b in template.micro_beats]
    assert "humiliation" in beat_ids
    assert "golden_finger_awakening" in beat_ids
    assert "first_counterattack" in beat_ids

def test_urban_template(skill):
    """都市品类应加载正确的开篇模板"""
    template = skill.get_genre_template("genre/urban")
    assert template is not None
    assert template.genre_id == "genre/urban"
    beat_ids = [b.beat_id for b in template.micro_beats]
    assert "betrayal" in beat_ids
    assert "identity_reveal" in beat_ids
    assert "face_slap" in beat_ids

def test_system_template(skill):
    """系统文品类应加载正确的开篇模板"""
    template = skill.get_genre_template("genre/system")
    assert template is not None
    assert template.genre_id == "genre/system"
    beat_ids = [b.beat_id for b in template.micro_beats]
    assert "system_activation" in beat_ids
    assert "first_mission" in beat_ids
    assert "reward_crush" in beat_ids

def test_unknown_genre_returns_none(skill):
    """未知品类应返回 None"""
    template = skill.get_genre_template("genre/unknown")
    assert template is None

@pytest.mark.asyncio
async def test_validate_chapter_passes_good_structure(skill):
    """结构良好的第一章应通过验证"""
    text = (
        "陈凡站在家族大殿中央，周围是嘲笑的目光。"
        "'废物！连炼气一层都突破不了！'族长大喝一声，"
        "一掌将他拍飞出去。"
        "就在他即将昏迷的刹那，脑海中突然响起一道冰冷的声音："
        "'叮！万界吞噬系统激活！'"
        "一股恐怖的力量从丹田深处涌出，"
        "陈凡的气息瞬间突破了炼气三层！"
        "全场震惊！"
    )
    analysis = await skill.validate_chapter(text, chapter_number=1, genre_id="genre/xuanhuan")
    assert analysis.passed is True
    assert analysis.first_conflict_at_word <= 300
    assert analysis.has_character_setup is True
    assert analysis.has_golden_finger is True
    assert analysis.has_first_climax is True

@pytest.mark.asyncio
async def test_validate_chapter_fails_slow_opening(skill):
    """开篇过慢应失败"""
    text = (
        "这是一个阳光明媚的早晨，陈凡走在去往学院的路上。"
        "路上遇到了很多同学，大家互相打招呼。"
        "学院里今天有一场重要的考试，陈凡心里有些紧张。"
        "他坐在教室里，看着窗外的风景，思绪飘得很远。"
        "老师开始发卷子，陈凡拿起笔，准备答题。"
        "他认真地做着每一道题，时间一分一秒地过去。"
        "终于做完了，他长舒一口气，交了卷子。"
        "走出教室，他看到天空中的云彩，心情很好。"
    )
    analysis = await skill.validate_chapter(text, chapter_number=1, genre_id="genre/xuanhuan")
    assert analysis.passed is False
    assert analysis.first_conflict_at_word > 300
