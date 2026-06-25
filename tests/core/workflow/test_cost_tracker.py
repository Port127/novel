import pytest
from novel.core.workflow.cost_tracker import CostTracker, BudgetExceededError, TokenLimitExceededError
from novel.core.skills.base import TokenUsage

def test_cost_tracker_accumulates_usage():
    tracker = CostTracker(daily_budget=15.0)
    
    usage1 = TokenUsage(prompt_tokens=1000, completion_tokens=500, model="gpt-4o-mini")
    tracker.record(usage1)
    
    usage2 = TokenUsage(prompt_tokens=2000, completion_tokens=1000, model="gpt-4o-mini")
    tracker.record(usage2)
    
    assert tracker.total_tokens == 4500
    assert tracker.total_cost > 0
    assert tracker.total_cost < 15.0

def test_cost_tracker_triggers_warning():
    tracker = CostTracker(daily_budget=0.001)
    
    # gpt-4o 单次上限 8000 tokens
    usage = TokenUsage(prompt_tokens=5000, completion_tokens=2000, model="gpt-4o")
    tracker.record(usage)
    
    assert tracker.is_warning_triggered
    assert tracker.remaining_budget < 0

def test_cost_tracker_raises_on_exceed():
    tracker = CostTracker(daily_budget=0.001, hard_limit=True)
    
    # gpt-4o 单次上限 8000 tokens，这里用合规数
    usage = TokenUsage(prompt_tokens=5000, completion_tokens=2000, model="gpt-4o")
    
    with pytest.raises(BudgetExceededError):
        tracker.record(usage)

def test_token_limit_per_call():
    """单次调用 token 上限检测"""
    tracker = CostTracker()
    
    # gpt-4o-mini 上限 4000 tokens
    cheap_usage = TokenUsage(prompt_tokens=3500, completion_tokens=3500, model="gpt-4o-mini")
    with pytest.raises(TokenLimitExceededError):
        tracker.record(cheap_usage)
    
    # gpt-4o 上限 8000 tokens
    expensive_usage = TokenUsage(prompt_tokens=7500, completion_tokens=7500, model="gpt-4o")
    with pytest.raises(TokenLimitExceededError):
        tracker.record(expensive_usage)

def test_token_limit_within_bounds():
    """token 在上限内应正常通过"""
    tracker = CostTracker()
    
    usage = TokenUsage(prompt_tokens=2000, completion_tokens=1000, model="gpt-4o-mini")
    tracker.record(usage)
    assert tracker.total_tokens == 3000
