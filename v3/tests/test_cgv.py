import json
from pathlib import Path

import pytest

from crawlers.cgv import CGVCrawler

FIXTURE = Path(__file__).parent / "fixtures" / "cgv_sample.json"


@pytest.fixture
def cgv_data():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_parse_returns_correct_count(cgv_data):
    events = CGVCrawler()._parse(cgv_data)
    assert len(events) == 2


def test_parse_theater_is_cgv(cgv_data):
    events = CGVCrawler()._parse(cgv_data)
    assert all(e.theater == "CGV" for e in events)


def test_parse_title(cgv_data):
    events = CGVCrawler()._parse(cgv_data)
    assert events[0].title == "[무대인사] 어벤져스: 엔드게임"


def test_parse_event_type_stage(cgv_data):
    events = CGVCrawler()._parse(cgv_data)
    assert events[0].event_type == "무대인사"


def test_parse_event_type_preview(cgv_data):
    events = CGVCrawler()._parse(cgv_data)
    assert events[1].event_type == "시사회"


def test_parse_date_range(cgv_data):
    events = CGVCrawler()._parse(cgv_data)
    assert "2025-06-01" in events[0].date
    assert "2025-06-07" in events[0].date


def test_parse_single_date_when_start_equals_end(cgv_data):
    events = CGVCrawler()._parse(cgv_data)
    # 두 번째 이벤트는 같은 날
    assert events[1].date == "2025-06-10"


def test_parse_actors(cgv_data):
    events = CGVCrawler()._parse(cgv_data)
    assert "로버트 다우니 주니어" in events[0].actors
    assert "크리스 에반스" in events[0].actors


def test_parse_empty_actors(cgv_data):
    events = CGVCrawler()._parse(cgv_data)
    assert events[1].actors == []


def test_parse_booking_url(cgv_data):
    events = CGVCrawler()._parse(cgv_data)
    assert "12345" in events[0].booking_url


def test_crawl_returns_empty_on_network_error(mocker):
    crawler = CGVCrawler()
    mocker.patch.object(crawler, "_fetch_data", side_effect=Exception("network error"))
    assert crawler.crawl() == []
