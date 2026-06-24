import pytest
from novel.core.skills.pipeline import Skill, run_skill_pipeline

@pytest.mark.asyncio
async def test_run_skill_pipeline():
    skill1 = Skill(name="Remove AI", trigger_phase="deslop", system_prompt="Remove metaphors")
    skill2 = Skill(name="Add Hook", trigger_phase="hook", system_prompt="Add suspense at end")
    
    # Mocking the LLM modifier function for the test
    async def mock_modifier(text, prompt):
        return f"{text} -> {prompt[:5]}"
        
    result = await run_skill_pipeline([skill1, skill2], "Chapter start.", llm_func=mock_modifier)
    assert result == "Chapter start. -> Remov -> Add s"
