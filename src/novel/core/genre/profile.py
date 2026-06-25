from pydantic import BaseModel, Field

# 创作类 Skill 列表（需要品类画像）
CREATION_SKILLS = {
    "forge_golden_chapters",
    "ask_architect",
    "design_character",
    "design_paywall",
    "audit_hooks",
}

class GenreProfile(BaseModel):
    genre_id: str
    name: str
    weights: dict[str, float] = Field(default_factory=dict)
    rhythm_params: dict[str, int] = Field(default_factory=dict)
    taboos: list[str] = Field(default_factory=list)

class GenreRouter:
    def __init__(self):
        self._current_genre: str | None = None
    
    @property
    def current_genre(self) -> str | None:
        return self._current_genre
    
    def set_genre(self, genre_id: str) -> None:
        self._current_genre = genre_id
    
    def require_genre(self) -> str:
        """获取当前品类，未设置时抛出异常"""
        if self._current_genre is None:
            raise ValueError(
                "genre_profile is required. "
                "Please set genre before invoking creation skills."
            )
        return self._current_genre
    
    def is_genre_required(self, skill_name: str) -> bool:
        """判断某个 Skill 是否需要品类画像"""
        return skill_name in CREATION_SKILLS
    
    def check_prerequisite(self, skill_name: str) -> bool:
        """检查 Skill 的前置条件是否满足"""
        if not self.is_genre_required(skill_name):
            return True
        return self._current_genre is not None
