from pathlib import Path

import pytest

from crawlers.megabox import MegaboxCrawler

FIXTURE = Path(__file__).parent / "fixtures" / "megabox_sample.html"


@pytest.fixture
def html():
    return FIXTURE.read_text(encoding="utf-8")


def test_parse_returns_correct_count(html):
    events = MegaboxCrawler()._parse(html)
    assert len(events) == 2


def test_parse_theater_is_megabox(html):
    events = MegaboxCrawler()._parse(html)
    assert all(e.theater == "Megabox" for e in events)


def test_parse_title(html):
    events = MegaboxCrawler()._parse(html)
    assert events[0].title == "[무대인사] 어벤져스: 엔드게임"


def test_parse_event_type_stage(html):
    events = MegaboxCrawler()._parse(html)
    assert events[0].event_type == "무대인사"


def test_parse_event_type_preview(html):
    events = MegaboxCrawler()._parse(html)
    assert events[1].event_type == "시사회"


def test_parse_date(html):
    events = MegaboxCrawler()._parse(html)
    assert "2025.06.01" in events[0].date


def test_parse_actors_empty(html):
    events = MegaboxCrawler()._parse(html)
    assert events[0].actors == []


def test_parse_booking_url_contains_id(html):
    events = MegaboxCrawler()._parse(html)
    assert "11111" in events[0].booking_url


def test_crawl_returns_empty_on_selenium_error(mocker):
    crawler = MegaboxCrawler()
    mocker.patch.object(crawler, "_fetch_page", side_effect=Exception("selenium error"))
    assert crawler.crawl() == []
