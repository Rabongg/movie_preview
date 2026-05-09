import pytest
from services.crawler_health_service import CrawlerHealthService


@pytest.fixture
def health(tmp_path):
    return CrawlerHealthService(data_file=tmp_path / "crawler_health.json")


def test_record_zero_increments_count(health):
    assert health.record_zero("MegaboxCrawler") == 1
    assert health.record_zero("MegaboxCrawler") == 2


def test_record_success_resets_count(health):
    health.record_zero("MegaboxCrawler")
    health.record_zero("MegaboxCrawler")
    health.record_success("MegaboxCrawler")
    assert health.get_consecutive_zeros("MegaboxCrawler") == 0


def test_crawlers_tracked_independently(health):
    health.record_zero("MegaboxCrawler")
    health.record_zero("MegaboxCrawler")
    health.record_zero("LotteCinemaCrawler")
    assert health.get_consecutive_zeros("MegaboxCrawler") == 2
    assert health.get_consecutive_zeros("LotteCinemaCrawler") == 1


def test_unknown_crawler_returns_zero(health):
    assert health.get_consecutive_zeros("UnknownCrawler") == 0


def test_persists_across_instances(tmp_path):
    health1 = CrawlerHealthService(data_file=tmp_path / "crawler_health.json")
    health1.record_zero("MegaboxCrawler")
    health1.record_zero("MegaboxCrawler")

    health2 = CrawlerHealthService(data_file=tmp_path / "crawler_health.json")
    assert health2.get_consecutive_zeros("MegaboxCrawler") == 2
