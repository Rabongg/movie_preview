import pytest
from pathlib import Path
from models.event import Event
from services.storage_service import StorageService


@pytest.fixture
def storage(tmp_path):
    return StorageService(data_file=tmp_path / "sent_events.json")


@pytest.fixture
def event_a():
    return Event(theater="CGV", event_type="무대인사", title="어벤져스", date="2025-06-01")


@pytest.fixture
def event_b():
    return Event(theater="Megabox", event_type="시사회", title="인터스텔라", date="2025-06-02")


def test_load_sent_ids_empty_when_no_file(storage):
    assert storage.load_sent_ids() == set()


def test_save_then_load_contains_event_id(storage, event_a):
    storage.save([event_a])
    assert event_a.event_id in storage.load_sent_ids()


def test_filter_new_excludes_already_sent(storage, event_a):
    storage.save([event_a])
    assert storage.filter_new([event_a]) == []


def test_filter_new_keeps_unsent_events(storage, event_a, event_b):
    storage.save([event_a])
    result = storage.filter_new([event_a, event_b])
    assert result == [event_b]


def test_save_appends_without_overwriting(storage, event_a, event_b):
    storage.save([event_a])
    storage.save([event_b])
    sent_ids = storage.load_sent_ids()
    assert event_a.event_id in sent_ids
    assert event_b.event_id in sent_ids


def test_save_creates_parent_directories(tmp_path, event_a):
    deep = tmp_path / "a" / "b" / "sent.json"
    StorageService(data_file=deep).save([event_a])
    assert deep.exists()


def test_saved_json_has_expected_fields(storage, event_a):
    import json
    storage.save([event_a])
    data = json.loads(storage.data_file.read_text(encoding="utf-8"))
    entry = data["sent"][0]
    assert entry["id"] == event_a.event_id
    assert entry["title"] == event_a.title
    assert entry["theater"] == event_a.theater
    assert entry["date"] == event_a.date
    assert entry["event_type"] == event_a.event_type
    assert "sent_at" in entry
