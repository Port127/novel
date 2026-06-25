from typing import Any
from pydantic import BaseModel, Field
from novel.core.skills.base import BaseCommercialSkill, CommercialVerdict, SkillResult, TokenUsage

class GenreWeights(BaseModel):
    """品类爽感维度权重"""
    genre: str
    face_slap_weight: float = Field(ge=0, le=1, description="打脸权重")
    upgrade_weight: float = Field(ge=0, le=1, description="升级权重")
    romance_weight: float = Field(ge=0, le=1, description="CP/感情线权重")
    suspense_weight: float = Field(ge=0, le=1, description="悬念权重")

class CharacterDesign(BaseModel):
    """人设设计结果"""
    name: str
    archetype: str
    face_slap_index: int = Field(ge=1, le=10, description="打脸指数 1-10")
    cp_score: int = Field(ge=1, le=10, description="CP 感/嗑点 1-10")
    villain_disgust_level: int = Field(ge=1, le=10, description="反派恶心度 1-10")
    golden_finger: str
    golden_finger_limit: str
    genre_weights: GenreWeights
    overall_score: float = Field(ge=0, le=100)
    passed: bool
    
    # 可选字段
    villain_name: str | None = None
    villain_background: str | None = None

class DesignCharacterSkill(BaseCommercialSkill):
    """爽感人设主编 - 根据品类设计符合爽感需求的人设"""
    
    name = "design_character"
    
    # 品类权重配置
    GENRE_WEIGHTS = {
        "genre/xuanhuan": GenreWeights(
            genre="genre/xuanhuan",
            face_slap_weight=0.8,
            upgrade_weight=0.9,
            romance_weight=0.3,
            suspense_weight=0.5,
        ),
        "genre/urban": GenreWeights(
            genre="genre/urban",
            face_slap_weight=0.9,
            upgrade_weight=0.3,
            romance_weight=0.6,
            suspense_weight=0.4,
        ),
        "genre/system": GenreWeights(
            genre="genre/system",
            face_slap_weight=0.7,
            upgrade_weight=0.8,
            romance_weight=0.4,
            suspense_weight=0.6,
        ),
    }
    
    async def evaluate(self, text: str, context: dict | None = None) -> CommercialVerdict:
        """评估人设文本（此技能主要用于设计，evaluate 返回通过）"""
        # 如果 context 包含人设参数，使用 design_character 进行评估
        if context and "name" in context:
            design = await self.design_character(
                name=context["name"],
                genre_id=context.get("genre_id", "genre/urban"),
                background=context.get("background", ""),
                personality=context.get("personality", ""),
                golden_finger=context.get("golden_finger", ""),
                villain_name=context.get("villain_name"),
                villain_background=context.get("villain_background"),
            )
            return CommercialVerdict(
                passed=design.passed,
                diagnostics=[] if design.passed else [f"人设评分不足：{design.overall_score}"],
                layer_scores={"overall": design.overall_score},
                severity="info" if design.passed else "warning"
            )
        
        return CommercialVerdict(
            passed=True,
            diagnostics=["人设主编主要用于设计，文本评估始终通过"],
            layer_scores={"relevance": 100.0},
            severity="info"
        )
    
    async def fix(self, text: str, verdict: CommercialVerdict) -> SkillResult:
        """修复文本（此技能不修改文本）"""
        return SkillResult(text=text, token_usage=TokenUsage())
    
    async def design_character(
        self,
        name: str,
        genre_id: str,
        background: str,
        personality: str,
        golden_finger: str,
        villain_name: str | None = None,
        villain_background: str | None = None,
    ) -> CharacterDesign:
        """设计角色人设"""
        # 获取品类权重
        genre_weights = self.GENRE_WEIGHTS.get(genre_id, self.GENRE_WEIGHTS["genre/urban"])
        
        # 确定角色原型
        archetype = self._determine_archetype(background, personality, golden_finger)
        
        # 计算打脸指数
        face_slap_index = self._calculate_face_slap_index(background, personality, golden_finger)
        
        # 计算 CP 感
        cp_score = self._calculate_cp_score(personality, background)
        
        # 计算反派恶心度
        villain_disgust_level = self._calculate_villain_disgust(villain_background) if villain_background else 5
        
        # 计算金手指限制
        golden_finger_limit = self._determine_golden_finger_limit(golden_finger)
        
        # 计算综合评分
        overall_score = self._calculate_overall_score(
            genre_weights,
            face_slap_index,
            cp_score,
            villain_disgust_level,
        )
        
        # 判断是否通过（综合评分 >= 70 且打脸指数 >= 5）
        passed = overall_score >= 70 and face_slap_index >= 5
        
        return CharacterDesign(
            name=name,
            archetype=archetype,
            face_slap_index=face_slap_index,
            cp_score=cp_score,
            villain_disgust_level=villain_disgust_level,
            golden_finger=golden_finger,
            golden_finger_limit=golden_finger_limit,
            genre_weights=genre_weights,
            overall_score=overall_score,
            passed=passed,
            villain_name=villain_name,
            villain_background=villain_background,
        )
    
    def _determine_archetype(self, background: str, personality: str, golden_finger: str) -> str:
        """确定角色原型"""
        if "废柴" in background or "废物" in background:
            if "隐忍" in personality:
                return "扮猪吃虎"
            else:
                return "废柴逆袭"
        elif "退婚" in background or "背叛" in background:
            return "复仇归来"
        elif "隐藏" in golden_finger or "身份" in golden_finger:
            return "隐藏大佬"
        else:
            return "普通主角"
    
    def _calculate_face_slap_index(self, background: str, personality: str, golden_finger: str) -> int:
        """计算打脸指数（1-10）"""
        score = 5  # 基础分
        
        # 背景加分
        if "废柴" in background or "废物" in background:
            score += 2
        if "退婚" in background or "背叛" in background:
            score += 2
        if "羞辱" in background or "嘲笑" in background:
            score += 1
        
        # 性格加分
        if "腹黑" in personality or "狠辣" in personality:
            score += 1
        if "城府深" in personality:
            score += 1
        
        # 金手指加分
        if "系统" in golden_finger:
            score += 1
        if "隐藏身份" in golden_finger or "继承人" in golden_finger:
            score += 2
        
        return min(10, max(1, score))
    
    def _calculate_cp_score(self, personality: str, background: str) -> int:
        """计算 CP 感/嗑点（1-10）"""
        score = 5  # 基础分
        
        # 性格加分
        if "腹黑" in personality or "霸道" in personality:
            score += 2
        if "温柔" in personality or "深情" in personality:
            score += 1
        if "痞帅" in personality:
            score += 2
        
        # 背景加分
        if "隐藏身份" in background:
            score += 1
        
        return min(10, max(1, score))
    
    def _calculate_villain_disgust(self, villain_background: str) -> int:
        """计算反派恶心度（1-10）"""
        score = 5  # 基础分
        
        if "羞辱" in villain_background or "嘲笑" in villain_background:
            score += 2
        if "背叛" in villain_background or "陷害" in villain_background:
            score += 2
        if "抢走" in villain_background or "夺走" in villain_background:
            score += 2
        if "多次" in villain_background:
            score += 1
        
        return min(10, max(1, score))
    
    def _determine_golden_finger_limit(self, golden_finger: str) -> str:
        """确定金手指限制"""
        if "系统" in golden_finger:
            return "每日任务次数有限"
        elif "吞噬" in golden_finger:
            return "需要消耗资源"
        elif "空间" in golden_finger:
            return "空间大小有限"
        else:
            return "使用有代价"
    
    def _calculate_overall_score(
        self,
        genre_weights: GenreWeights,
        face_slap_index: int,
        cp_score: int,
        villain_disgust_level: int,
    ) -> float:
        """计算综合评分（0-100）"""
        # 基础分
        score = 50.0
        
        # 打脸指数贡献（权重最高）
        score += face_slap_index * genre_weights.face_slap_weight * 5
        
        # CP 感贡献
        score += cp_score * genre_weights.romance_weight * 3
        
        # 反派恶心度贡献
        score += villain_disgust_level * 2
        
        return min(100.0, max(0.0, score))
