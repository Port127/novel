from pydantic import BaseModel, Field
from novel.core.skills.base import BaseCommercialSkill, CommercialVerdict, SkillResult, TokenUsage

class MicroBeat(BaseModel):
    beat_id: str
    description: str
    target_words: int = Field(ge=50)
    emotion_target: str

class GenreTemplate(BaseModel):
    genre_id: str
    micro_beats: list[MicroBeat]

class GoldenChapterAnalysis(BaseModel):
    chapter_number: int
    first_conflict_at_word: int
    has_character_setup: bool
    has_golden_finger: bool
    has_first_climax: bool
    beats: list[MicroBeat] = Field(default_factory=list)
    overall_score: float = Field(ge=0, le=100)
    passed: bool
    diagnostics: list[str] = Field(default_factory=list)

# 品类模板
TEMPLATES = {
    "genre/xuanhuan": GenreTemplate(
        genre_id="genre/xuanhuan",
        micro_beats=[
            MicroBeat(
                beat_id="humiliation",
                description="主角受辱，引发读者同情",
                target_words=300,
                emotion_target="压抑",
            ),
            MicroBeat(
                beat_id="golden_finger_awakening",
                description="金手指觉醒，给予希望",
                target_words=400,
                emotion_target="期待",
            ),
            MicroBeat(
                beat_id="first_counterattack",
                description="首次反击，展示力量",
                target_words=500,
                emotion_target="爽快",
            ),
        ],
    ),
    "genre/urban": GenreTemplate(
        genre_id="genre/urban",
        micro_beats=[
            MicroBeat(
                beat_id="betrayal",
                description="被退婚/背叛，制造冲突",
                target_words=300,
                emotion_target="愤怒",
            ),
            MicroBeat(
                beat_id="identity_reveal",
                description="隐藏身份曝光",
                target_words=400,
                emotion_target="震惊",
            ),
            MicroBeat(
                beat_id="face_slap",
                description="第一波打脸",
                target_words=500,
                emotion_target="爽快",
            ),
        ],
    ),
    "genre/system": GenreTemplate(
        genre_id="genre/system",
        micro_beats=[
            MicroBeat(
                beat_id="system_activation",
                description="系统激活，获得金手指",
                target_words=300,
                emotion_target="惊喜",
            ),
            MicroBeat(
                beat_id="first_mission",
                description="首个任务发布",
                target_words=400,
                emotion_target="紧张",
            ),
            MicroBeat(
                beat_id="reward_crush",
                description="完成任务，奖励碾压",
                target_words=500,
                emotion_target="爽快",
            ),
        ],
    ),
}

class ForgeGoldenChaptersSkill(BaseCommercialSkill):
    name = "forge_golden_chapters"
    
    async def evaluate(self, text: str, context: dict | None = None) -> CommercialVerdict:
        """评估黄金三章结构"""
        genre_id = context.get("genre_id", "genre/xuanhuan") if context else "genre/xuanhuan"
        chapter_number = context.get("chapter_number", 1) if context else 1
        
        analysis = await self.validate_chapter(text, chapter_number, genre_id)
        
        return CommercialVerdict(
            passed=analysis.passed,
            diagnostics=analysis.diagnostics,
            layer_scores={"overall": analysis.overall_score},
            severity="critical" if not analysis.passed else "info",
        )
    
    async def fix(self, text: str, verdict: CommercialVerdict) -> SkillResult:
        """根据诊断结果提供修复建议"""
        return SkillResult(text=text, token_usage=TokenUsage())
    
    async def validate_chapter(
        self, text: str, chapter_number: int, genre_id: str
    ) -> GoldenChapterAnalysis:
        """验证章节结构是否符合黄金三章标准"""
        diagnostics = []
        
        # 检查首冲突位置（应在 300 字内）
        first_conflict = self._find_first_conflict(text)
        if first_conflict > 300:
            diagnostics.append(f"首冲突过晚：在第 {first_conflict} 字才出现，应在 300 字内")
        
        # 检查人设是否建立
        has_character_setup = self._has_character_setup(text)
        if not has_character_setup:
            diagnostics.append("人设未建立：缺少主角基本信息")
        
        # 检查金手指是否亮相
        has_golden_finger = self._has_golden_finger(text)
        if not has_golden_finger:
            diagnostics.append("金手指未亮相：缺少系统/能力觉醒")
        
        # 检查第一个小高潮
        has_first_climax = self._has_first_climax(text)
        if not has_first_climax:
            diagnostics.append("缺少第一个小高潮：没有反击/爽点")
        
        # 计算综合分数
        score = 0
        if first_conflict <= 300:
            score += 25
        if has_character_setup:
            score += 25
        if has_golden_finger:
            score += 25
        if has_first_climax:
            score += 25
        
        passed = score >= 75 and first_conflict <= 300
        
        # 获取品类模板
        template = self.get_genre_template(genre_id)
        beats = template.micro_beats if template else []
        
        return GoldenChapterAnalysis(
            chapter_number=chapter_number,
            first_conflict_at_word=first_conflict,
            has_character_setup=has_character_setup,
            has_golden_finger=has_golden_finger,
            has_first_climax=has_first_climax,
            beats=beats,
            overall_score=score,
            passed=passed,
            diagnostics=diagnostics,
        )
    
    def get_genre_template(self, genre_id: str) -> GenreTemplate | None:
        """获取品类对应的开篇模板"""
        return TEMPLATES.get(genre_id)
    
    def _find_first_conflict(self, text: str) -> int:
        """查找首个冲突出现的位置"""
        conflict_keywords = ["废物", "嘲笑", "羞辱", "打飞", "踢飞", "拍飞", "骂道", "退婚", "背叛", "系统激活", "系统"]
        for kw in conflict_keywords:
            pos = text.find(kw)
            if pos >= 0:
                return pos
        # 如果没有找到冲突，返回一个很大的值，表示冲突"永不"出现
        return 99999
    
    def _has_character_setup(self, text: str) -> bool:
        """检查是否建立了人设"""
        setup_keywords = ["陈凡", "林", "萧", "叶", "主角", "少年", "少年", "青年"]
        return any(kw in text for kw in setup_keywords)
    
    def _has_golden_finger(self, text: str) -> bool:
        """检查金手指是否亮相"""
        golden_finger_keywords = ["系统", "觉醒", "金手指", "传承", "神器", "突破", "力量"]
        return any(kw in text for kw in golden_finger_keywords)
    
    def _has_first_climax(self, text: str) -> bool:
        """检查是否有第一个小高潮"""
        climax_keywords = ["震惊", "震惊", "惊呼", "不可能", "竟然", "突破", "反击", "一拳"]
        return any(kw in text for kw in climax_keywords)
