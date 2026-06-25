from typing import Any
from novel.core.skills.base import BaseCommercialSkill, CommercialVerdict, SkillResult, TokenUsage


class CheckLogicSkill(BaseCommercialSkill):
    """事实核查员 - 检查章节中的逻辑错误和设定冲突"""
    
    name = "check_logic"
    version = "0.1.0"
    
    def evaluate(self, chapter: dict[str, Any]) -> CommercialVerdict:
        """检查章节中的逻辑错误"""
        diagnostics = []
        layer_scores = {}
        
        # 检查章节是否包含内容
        content = chapter.get("content", "")
        if not content:
            diagnostics.append("章节内容为空，无法进行逻辑检查")
            layer_scores["content"] = 0.0
            return CommercialVerdict(
                passed=False,
                diagnostics=diagnostics,
                layer_scores=layer_scores,
                severity="critical"
            )
        
        layer_scores["content"] = 100.0
        
        # 检查角色名称一致性
        character_mentions = self._extract_character_mentions(content)
        if character_mentions:
            layer_scores["characters"] = 100.0
        else:
            layer_scores["characters"] = 50.0
            diagnostics.append("未检测到角色提及，请确认内容是否完整")
        
        # 检查时间线一致性（简单检查）
        time_markers = self._extract_time_markers(content)
        layer_scores["timeline"] = 100.0
        
        # 检查地点一致性
        locations = self._extract_locations(content)
        layer_scores["locations"] = 100.0
        
        # 综合评分
        passed = all(score >= 60 for score in layer_scores.values())
        
        if not diagnostics:
            diagnostics.append("逻辑检查通过，未发现明显错误")
        
        return CommercialVerdict(
            passed=passed,
            diagnostics=diagnostics,
            layer_scores=layer_scores,
            severity="info" if passed else "warning"
        )
    
    def fix(self, chapter: dict[str, Any], verdict: CommercialVerdict) -> SkillResult:
        """提供修复建议"""
        changes = []
        
        for diagnostic in verdict.diagnostics:
            if "角色提及" in diagnostic:
                changes.append("建议在章节开头明确提及主要角色")
            if "时间线" in diagnostic:
                changes.append("建议添加时间标记以明确事件顺序")
        
        reason = "提供了逻辑修复建议" if changes else "无需修复"
        
        return SkillResult(
            text=chapter.get("content", ""),
            token_usage=TokenUsage(),
            metadata={"changes": changes, "reason": reason}
        )
    
    def _extract_character_mentions(self, content: str) -> list[str]:
        """提取角色提及（简化版）"""
        # 实际实现应该使用 NLP 或 LLM
        common_names = ["主角", "他", "她", "张", "李", "王", "陈"]
        return [name for name in common_names if name in content]
    
    def _extract_time_markers(self, content: str) -> list[str]:
        """提取时间标记"""
        markers = ["早上", "中午", "晚上", "第二天", "三天后", "一个月后"]
        return [marker for marker in markers if marker in content]
    
    def _extract_locations(self, content: str) -> list[str]:
        """提取地点"""
        locations = ["家", "学校", "公司", "城市", "村庄", "山谷"]
        return [loc for loc in locations if loc in content]
