import pytest
from novel.core.skills.check_logic import CheckLogicSkill


class TestCheckLogicSkill:
    @pytest.fixture
    def skill(self):
        return CheckLogicSkill()
    
    def test_evaluate_good_chapter(self, skill):
        """测试良好章节的逻辑检查"""
        chapter = {
            "title": "第1章",
            "content": "主角早上起床，准备去学校。他走在路上，遇到了张三。两人一起走到学校，开始了新的一天。"
        }
        
        verdict = skill.evaluate(chapter)
        assert verdict.passed is True
        assert verdict.layer_scores["content"] == 100.0
        assert verdict.layer_scores["characters"] == 100.0
    
    def test_evaluate_empty_content(self, skill):
        """测试空内容的逻辑检查"""
        chapter = {
            "title": "第1章",
            "content": ""
        }
        
        verdict = skill.evaluate(chapter)
        assert verdict.passed is False
        assert any("章节内容为空" in d for d in verdict.diagnostics)
        assert verdict.severity == "critical"
    
    def test_evaluate_no_character_mentions(self, skill):
        """测试没有角色提及的章节"""
        chapter = {
            "title": "第1章",
            "content": "今天天气很好，阳光明媚。"
        }
        
        verdict = skill.evaluate(chapter)
        assert verdict.layer_scores["characters"] == 50.0
        assert any("角色提及" in d for d in verdict.diagnostics)
    
    def test_fix_empty_content(self, skill):
        """测试修复空内容"""
        chapter = {
            "title": "第1章",
            "content": ""
        }
        
        verdict = skill.evaluate(chapter)
        result = skill.fix(chapter, verdict)
        
        assert result.text == ""
        assert "无需修复" in result.metadata["reason"]
    
    def test_fix_no_character_mentions(self, skill):
        """测试修复没有角色提及的情况"""
        chapter = {
            "title": "第1章",
            "content": "今天天气很好，阳光明媚。"
        }
        
        verdict = skill.evaluate(chapter)
        result = skill.fix(chapter, verdict)
        
        assert "建议在章节开头明确提及主要角色" in result.metadata["changes"]
    
    def test_extract_character_mentions(self, skill):
        """测试角色提及提取"""
        content = "主角走在路上，遇到了张三。他向张三打招呼。"
        mentions = skill._extract_character_mentions(content)
        
        assert "主角" in mentions
        assert "他" in mentions
        assert "张" in mentions
    
    def test_extract_time_markers(self, skill):
        """测试时间标记提取"""
        content = "早上起床，中午吃饭，晚上睡觉。第二天继续。"
        markers = skill._extract_time_markers(content)
        
        assert "早上" in markers
        assert "中午" in markers
        assert "晚上" in markers
        assert "第二天" in markers
    
    def test_extract_locations(self, skill):
        """测试地点提取"""
        content = "主角从家出发，去了学校。然后在公司工作。"
        locations = skill._extract_locations(content)
        
        assert "家" in locations
        assert "学校" in locations
        assert "公司" in locations
