import pytest
from pydantic import BaseModel
from novel.core.skills.base import (
    BaseCommercialSkill,
    CommercialVerdict,
    SkillResult,
    TokenUsage,
)

class MockSkill(BaseCommercialSkill):
    name = "mock_skill"
    
    async def evaluate(self, text: str, context: dict | None = None) -> CommercialVerdict:
        passed = "good" in text.lower()
        return CommercialVerdict(
            passed=passed,
            diagnostics=[] if passed else ["缺少 'good' 关键词"],
            layer_scores={"mock": 80.0 if passed else 40.0},
        )
    
    async def fix(self, text: str, verdict: CommercialVerdict) -> SkillResult:
        if verdict.passed:
            return SkillResult(text=text, token_usage=TokenUsage(prompt_tokens=0, completion_tokens=0))
        fixed = text + " good"
        return SkillResult(
            text=fixed,
            token_usage=TokenUsage(prompt_tokens=10, completion_tokens=5),
        )

@pytest.mark.asyncio
async def test_verdict_passed():
    skill = MockSkill()
    verdict = await skill.evaluate("this is good text")
    assert verdict.passed is True
    assert verdict.diagnostics == []
    assert verdict.layer_scores["mock"] == 80.0

@pytest.mark.asyncio
async def test_verdict_failed():
    skill = MockSkill()
    verdict = await skill.evaluate("this is bad text")
    assert verdict.passed is False
    assert "缺少 'good' 关键词" in verdict.diagnostics
    assert verdict.layer_scores["mock"] == 40.0

@pytest.mark.asyncio
async def test_fix_returns_skill_result():
    skill = MockSkill()
    verdict = await skill.evaluate("bad text")
    result = await skill.fix("bad text", verdict)
    assert isinstance(result, SkillResult)
    assert "good" in result.text
    assert result.token_usage.prompt_tokens == 10
    assert result.token_usage.completion_tokens == 5

def test_token_usage_cost_calculation():
    usage = TokenUsage(prompt_tokens=1000, completion_tokens=500, model="gpt-4o-mini")
    assert usage.estimated_cost > 0
    assert usage.total_tokens == 1500
