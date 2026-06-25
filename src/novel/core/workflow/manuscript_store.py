from enum import Enum
from collections import deque

class ManuscriptTier(str, Enum):
    REFINED = "refined"   # 已通过 anti-ai-polish，可直接发布
    DRAFT = "draft"       # 已扩写但未精修
    OUTLINE = "outline"   # 仅有节拍表，需完整扩写

class ManuscriptStore:
    def __init__(self):
        self._store = {tier: deque() for tier in ManuscriptTier}
    
    def add(self, chapter_id: str, tier: ManuscriptTier) -> None:
        self._store[tier].append(chapter_id)
    
    def count(self, tier: ManuscriptTier) -> int:
        return len(self._store[tier])
    
    @property
    def total_count(self) -> int:
        return sum(len(q) for q in self._store.values())
    
    def consume_next(self) -> str | None:
        """发布时优先消耗精修稿，其次粗稿，最后大纲稿"""
        for tier in [ManuscriptTier.REFINED, ManuscriptTier.DRAFT, ManuscriptTier.OUTLINE]:
            if self._store[tier]:
                return self._store[tier].popleft()
        return None
