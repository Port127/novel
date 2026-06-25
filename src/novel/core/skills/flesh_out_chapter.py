"""
FleshOutChapterSkill - 节拍扩写员
根据章节大纲和节拍表，将简要大纲扩写为完整的章节正文
"""
from typing import Any
from novel.core.skills.base import BaseCommercialSkill, CommercialVerdict, SkillResult, TokenUsage


class FleshOutChapterSkill(BaseCommercialSkill):
    """节拍扩写员 - 将大纲扩写为完整章节"""
    
    name = "flesh_out_chapter"
    version = "0.1.0"
    
    def evaluate(self, outline: dict[str, Any]) -> CommercialVerdict:
        """评估大纲是否适合扩写"""
        diagnostics = []
        layer_scores = {}
        
        # 检查必要字段
        required_fields = ["title", "content", "beats"]
        missing_fields = [f for f in required_fields if f not in outline or not outline[f]]
        
        if missing_fields:
            diagnostics.append(f"大纲缺少必要字段: {', '.join(missing_fields)}")
            layer_scores["structure"] = 0.0
            return CommercialVerdict(
                passed=False,
                diagnostics=diagnostics,
                layer_scores=layer_scores,
                severity="critical"
            )
        
        # 检查节拍数量
        beats = outline.get("beats", [])
        if len(beats) < 3:
            diagnostics.append("节拍数量过少（至少需要3个节拍）")
            layer_scores["structure"] = 30.0
        elif len(beats) > 15:
            diagnostics.append("节拍数量过多，可能导致节奏拖沓")
            layer_scores["structure"] = 70.0
        else:
            layer_scores["structure"] = 100.0
        
        # 检查内容长度
        content = outline.get("content", "")
        if len(content) < 50:
            diagnostics.append("大纲内容过短，需要更多细节")
            layer_scores["detail"] = 40.0
        else:
            layer_scores["detail"] = 100.0
        
        # 检查目标字数
        target_words = outline.get("target_words", 0)
        if target_words < 2000:
            diagnostics.append("目标字数过少（建议至少2000字）")
            layer_scores["length"] = 50.0
        elif target_words > 5000:
            diagnostics.append("目标字数过多，建议拆分章节")
            layer_scores["length"] = 70.0
        else:
            layer_scores["length"] = 100.0
        
        passed = all(score >= 60 for score in layer_scores.values())
        
        if not diagnostics:
            diagnostics.append("大纲结构良好，可以扩写")
        
        return CommercialVerdict(
            passed=passed,
            diagnostics=diagnostics,
            layer_scores=layer_scores,
            severity="info" if passed else "warning"
        )
    
    def fix(self, outline: dict[str, Any], verdict: CommercialVerdict) -> SkillResult:
        """修复大纲问题"""
        fixed_outline = outline.copy()
        changes = []
        
        # 如果缺少标题，生成默认标题
        if not fixed_outline.get("title"):
            fixed_outline["title"] = "第X章 未命名章节"
            changes.append("添加了默认标题")
        
        # 如果节拍过少，添加基础节拍
        beats = fixed_outline.get("beats", [])
        if len(beats) < 3:
            base_beats = [
                {"id": 1, "description": "开场：场景设置", "target_words": 500},
                {"id": 2, "description": "发展：情节推进", "target_words": 1000},
                {"id": 3, "description": "结尾：悬念或转折", "target_words": 500}
            ]
            fixed_outline["beats"] = base_beats[:3-len(beats)] + beats
            changes.append(f"补充节拍至{len(fixed_outline['beats'])}个")
        
        # 如果目标字数缺失，设置默认值
        if not fixed_outline.get("target_words"):
            fixed_outline["target_words"] = 3000
            changes.append("设置默认目标字数：3000字")
        
        reason = "修复了大纲的结构问题" if changes else "大纲无需修复"
        
        # 将修复后的内容序列化为文本
        import json
        text_content = json.dumps(fixed_outline, ensure_ascii=False, indent=2)
        
        return SkillResult(
            text=text_content,
            token_usage=TokenUsage(),
            metadata={"changes": changes, "reason": reason}
        )
