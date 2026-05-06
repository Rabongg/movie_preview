import pytest
from models.event import Event


def test_event_id_is_deterministic():
    e1 = Event(theater="CGV", event_type="무대인사", title="어벤져스", date="2025-06-01")
    e2 = Event(theater="CGV", event_type="무대인사", title="어벤져스", date="2025-06-01")
    assert e1.event_id == e2.event_id


def test_event_id_differs_by_theater():
    cgv = Event(theater="CGV", event_type="무대인사", title="어벤져스", date="2025-06-01")
    mega = Event(theater="Megabox", event_type="무대인사", title="어벤져스", date="2025-06-01")
    assert cgv.event_id != mega.event_id


def test_event_id_differs_by_date():
    e1 = Event(theater="CGV", event_type="무대인사", title="어벤져스", date="2025-06-01")
    e2 = Event(theater="CGV", event_type="무대인사", title="어벤져스", date="2025-06-02")
    assert e1.event_id != e2.event_id


def test_event_id_differs_by_event_type():
    e1 = Event(theater="CGV", event_type="무대인사", title="어벤져스", date="2025-06-01")
    e2 = Event(theater="CGV", event_type="시사회", title="어벤져스", date="2025-06-01")
    assert e1.event_id != e2.event_id


def test_event_id_differs_by_title():
    e1 = Event(theater="CGV", event_type="무대인사", title="영화A", date="2025-06-01")
    e2 = Event(theater="CGV", event_type="무대인사", title="영화B", date="2025-06-01")
    assert e1.event_id != e2.event_id


def test_optional_fields_have_defaults():
    event = Event(theater="CGV", event_type="무대인사", title="어벤져스", date="2025-06-01")
    assert event.time == ""
    assert event.location == ""
    assert event.actors == []
    assert event.booking_url == ""


def test_event_id_is_md5_hex_string():
    event = Event(theater="CGV", event_type="무대인사", title="어벤져스", date="2025-06-01")
    assert len(event.event_id) == 32
    assert all(c in "0123456789abcdef" for c in event.event_id)
