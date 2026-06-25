"""
Tests for FleshOutChapterSkill - 节拍扩写员
"""
import pytest
from novel.core.skills.flesh_out_chapter import FleshOutChapterSkill


class TestFleshOutChapterSkill:
    @pytest.fixture
    def skill(self):
        return FleshOutChapterSkill()
    
    def test_evaluate_good_outline(self, skill):
        """测试良好大纲的评估"""
        outline = {
            "title": "第1章 觉醒",
            "content": "主角在一个平凡的小村庄长大，从小就与众不同。某天突然觉醒了神秘的力量，从此踏上了不平凡的道路，开启了传奇人生。",
            "beats": [
                {"id": 1, "description": "开场：村庄日常", "target_words": 500},
                {"id": 2, "description": "发展：觉醒时刻", "target_words": 1500},
                {"id": 3, "description": "高潮：初次战斗", "target_words": 1000},
                {"id": 4, "description": "结尾：踏上旅程", "target_words": 500}
            ],
            "target_words": 3500
        }
        
        verdict = skill.evaluate(outline)
        assert verdict.passed is True
        assert verdict.layer_scores["structure"] == 100.0
        assert verdict.layer_scores["detail"] == 100.0
        assert verdict.layer_scores["length"] == 100.0
    
    def test_evaluate_missing_fields(self, skill):
        """测试缺少必要字段的评估"""
        outline = {
            "title": "第1章"
            # 缺少 content 和 beats
        }
        
        verdict = skill.evaluate(outline)
        assert verdict.passed is False
        assert "content" in str(verdict.diagnostics)
        assert "beats" in str(verdict.diagnostics)
        assert verdict.layer_scores["structure"] == 0.0
    
    def test_evaluate_too_few_beats(self, skill):
        """测试节拍数量过少的评估"""
        outline = {
            "title": "第1章",
            "content": "一些内容...",
            "beats": [
                {"id": 1, "description": "开场"}
            ],
            "target_words": 3000
        }
        
        verdict = skill.evaluate(outline)
        assert verdict.passed is False
        assert verdict.layer_scores["structure"] == 30.0
        assert any("节拍数量过少" in d for d in verdict.diagnostics)
    
    def test_evaluate_too_many_beats(self, skill):
        """测试节拍数量过多的评估"""
        outline = {
            "title": "第1章",
            "content": "一些内容...",
            "beats": [{"id": i, "description": f"节拍{i}"} for i in range(20)],
            "target_words": 3000
        }
        
        verdict = skill.evaluate(outline)
        assert verdict.passed is False
        assert verdict.layer_scores["structure"] == 70.0
        assert any("节拍数量过多" in d for d in verdict.diagnostics)
    
    def test_evaluate_short_content(self, skill):
        """测试内容过短的评估"""
        outline = {
            "title": "第1章",
            "content": "短",
            "beats": [
                {"id": 1, "description": "开场"},
                {"id": 2, "description": "发展"},
                {"id": 3, "description": "结尾"}
            ],
            "target_words": 3000
        }
        
        verdict = skill.evaluate(outline)
        assert verdict.passed is False
        assert verdict.layer_scores["detail"] == 40.0
        assert any("大纲内容过短" in d for d in verdict.diagnostics)
    
    def test_evaluate_target_words_too_short(self, skill):
        """测试目标字数过少的评估"""
        outline = {
            "title": "第1章",
            "content": "足够长的内容描述...",
            "beats": [
                {"id": 1, "description": "开场"},
                {"id": 2, "description": "发展"},
                {"id": 3, "description": "结尾"}
            ],
            "target_words": 1000
        }
        
        verdict = skill.evaluate(outline)
        assert verdict.passed is False
        assert verdict.layer_scores["length"] == 50.0
        assert any("目标字数过少" in d for d in verdict.diagnostics)
    
    def test_evaluate_target_words_too_long(self, skill):
        """测试目标字数过多的评估"""
        outline = {
            "title": "第1章",
            "content": "足够长的内容描述...",
            "beats": [
                {"id": 1, "description": "开场"},
                {"id": 2, "description": "发展"},
                {"id": 3, "description": "结尾"}
            ],
            "target_words": 8000
        }
        
        verdict = skill.evaluate(outline)
        assert verdict.passed is False
        assert verdict.layer_scores["length"] == 70.0
        assert any("目标字数过多" in d for d in verdict.diagnostics)
    
    def test_fix_missing_title(self, skill):
        """测试修复缺少标题"""
        outline = {
            "content": "内容...",
            "beats": [{"id": 1, "description": "节拍"}],
            "target_words": 3000
        }
        
        verdict = skill.evaluate(outline)
        result = skill.fix(outline, verdict)
        
        import json
        fixed_outline = json.loads(result.text)
        assert fixed_outline["title"] == "第X章 未命名章节"
        assert "添加了默认标题" in result.metadata["changes"]
    
    def test_fix_too_few_beats(self, skill):
        """测试修复节拍数量过少"""
        outline = {
            "title": "第1章",
            "content": "内容描述内容描述内容描述内容描述内容描述内容描述内容描述内容描述内容描述",
            "beats": [{"id": 1, "description": "节拍1"}],
            "target_words": 3000
        }
        
        verdict = skill.evaluate(outline)
        result = skill.fix(outline, verdict)
        
        import json
        fixed_outline = json.loads(result.text)
        assert len(fixed_outline["beats"]) >= 3
        assert any("补充节拍" in c for c in result.metadata["changes"])
    
    def test_fix_missing_target_words(self, skill):
        """测试修复缺少目标字数"""
        outline = {
            "title": "第1章",
            "content": "内容描述内容描述内容描述内容描述内容描述内容描述内容描述内容描述内容描述",
            "beats": [
                {"id": 1, "description": "节拍1"},
                {"id": 2, "description": "节拍2"},
                {"id": 3, "description": "节拍3"}
            ]
        }
        
        verdict = skill.evaluate(outline)
        result = skill.fix(outline, verdict)
        
        import json
        fixed_outline = json.loads(result.text)
        assert fixed_outline["target_words"] == 3000
        assert any("设置默认目标字数" in c for c in result.metadata["changes"])
    
    def test_fix_no_changes_needed(self, skill):
        """测试无需修复的情况"""
        outline = {
            "title": "第1章",
            "content": "足够长的内容描述足够长的内容描述足够长的内容描述足够长的内容描述足够长的内容描述足够长的内容描述",
            "beats": [
                {"id": 1, "description": "开场"},
                {"id": 2, "description": "发展"},
                {"id": 3, "description": "结尾"}
            ],
            "target_words": 3000
        }
        
        verdict = skill.evaluate(outline)
        result = skill.fix(outline, verdict)
        
        assert result.metadata["reason"] == "大纲无需修复"
