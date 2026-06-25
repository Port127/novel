from typing import Any
from pydantic import BaseModel, Field
from novel.core.skills.base import CommercialVerdict, SkillResult

class Archetype(BaseModel):
    """角色原型"""
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    traits: list[str] = Field(..., min_length=1)
    goals: list[str] = Field(..., min_length=1)
    flaws: list[str] = Field(..., min_length=1)

class TropeTemplate(BaseModel):
    """套路模板"""
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    steps: list[str] = Field(..., min_length=1)
    emotional_curve: list[int] = Field(..., min_length=1)

class AskArchitectSkill:
    """剧情与节奏架构师 - 分析大纲结构和节奏问题"""
    
    name = "ask_architect"
    version = "0.1.0"
    
    # 内置原型库
    ARCHETYPES = {
        "hero": Archetype(
            id="hero",
            name="英雄",
            traits=["勇敢", "正义", "执着"],
            goals=["拯救世界", "保护亲友"],
            flaws=["傲慢", "冲动"]
        ),
        "mentor": Archetype(
            id="mentor",
            name="导师",
            traits=["智慧", "神秘", "强大"],
            goals=["引导主角", "传承知识"],
            flaws=["过于保守", "隐藏真相"]
        ),
        "villain": Archetype(
            id="villain",
            name="反派",
            traits=["强大", "狡猾", "残忍"],
            goals=["统治世界", "复仇"],
            flaws=["自负", "孤独"]
        )
    }
    
    # 内置套路模板库
    TROPES = {
        "face_slap": TropeTemplate(
            id="face_slap",
            name="打脸",
            description="主角被轻视后反击",
            steps=["被嘲笑", "积蓄力量", "一击制胜"],
            emotional_curve=[30, 50, 90]
        ),
        "upgrade": TropeTemplate(
            id="upgrade",
            name="升级",
            description="主角突破境界",
            steps=["遇到瓶颈", "获得机遇", "突破成功"],
            emotional_curve=[40, 60, 95]
        ),
        "romance": TropeTemplate(
            id="romance",
            name="情感",
            description="感情线发展",
            steps=["初遇", "误会", "相恋"],
            emotional_curve=[50, 30, 85]
        )
    }
    
    def evaluate(self, outline: dict[str, Any]) -> CommercialVerdict:
        """评估大纲质量"""
        analysis = self.analyze_outline(outline)
        
        passed = len(analysis["pacing"]["issues"]) == 0
        diagnostics = analysis["pacing"]["issues"]
        
        # 即使通过，也添加分析信息
        if passed:
            diagnostics.append(f"大纲结构良好，共 {analysis['structure']['total_chapters']} 章")
        
        return CommercialVerdict(
            passed=passed,
            diagnostics=diagnostics,
            score=100 if passed else 60,
            metadata=analysis
        )
    
    def fix(self, outline: dict[str, Any], verdict: CommercialVerdict) -> SkillResult:
        """修复大纲问题"""
        # 生成建议
        advice = self._generate_structure_advice(verdict.diagnostics)
        
        return SkillResult(
            fixed_content=outline,
            changes=advice,
            reason="根据架构分析生成修复建议"
        )
    
    def analyze_outline(self, outline: dict[str, Any]) -> dict[str, Any]:
        """分析大纲结构"""
        chapters = outline.get("chapters", [])
        
        if not chapters:
            return {
                "structure": {"issues": ["大纲缺少章节"]},
                "pacing": {"issues": ["大纲为空"]},
                "conflict": {"issues": ["无冲突信息"]}
            }
        
        rhythm_issues = self._detect_rhythm_issues(chapters)
        
        return {
            "structure": {
                "total_chapters": len(chapters),
                "issues": [] if len(chapters) >= 3 else ["章节数量过少"]
            },
            "pacing": {
                "issues": rhythm_issues
            },
            "conflict": {
                "issues": [] if any("危机" in ch.get("title", "") for ch in chapters) else ["缺少冲突高潮"]
            }
        }
    
    def _detect_rhythm_issues(self, chapters: list[dict]) -> list[str]:
        """检测节奏问题"""
        issues = []
        
        # 检查连续慢节奏
        slow_count = 0
        for i, chapter in enumerate(chapters):
            pacing = chapter.get("pacing", "medium")
            if pacing == "slow":
                slow_count += 1
                if slow_count >= 3:
                    issues.append(f"第{i-slow_count+2}-{i+1}章连续慢节奏，需要加快")
                    break
            else:
                slow_count = 0
        
        return issues
    
    def _generate_structure_advice(self, issues: list[str]) -> list[str]:
        """生成结构建议"""
        advice = []
        
        for issue in issues:
            if "节奏" in issue or "连续慢节奏" in issue:
                advice.append("建议在高潮章节前增加铺垫，在低谷章节后增加转折，调整节奏分布")
            elif "冲突" in issue:
                advice.append("建议增加主要冲突点，提升故事张力")
        
        return advice
    
    def get_trope(self, trope_id: str) -> TropeTemplate | None:
        """获取套路模板"""
        return self.TROPES.get(trope_id)
    
    def get_archetype(self, archetype_id: str) -> Archetype | None:
        """获取角色原型"""
        return self.ARCHETYPES.get(archetype_id)
