import pytest
from novel.core.workflow.manuscript_store import ManuscriptStore, ManuscriptTier

def test_manuscript_tier_classification():
    store = ManuscriptStore()
    
    store.add("chapter_101", tier=ManuscriptTier.REFINED)
    store.add("chapter_102", tier=ManuscriptTier.DRAFT)
    store.add("chapter_103", tier=ManuscriptTier.OUTLINE)
    
    assert store.count(ManuscriptTier.REFINED) == 1
    assert store.count(ManuscriptTier.DRAFT) == 1
    assert store.count(ManuscriptTier.OUTLINE) == 1
    assert store.total_count == 3

def test_consume_priority():
    """发布时优先消耗精修稿"""
    store = ManuscriptStore()
    store.add("chapter_101", tier=ManuscriptTier.REFINED)
    store.add("chapter_102", tier=ManuscriptTier.DRAFT)
    
    consumed = store.consume_next()
    assert consumed == "chapter_101"
    assert store.count(ManuscriptTier.REFINED) == 0
    
    consumed = store.consume_next()
    assert consumed == "chapter_102"

def test_empty_store_returns_none():
    store = ManuscriptStore()
    assert store.consume_next() is None
