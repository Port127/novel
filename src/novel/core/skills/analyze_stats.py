import csv
import io
from typing import Any
from pydantic import BaseModel, Field
from novel.core.skills.base import BaseCommercialSkill, CommercialVerdict, SkillResult, TokenUsage


class ChapterStats(BaseModel):
    """单章统计数据"""
    chapter_id: int
    read_count: int
    completion_rate: float
    comment_count: int
    like_count: int
    retention_rate: float


class OverallStats(BaseModel):
    """总体统计数据"""
    total_chapters: int
    avg_completion_rate: float
    avg_retention_rate: float
    total_comments: int
    total_likes: int
    chapter_stats: list[ChapterStats]


class AnalyzeStatsSkill(BaseCommercialSkill):
    """数据诊断师 - 分析小说数据，识别问题章节"""
    
    name = "analyze_stats"
    version = "0.1.0"
    
    # 阈值配置
    RETENTION_DROP_THRESHOLD = 0.15  # 追读率下降超过15%视为问题
    LOW_ENGAGEMENT_THRESHOLD = 0.3   # 互动率低于平均值30%视为低互动
    
    def parse_stats_csv(self, csv_data: str) -> list[ChapterStats]:
        """解析 CSV 格式的统计数据"""
        stats_list = []
        reader = csv.DictReader(io.StringIO(csv_data))
        
        for row in reader:
            stats = ChapterStats(
                chapter_id=int(row['chapter_id']),
                read_count=int(row['read_count']),
                completion_rate=float(row['completion_rate']),
                comment_count=int(row['comment_count']),
                like_count=int(row['like_count']),
                retention_rate=float(row.get('retention_rate', 0.0))
            )
            stats_list.append(stats)
        
        return stats_list
    
    def calculate_overall_stats(self, chapter_stats: list[ChapterStats]) -> OverallStats:
        """计算总体统计"""
        if not chapter_stats:
            return OverallStats(
                total_chapters=0,
                avg_completion_rate=0.0,
                avg_retention_rate=0.0,
                total_comments=0,
                total_likes=0,
                chapter_stats=[]
            )
        
        total_chapters = len(chapter_stats)
        avg_completion_rate = sum(s.completion_rate for s in chapter_stats) / total_chapters
        avg_retention_rate = sum(s.retention_rate for s in chapter_stats) / total_chapters
        total_comments = sum(s.comment_count for s in chapter_stats)
        total_likes = sum(s.like_count for s in chapter_stats)
        
        return OverallStats(
            total_chapters=total_chapters,
            avg_completion_rate=avg_completion_rate,
            avg_retention_rate=avg_retention_rate,
            total_comments=total_comments,
            total_likes=total_likes,
            chapter_stats=chapter_stats
        )
    
    def detect_retention_drop(self, chapter_stats: list[ChapterStats]) -> list[str]:
        """检测追读率下降问题"""
        issues = []
        
        for i in range(1, len(chapter_stats)):
            prev_retention = chapter_stats[i-1].retention_rate
            curr_retention = chapter_stats[i].retention_rate
            
            if prev_retention > 0:
                drop_rate = (prev_retention - curr_retention) / prev_retention
                if drop_rate > self.RETENTION_DROP_THRESHOLD:
                    issues.append(
                        f"第{chapter_stats[i].chapter_id}章追读率下降{drop_rate:.1%}，"
                        f"从{prev_retention:.1%}降至{curr_retention:.1%}"
                    )
        
        return issues
    
    def detect_low_engagement(self, chapter_stats: list[ChapterStats]) -> list[str]:
        """检测低互动章节"""
        issues = []
        
        if not chapter_stats:
            return issues
        
        avg_comments = sum(s.comment_count for s in chapter_stats) / len(chapter_stats)
        avg_likes = sum(s.like_count for s in chapter_stats) / len(chapter_stats)
        
        for stats in chapter_stats:
            engagement_ratio = (stats.comment_count / max(avg_comments, 1) + 
                              stats.like_count / max(avg_likes, 1)) / 2
            
            if engagement_ratio < self.LOW_ENGAGEMENT_THRESHOLD:
                issues.append(
                    f"第{stats.chapter_id}章互动率偏低，"
                    f"评论{stats.comment_count}（平均{avg_comments:.0f}），"
                    f"点赞{stats.like_count}（平均{avg_likes:.0f}）"
                )
        
        return issues
    
    def evaluate(self, chapter_stats: list[ChapterStats]) -> CommercialVerdict:
        """评估数据质量"""
        if not chapter_stats:
            return CommercialVerdict(
                passed=False,
                diagnostics=["无数据可分析"],
                layer_scores={},
                severity="critical"
            )
        
        # 计算总体统计
        overall = self.calculate_overall_stats(chapter_stats)
        
        # 检测问题
        retention_issues = self.detect_retention_drop(chapter_stats)
        engagement_issues = self.detect_low_engagement(chapter_stats)
        
        all_issues = retention_issues + engagement_issues
        
        # 计算分数（转换为 layer_scores）
        base_score = 100.0
        score_deduction = len(all_issues) * 15.0
        
        # 考虑平均追读率
        if overall.avg_retention_rate < 0.5:
            score_deduction += 20.0
        elif overall.avg_retention_rate < 0.6:
            score_deduction += 10.0
        
        final_score = max(0.0, base_score - score_deduction)
        passed = final_score >= 60
        
        # 构建诊断信息
        diagnostics = []
        if retention_issues:
            diagnostics.append(f"追读率问题：{len(retention_issues)}章")
            diagnostics.extend(retention_issues)
        if engagement_issues:
            diagnostics.append(f"低互动问题：{len(engagement_issues)}章")
            diagnostics.extend(engagement_issues)
        
        if passed:
            diagnostics.append(f"整体数据良好，平均追读率{overall.avg_retention_rate:.1%}")
        
        metadata = {
            "overall_stats": overall.model_dump(),
            "retention_issues": retention_issues,
            "engagement_issues": engagement_issues,
            "score": final_score
        }
        
        return CommercialVerdict(
            passed=passed,
            diagnostics=diagnostics,
            layer_scores={"overall": final_score},
            severity="info" if passed else "warning"
        )
    
    def fix(self, chapter_stats: list[ChapterStats], verdict: CommercialVerdict) -> SkillResult:
        """生成改进建议"""
        if not chapter_stats:
            return SkillResult(
                text="无数据可分析",
                token_usage=TokenUsage(),
                metadata={}
            )
        
        changes = []
        
        # 提取问题章节
        retention_issues = self.detect_retention_drop(chapter_stats)
        engagement_issues = self.detect_low_engagement(chapter_stats)
        
        # 生成建议
        if retention_issues:
            changes.append("建议：对追读率下降的章节进行内容优化，检查是否有情节拖沓或悬念不足的问题")
        
        if engagement_issues:
            changes.append("建议：对低互动章节增加冲突点和钩子，提升读者参与度")
        
        # 针对具体章节给出建议
        for issue in retention_issues + engagement_issues:
            chapter_match = issue.split("章")[0].replace("第", "")
            if chapter_match.isdigit():
                chapter_id = int(chapter_match)
                changes.append(f"第{chapter_id}章需要重点优化")
        
        reason = f"识别出{len(retention_issues)}个追读率问题和{len(engagement_issues)}个低互动问题"
        
        # 将建议文本化
        suggestion_text = "\n".join(changes)
        
        return SkillResult(
            text=suggestion_text,
            token_usage=TokenUsage(),
            metadata={"changes": changes, "reason": reason}
        )
