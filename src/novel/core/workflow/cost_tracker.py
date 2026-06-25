from datetime import date
from novel.core.skills.base import TokenUsage

class BudgetExceededError(Exception):
    pass

class TokenLimitExceededError(Exception):
    pass

# 每模型单次调用 token 上限（prompt + completion）
TOKEN_LIMITS_PER_CALL = {
    "cheap": 4000,
    "expensive": 8000,
}

# 模型分级映射
MODEL_TIER = {
    "gpt-4o": "expensive",
    "gpt-4o-mini": "cheap",
    "gpt-3.5-turbo": "cheap",
}

class CostTracker:
    def __init__(self, daily_budget: float = 15.0, hard_limit: bool = False):
        self.daily_budget = daily_budget
        self.hard_limit = hard_limit
        self._total_cost = 0.0
        self._total_tokens = 0
        self._date = date.today()
    
    def record(self, usage: TokenUsage) -> None:
        # 检查单次调用上限
        tier = MODEL_TIER.get(usage.model, "cheap")
        limit = TOKEN_LIMITS_PER_CALL[tier]
        if usage.total_tokens > limit:
            raise TokenLimitExceededError(
                f"单次调用超出 {tier} 级别上限：{usage.total_tokens} > {limit}（模型：{usage.model}）"
            )
        
        self._total_cost += usage.estimated_cost
        self._total_tokens += usage.total_tokens
        
        if self.hard_limit and self._total_cost > self.daily_budget:
            raise BudgetExceededError(
                f"超出每日预算：${self._total_cost:.4f} > ${self.daily_budget:.4f}"
            )
    
    @property
    def total_cost(self) -> float:
        return round(self._total_cost, 6)
    
    @property
    def total_tokens(self) -> int:
        return self._total_tokens
    
    @property
    def remaining_budget(self) -> float:
        return self.daily_budget - self._total_cost
    
    @property
    def is_warning_triggered(self) -> bool:
        return self._total_cost >= self.daily_budget * 0.8
