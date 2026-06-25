import pytest
from novel.core.skills.ask_architect import AskArchitectSkill, Archetype, TropeTemplate
from pydantic import ValidationError

class TestAskArchitectSkill:
    @pytest.fixture
    def skill(self):
        return AskArchitectSkill()

    def test_archetype_creation(self):
        """测试原型创建"""
        archetype = Archetype(
            id="hero",
            name="英雄",
            traits=["勇敢", "正义"],
            goals=["拯救世界"],
            flaws=["傲慢"]
        )
        assert archetype.id == "hero"
        assert archetype.name == "英雄"
        assert len(archetype.traits) == 2

    def test_archetype_validation(self):
        """测试原型验证失败"""
        with pytest.raises(ValidationError):
            Archetype(id="", name="", traits=[], goals=[], flaws=[])

    def test_trope_template_creation(self):
        """测试套路模板创建"""
        template = TropeTemplate(
            id="face_slap",
            name="打脸",
            description="主角被轻视后反击",
            steps=["被嘲笑", "积蓄力量", "一击制胜"],
            emotional_curve=[30, 50, 90]
        )
        assert template.id == "face_slap"
        assert len(template.steps) == 3
        assert len(template.emotional_curve) == 3

    def test_trope_template_validation(self):
        """测试套路模板验证失败"""
        with pytest.raises(ValidationError):
            TropeTemplate(
                id="",
                name="",
                description="",
                steps=[],
                emotional_curve=[]
            )

    def test_analyze_outline_basic(self, skill):
        """测试基本大纲分析"""
        outline = {
            "chapters": [
                {"id": 1, "title": "觉醒", "summary": "主角获得金手指"},
                {"id": 2, "title": "初试", "summary": "主角使用能力"},
                {"id": 3, "title": "危机", "summary": "遇到强敌"},
                {"id": 4, "title": "突破", "summary": "主角突破自我"},
                {"id": 5, "title": "胜利", "summary": "战胜敌人"}
            ]
        }
        
        analysis = skill.analyze_outline(outline)
        assert analysis is not None
        assert "structure" in analysis
        assert "pacing" in analysis
        assert "conflict" in analysis

    def test_analyze_outline_missing_chapters(self, skill):
        """测试大纲缺少章节"""
        outline = {"chapters": []}
        
        analysis = skill.analyze_outline(outline)
        assert analysis is not None
        assert analysis["structure"]["issues"] is not None

    def test_detect_rhythm_issues_continuous_slow(self, skill):
        """测试检测连续慢节奏"""
        chapters = [
            {"id": i, "title": f"第{i}章", "summary": "日常描写", "pacing": "slow"}
            for i in range(1, 8)
        ]
        
        issues = skill._detect_rhythm_issues(chapters)
        assert len(issues) > 0
        assert any("连续" in issue and "慢节奏" in issue for issue in issues)

    def test_detect_rhythm_issues_normal(self, skill):
        """测试正常节奏分布"""
        chapters = [
            {"id": 1, "pacing": "slow"},
            {"id": 2, "pacing": "medium"},
            {"id": 3, "pacing": "fast"},
            {"id": 4, "pacing": "slow"},
            {"id": 5, "pacing": "medium"},
        ]
        
        issues = skill._detect_rhythm_issues(chapters)
        assert len(issues) == 0

    def test_generate_structure_advice(self, skill):
        """测试生成结构建议"""
        issues = ["第1-3章节奏过慢"]
        advice = skill._generate_structure_advice(issues)
        
        assert len(advice) > 0
        assert any("节奏" in a for a in advice)

    def test_get_trope_by_id(self, skill):
        """测试获取套路模板"""
        template = skill.get_trope("face_slap")
        assert template is not None
        assert template.id == "face_slap"
        assert template.name == "打脸"

    def test_get_trope_not_found(self, skill):
        """测试获取不存在的套路"""
        template = skill.get_trope("nonexistent")
        assert template is None

    def test_get_archetype_by_id(self, skill):
        """测试获取原型"""
        archetype = skill.get_archetype("hero")
        assert archetype is not None
        assert archetype.id == "hero"

    def test_get_archetype_not_found(self, skill):
        """测试获取不存在的原型"""
        archetype = skill.get_archetype("nonexistent")
        assert archetype is None

    def test_evaluate_good_outline(self, skill):
        """测试评估优秀大纲"""
        outline = {
            "chapters": [
                {"id": 1, "title": "觉醒", "summary": "主角获得金手指", "pacing": "fast"},
                {"id": 2, "title": "冲突", "summary": "遇到敌人", "pacing": "fast"},
                {"id": 3, "title": "反击", "summary": "主角反击", "pacing": "fast"},
            ]
        }
        
        verdict = skill.evaluate(outline)
        assert verdict.passed is True
        assert len(verdict.diagnostics) > 0

    def test_evaluate_poor_outline(self, skill):
        """测试评估问题大纲"""
        outline = {
            "chapters": [
                {"id": i, "title": f"第{i}章", "summary": "日常", "pacing": "slow"}
                for i in range(1, 8)
            ]
        }
        
        verdict = skill.evaluate(outline)
        assert verdict.passed is False
        assert len(verdict.diagnostics) > 0
