import pytest
from novel.core.workflow.daily_manager import DailyUpdateManager, ReserveStatus

def test_stock_warning_yellow():
    manager = DailyUpdateManager(
        written_chapters=105,
        published_chapters=98,
        mode="fine",
    )
    status = manager.check_reserves()
    assert status.level == "yellow"
    assert status.reserve_count == 7
    assert status.is_warning

def test_stock_warning_red():
    manager = DailyUpdateManager(
        written_chapters=103,
        published_chapters=99,
        mode="fine",
    )
    status = manager.check_reserves()
    assert status.level == "red"
    assert status.reserve_count == 4

def test_stock_warning_normal():
    manager = DailyUpdateManager(
        written_chapters=120,
        published_chapters=100,
        mode="fine",
    )
    status = manager.check_reserves()
    assert status.level == "green"
    assert not status.is_warning

def test_fast_mode_skills():
    manager = DailyUpdateManager(written_chapters=110, published_chapters=100, mode="fast")
    skills = manager.get_skill_pipeline()
    assert "flesh_out_chapter" in skills
    assert "anti_ai_polish" in skills
    assert len(skills) == 2

def test_fine_mode_skills():
    manager = DailyUpdateManager(written_chapters=110, published_chapters=100, mode="fine")
    skills = manager.get_skill_pipeline()
    assert len(skills) >= 4

def test_emergency_mode_activation():
    manager = DailyUpdateManager(
        written_chapters=104,
        published_chapters=100,
        mode="fine",
    )
    status = manager.check_reserves()
    assert status.level == "red"
    
    recommended_mode = manager.get_recommended_mode()
    assert recommended_mode == "fast"

def test_leave_suggestion_on_low_quality():
    """连续低质量应该建议请假"""
    manager = DailyUpdateManager(written_chapters=110, published_chapters=100, mode="fine")
    
    manager.record_quality_score(45.0)
    manager.record_quality_score(50.0)
    manager.record_quality_score(55.0)
    
    assert manager.should_suggest_leave() is True

def test_no_leave_suggestion_on_normal_quality():
    """正常质量不应建议请假"""
    manager = DailyUpdateManager(written_chapters=110, published_chapters=100, mode="fine")
    
    manager.record_quality_score(75.0)
    manager.record_quality_score(80.0)
    
    assert manager.should_suggest_leave() is False

def test_leave_suggestion_insufficient_data():
    """少于3章数据不应建议请假"""
    manager = DailyUpdateManager(written_chapters=110, published_chapters=100, mode="fine")
    
    manager.record_quality_score(45.0)
    
    assert manager.should_suggest_leave() is False

def test_reserve_status_properties():
    """ReserveStatus 属性测试"""
    status_green = ReserveStatus(level="green", reserve_count=15)
    assert not status_green.is_warning
    
    status_yellow = ReserveStatus(level="yellow", reserve_count=8)
    assert status_yellow.is_warning
    
    status_red = ReserveStatus(level="red", reserve_count=3)
    assert status_red.is_warning
