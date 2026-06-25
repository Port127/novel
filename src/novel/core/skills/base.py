from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Literal

# 模型定价表 (每 1K token，单位：美元)
MODEL_PRICING = {
    "gpt-4o": {"prompt": 0.005, "completion": 0.015},
    "gpt-4o-mini": {"prompt": 0.00015, "completion": 0.0006},
    "gpt-3.5-turbo": {"prompt": 0.0005, "completion": 0.0015},
}

class TokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    model: str = "gpt-4o-mini"
    
    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens
    
    @property
    def estimated_cost(self) -> float:
        pricing = MODEL_PRICING.get(self.model, MODEL_PRICING["gpt-4o-mini"])
        prompt_cost = (self.prompt_tokens / 1000) * pricing["prompt"]
        completion_cost = (self.completion_tokens / 1000) * pricing["completion"]
        return round(prompt_cost + completion_cost, 6)

class CommercialVerdict(BaseModel):
    passed: bool
    diagnostics: list[str] = Field(default_factory=list)
    layer_scores: dict[str, float] = Field(default_factory=dict)
    severity: Literal["info", "warning", "critical"] = "info"

class SkillResult(BaseModel):
    text: str
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    metadata: dict = Field(default_factory=dict)

class BaseCommercialSkill(ABC):
    name: str = "unnamed skill"
    
    @abstractmethod
    async def evaluate(self, text: str, context: dict | None = None) -> CommercialVerdict:
        """评估文本质量，返回结构化判定结果"""
        ...
    
    @abstractmethod
    async def fix(self, text: str, verdict: CommercialVerdict) -> SkillResult:
        """根据判定结果修复文本，返回修复后的文本和 token 消耗"""
        ...
