import json
from pathlib import Path
from unittest.mock import patch

import pytest

from crawlers.lotte_cinema import LotteCinemaCrawler

FIXTURE = Path(__file__).parent / "fixtures" / "lotte_sample.json"


@pytest.fixture
def items():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))["Items"]


def test_parse_returns_correct_count(items):
    events = LotteCinemaCrawler()._parse(items)
    assert len(events) == 2


def test_parse_theater_is_lotte(items):
    events = LotteCinemaCrawler()._parse(items)
    assert all(e.theater == "LotteCinema" for e in events)


def test_parse_title(items):
    events = LotteCinemaCrawler()._parse(items)
    assert events[0].title == "<무대인사> 어벤져스: 엔드게임"


def test_parse_event_type_stage(items):
    events = LotteCinemaCrawler()._parse(items)
    assert events[0].event_type == "무대인사"


def test_parse_event_type_preview(items):
    events = LotteCinemaCrawler()._parse(items)
    assert events[1].event_type == "시사회"


def test_parse_date(items):
    events = LotteCinemaCrawler()._parse(items)
    assert "2025.06.01" in events[0].date


def test_parse_actors_empty(items):
    events = LotteCinemaCrawler()._parse(items)
    assert events[0].actors == []


def test_parse_booking_url_contains_event_id(items):
    events = LotteCinemaCrawler()._parse(items)
    assert "401070011111111" in events[0].booking_url


def test_crawl_returns_empty_on_request_error(mocker):
    crawler = LotteCinemaCrawler()
    mocker.patch.object(crawler, "_fetch_data", side_effect=Exception("request error"))
    assert crawler.crawl() == []
