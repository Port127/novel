from pydantic import BaseModel
from typing import Literal
from novel.core.workflow.cost_tracker import CostTracker

class ReserveStatus(BaseModel):
    level: Literal["green", "yellow", "red"]
    reserve_count: int
    
    @property
    def is_warning(self) -> bool:
        return self.level in ("yellow", "red")

class DailyUpdateManager:
    def __init__(
        self,
        written_chapters: int,
        published_chapters: int,
        mode: Literal["fast", "fine"] = "fine",
        daily_budget: float = 15.0,
    ):
        self.written_chapters = written_chapters
        self.published_chapters = published_chapters
        self.mode = mode
        self.cost_tracker = CostTracker(daily_budget=daily_budget)
        self._quality_scores = []
    
    def check_reserves(self) -> ReserveStatus:
        reserve = self.written_chapters - self.published_chapters
        
        if reserve >= 10:
            return ReserveStatus(level="green", reserve_count=reserve)
        elif reserve >= 6:
            return ReserveStatus(level="yellow", reserve_count=reserve)
        else:
            return ReserveStatus(level="red", reserve_count=reserve)
    
    def get_skill_pipeline(self) -> list[str]:
        status = self.check_reserves()
        
        # 红色预警：强制快速模式
        if status.level == "red":
            return ["flesh_out_chapter", "anti_ai_polish"]
        
        if self.mode == "fast":
            return ["flesh_out_chapter", "anti_ai_polish"]
        else:  # fine mode
            return [
                "flesh_out_chapter",
                "check_logic",
                "anti_ai_polish",
                "audit_hooks",
            ]
    
    def get_recommended_mode(self) -> Literal["fast", "fine"]:
        status = self.check_reserves()
        if status.level == "red":
            return "fast"
        return self.mode
    
    def record_quality_score(self, score: float) -> None:
        """记录章节质量评分（anti-ai-polish 五层综合分）"""
        self._quality_scores.append(score)
        # 只保留最近 3 章
        if len(self._quality_scores) > 3:
            self._quality_scores = self._quality_scores[-3:]
    
    def should_suggest_leave(self) -> bool:
        """连续 3 章质量评分低于 60 分，建议请假"""
        if len(self._quality_scores) < 3:
            return False
        return all(score < 60 for score in self._quality_scores[-3:])
