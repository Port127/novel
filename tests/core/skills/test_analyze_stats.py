import pytest
from novel.core.skills.analyze_stats import AnalyzeStatsSkill, ChapterStats, OverallStats


class TestAnalyzeStatsSkill:
    @pytest.fixture
    def skill(self):
        return AnalyzeStatsSkill()

    def test_chapter_stats_creation(self):
        """测试章节统计数据创建"""
        stats = ChapterStats(
            chapter_id=1,
            read_count=1000,
            completion_rate=0.85,
            comment_count=50,
            like_count=200,
            retention_rate=0.75
        )
        assert stats.chapter_id == 1
        assert stats.read_count == 1000
        assert stats.completion_rate == 0.85
        assert stats.retention_rate == 0.75

    def test_overall_stats_creation(self):
        """测试总体统计数据创建"""
        chapter_stats = [
            ChapterStats(chapter_id=1, read_count=1000, completion_rate=0.8, comment_count=10, like_count=50, retention_rate=0.7),
            ChapterStats(chapter_id=2, read_count=900, completion_rate=0.75, comment_count=8, like_count=40, retention_rate=0.65),
        ]
        overall = OverallStats(
            total_chapters=2,
            avg_completion_rate=0.775,
            avg_retention_rate=0.675,
            total_comments=18,
            total_likes=90,
            chapter_stats=chapter_stats
        )
        assert overall.total_chapters == 2
        assert overall.avg_completion_rate == 0.775
        assert overall.total_comments == 18

    def test_parse_stats_csv(self, skill):
        """测试解析 CSV 数据"""
        csv_data = """chapter_id,read_count,completion_rate,comment_count,like_count
1,1000,0.85,50,200
2,900,0.75,30,150
3,800,0.90,40,180"""
        
        stats_list = skill.parse_stats_csv(csv_data)
        assert len(stats_list) == 3
        assert stats_list[0].chapter_id == 1
        assert stats_list[0].read_count == 1000
        assert stats_list[1].completion_rate == 0.75
        assert stats_list[2].comment_count == 40

    def test_parse_stats_csv_empty(self, skill):
        """测试解析空 CSV 数据"""
        csv_data = "chapter_id,read_count,completion_rate,comment_count,like_count"
        stats_list = skill.parse_stats_csv(csv_data)
        assert len(stats_list) == 0

    def test_calculate_overall_stats(self, skill):
        """测试计算总体统计"""
        chapter_stats = [
            ChapterStats(chapter_id=1, read_count=1000, completion_rate=0.8, comment_count=10, like_count=50, retention_rate=0.7),
            ChapterStats(chapter_id=2, read_count=900, completion_rate=0.7, comment_count=20, like_count=60, retention_rate=0.6),
            ChapterStats(chapter_id=3, read_count=800, completion_rate=0.9, comment_count=30, like_count=70, retention_rate=0.8),
        ]
        
        overall = skill.calculate_overall_stats(chapter_stats)
        assert overall.total_chapters == 3
        assert abs(overall.avg_completion_rate - 0.8) < 0.01  # (0.8+0.7+0.9)/3 = 0.8
        assert abs(overall.avg_retention_rate - 0.7) < 0.01    # (0.7+0.6+0.8)/3 = 0.7
        assert overall.total_comments == 60
        assert overall.total_likes == 180

    def test_detect_retention_drop(self, skill):
        """测试检测追读率下降"""
        chapter_stats = [
            ChapterStats(chapter_id=1, read_count=1000, completion_rate=0.8, comment_count=10, like_count=50, retention_rate=0.7),
            ChapterStats(chapter_id=2, read_count=950, completion_rate=0.75, comment_count=8, like_count=45, retention_rate=0.65),
            ChapterStats(chapter_id=3, read_count=600, completion_rate=0.7, comment_count=5, like_count=30, retention_rate=0.5),  # 大幅下降
            ChapterStats(chapter_id=4, read_count=500, completion_rate=0.65, comment_count=3, like_count=20, retention_rate=0.45),  # 继续下降
        ]
        
        issues = skill.detect_retention_drop(chapter_stats)
        assert len(issues) > 0
        assert any("第3章" in issue or "第4章" in issue for issue in issues)

    def test_detect_retention_drop_no_issue(self, skill):
        """测试正常追读率无问题"""
        chapter_stats = [
            ChapterStats(chapter_id=1, read_count=1000, completion_rate=0.8, comment_count=10, like_count=50, retention_rate=0.7),
            ChapterStats(chapter_id=2, read_count=950, completion_rate=0.78, comment_count=9, like_count=48, retention_rate=0.68),
            ChapterStats(chapter_id=3, read_count=900, completion_rate=0.76, comment_count=8, like_count=45, retention_rate=0.66),
        ]
        
        issues = skill.detect_retention_drop(chapter_stats)
        assert len(issues) == 0

    def test_detect_low_engagement(self, skill):
        """测试检测低互动章节"""
        chapter_stats = [
            ChapterStats(chapter_id=1, read_count=1000, completion_rate=0.8, comment_count=50, like_count=200, retention_rate=0.7),
            ChapterStats(chapter_id=2, read_count=900, completion_rate=0.75, comment_count=5, like_count=20, retention_rate=0.65),  # 低互动
            ChapterStats(chapter_id=3, read_count=800, completion_rate=0.85, comment_count=40, like_count=150, retention_rate=0.75),
        ]
        
        issues = skill.detect_low_engagement(chapter_stats)
        assert len(issues) > 0
        assert any("第2章" in issue for issue in issues)

    def test_detect_low_engagement_no_issue(self, skill):
        """测试正常互动无问题"""
        chapter_stats = [
            ChapterStats(chapter_id=1, read_count=1000, completion_rate=0.8, comment_count=50, like_count=200, retention_rate=0.7),
            ChapterStats(chapter_id=2, read_count=900, completion_rate=0.75, comment_count=45, like_count=180, retention_rate=0.65),
            ChapterStats(chapter_id=3, read_count=800, completion_rate=0.85, comment_count=40, like_count=150, retention_rate=0.75),
        ]
        
        issues = skill.detect_low_engagement(chapter_stats)
        assert len(issues) == 0

    def test_evaluate_good_stats(self, skill):
        """测试评估良好数据"""
        chapter_stats = [
            ChapterStats(chapter_id=1, read_count=1000, completion_rate=0.85, comment_count=50, like_count=200, retention_rate=0.75),
            ChapterStats(chapter_id=2, read_count=950, completion_rate=0.80, comment_count=45, like_count=180, retention_rate=0.70),
            ChapterStats(chapter_id=3, read_count=900, completion_rate=0.82, comment_count=40, like_count=160, retention_rate=0.68),
        ]
        
        verdict = skill.evaluate(chapter_stats)
        assert verdict.passed is True
        assert verdict.layer_scores["overall"] >= 80
        assert len(verdict.diagnostics) > 0

    def test_evaluate_poor_stats(self, skill):
        """测试评估差数据"""
        chapter_stats = [
            ChapterStats(chapter_id=1, read_count=1000, completion_rate=0.8, comment_count=10, like_count=50, retention_rate=0.7),
            ChapterStats(chapter_id=2, read_count=600, completion_rate=0.5, comment_count=2, like_count=10, retention_rate=0.4),
            ChapterStats(chapter_id=3, read_count=400, completion_rate=0.4, comment_count=1, like_count=5, retention_rate=0.3),
        ]
        
        verdict = skill.evaluate(chapter_stats)
        assert verdict.passed is False
        assert verdict.layer_scores["overall"] < 60
        assert len(verdict.diagnostics) > 0

    def test_fix_generate_suggestions(self, skill):
        """测试修复生成建议"""
        chapter_stats = [
            ChapterStats(chapter_id=1, read_count=1000, completion_rate=0.8, comment_count=50, like_count=200, retention_rate=0.7),
            ChapterStats(chapter_id=2, read_count=600, completion_rate=0.5, comment_count=2, like_count=10, retention_rate=0.4),
        ]
        
        verdict = skill.evaluate(chapter_stats)
        result = skill.fix(chapter_stats, verdict)
        assert result.text is not None
        assert len(result.metadata.get("changes", [])) > 0
        assert "追读率" in result.metadata.get("reason", "") or "问题" in result.metadata.get("reason", "")
