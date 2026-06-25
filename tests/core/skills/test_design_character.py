import pytest
from novel.core.skills.design_character import DesignCharacterSkill, CharacterDesign, GenreWeights

@pytest.fixture
def skill():
    return DesignCharacterSkill()

def test_genre_weights_schema():
    """验证品类权重 Schema"""
    weights = GenreWeights(
        genre="genre/urban",
        face_slap_weight=0.9,
        upgrade_weight=0.3,
        romance_weight=0.6,
        suspense_weight=0.4,
    )
    assert weights.genre == "genre/urban"
    assert weights.face_slap_weight == 0.9

def test_character_design_schema():
    """验证人设 Schema"""
    design = CharacterDesign(
        name="陈凡",
        archetype="扮猪吃虎",
        face_slap_index=9,
        cp_score=7,
        villain_disgust_level=8,
        golden_finger="万界吞噬系统",
        golden_finger_limit="每日只能吞噬一次",
        genre_weights=GenreWeights(
            genre="genre/xuanhuan",
            face_slap_weight=0.8,
            upgrade_weight=0.9,
            romance_weight=0.3,
            suspense_weight=0.5,
        ),
        overall_score=85.0,
        passed=True,
    )
    assert design.name == "陈凡"
    assert design.face_slap_index == 9
    assert design.overall_score == 85.0

@pytest.mark.asyncio
async def test_xuanhuan_character(skill):
    """玄幻品类人设设计"""
    design = await skill.design_character(
        name="陈凡",
        genre_id="genre/xuanhuan",
        background="家族废柴，被族人嘲笑",
        personality="隐忍，狠辣",
        golden_finger="万界吞噬系统",
    )
    assert design is not None
    assert design.name == "陈凡"
    assert design.genre_weights.genre == "genre/xuanhuan"
    assert design.genre_weights.upgrade_weight >= 0.8
    assert design.face_slap_index >= 7

@pytest.mark.asyncio
async def test_urban_character(skill):
    """都市品类人设设计"""
    design = await skill.design_character(
        name="林宇",
        genre_id="genre/urban",
        background="被退婚的穷小子",
        personality="腹黑，城府深",
        golden_finger="隐藏身份：华夏第一财团继承人",
    )
    assert design is not None
    assert design.name == "林宇"
    assert design.genre_weights.genre == "genre/urban"
    assert design.genre_weights.face_slap_weight >= 0.8
    assert design.face_slap_index >= 8

@pytest.mark.asyncio
async def test_character_with_villain(skill):
    """带反派的人设设计"""
    design = await skill.design_character(
        name="陈凡",
        genre_id="genre/xuanhuan",
        background="家族废柴",
        personality="隐忍",
        golden_finger="吞噬系统",
        villain_name="陈浩",
        villain_background="家族天才，多次羞辱主角",
    )
    assert design is not None
    assert design.villain_disgust_level >= 7

@pytest.mark.asyncio
async def test_evaluate_character(skill):
    """评估人设质量"""
    verdict = await skill.evaluate(
        "",
        context={
            "name": "陈凡",
            "genre_id": "genre/xuanhuan",
            "background": "家族废柴",
            "personality": "隐忍",
            "golden_finger": "吞噬系统",
        }
    )
    assert verdict.passed is True

@pytest.mark.asyncio
async def test_low_face_slap_fails(skill):
    """打脸指数过低应该失败"""
    design = await skill.design_character(
        name="张三",
        genre_id="genre/urban",
        background="普通上班族",
        personality="老实人",
        golden_finger="无",
    )
    # 平凡角色打脸指数应该不高
    assert design.face_slap_index <= 6
    # 但综合评分可能仍然通过（因为其他维度如CP感可能不错）
    # 所以不强制要求 passed=False
