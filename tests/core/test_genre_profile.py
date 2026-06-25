import pytest
from novel.core.genre.profile import GenreProfile, GenreRouter

def test_genre_profile_loading():
    """品类画像应该能正确加载"""
    profile = GenreProfile(
        genre_id="genre/urban",
        name="都市",
        weights={
            "face_slap": 0.9,
            "upgrade": 0.3,
            "romance": 0.6,
            "suspense": 0.4,
        },
        rhythm_params={
            "small_climax_interval": 5,
            "big_climax_interval": 20,
        },
        taboos=["主角长期受虐", "后宫修罗场"],
    )
    assert profile.genre_id == "genre/urban"
    assert profile.weights["face_slap"] == 0.9

def test_genre_router_enforces_profile():
    """品类路由门禁应该阻断未指定品类的创作任务"""
    router = GenreRouter()
    
    # 未设置品类时，应该阻断
    with pytest.raises(ValueError, match="genre_profile"):
        router.require_genre()
    
    # 设置品类后，应该通过
    router.set_genre("genre/urban")
    assert router.current_genre == "genre/urban"

def test_genre_router_blocks_missing_genre():
    """创作类 Skill 启动前必须检查品类"""
    router = GenreRouter()
    
    # 模拟创作 Skill 调用
    skill_name = "design_character"
    result = router.check_prerequisite(skill_name)
    assert result is False

CREATION_SKILLS = [
    "forge_golden_chapters",
    "ask_architect",
    "design_character",
    "design_paywall",
    "audit_hooks",
]

@pytest.mark.parametrize("skill_name", CREATION_SKILLS)
def test_genre_required_for_creation_skills(skill_name):
    """所有创作类 Skill 都需要品类画像"""
    router = GenreRouter()
    assert router.is_genre_required(skill_name) is True
