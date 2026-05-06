from unittest.mock import MagicMock, patch

import pytest

from models.event import Event
from services.storage_service import StorageService


@pytest.fixture
def new_event():
    return Event(theater="CGV", event_type="무대인사", title="어벤져스", date="2025-06-01")


def _run_main(mocker, cgv_events, megabox_events, lotte_events, storage, smtp_mock):
    mocker.patch("main.CGVCrawler").return_value.crawl.return_value = cgv_events
    mocker.patch("main.MegaboxCrawler").return_value.crawl.return_value = megabox_events
    mocker.patch("main.LotteCinemaCrawler").return_value.crawl.return_value = lotte_events
    mocker.patch("main.StorageService", return_value=storage)
    mocker.patch("main.ArchiveService").return_value.run.return_value = None
    mocker.patch("main.SENDER_EMAIL", "sender@gmail.com")
    mocker.patch("main.SENDER_KEY", "key")
    mocker.patch("main.RECEIVER_EMAILS", ["recipient@example.com"])

    with patch("smtplib.SMTP_SSL") as mock_smtp_cls:
        mock_server = MagicMock()
        mock_smtp_cls.return_value.__enter__.return_value = mock_server
        smtp_mock["server"] = mock_server
        from main import main
        main()


def test_main_sends_email_for_new_events(mocker, tmp_path, new_event):
    storage = StorageService(data_file=tmp_path / "sent.json")
    smtp = {}
    _run_main(mocker, [new_event], [], [], storage, smtp)

    smtp["server"].sendmail.assert_called_once()


def test_main_saves_events_after_sending(mocker, tmp_path, new_event):
    storage = StorageService(data_file=tmp_path / "sent.json")
    smtp = {}
    _run_main(mocker, [new_event], [], [], storage, smtp)

    assert new_event.event_id in storage.load_sent_ids()


def test_main_skips_email_when_no_new_events(mocker, tmp_path, new_event):
    storage = StorageService(data_file=tmp_path / "sent.json")
    storage.save([new_event])  # 이미 발송됨
    smtp = {}
    _run_main(mocker, [new_event], [], [], storage, smtp)

    smtp["server"].sendmail.assert_not_called()


def test_main_collects_from_all_crawlers(mocker, tmp_path):
    e1 = Event(theater="CGV", event_type="무대인사", title="영화1", date="2025-06-01")
    e2 = Event(theater="Megabox", event_type="시사회", title="영화2", date="2025-06-01")
    e3 = Event(theater="LotteCinema", event_type="무대인사", title="영화3", date="2025-06-01")
    storage = StorageService(data_file=tmp_path / "sent.json")
    smtp = {}
    _run_main(mocker, [e1], [e2], [e3], storage, smtp)

    smtp["server"].sendmail.assert_called_once()
    sent_ids = storage.load_sent_ids()
    assert e1.event_id in sent_ids
    assert e2.event_id in sent_ids
    assert e3.event_id in sent_ids


def test_main_does_not_save_when_email_fails(mocker, tmp_path, new_event):
    storage = StorageService(data_file=tmp_path / "sent.json")
    mocker.patch("main.CGVCrawler").return_value.crawl.return_value = [new_event]
    mocker.patch("main.MegaboxCrawler").return_value.crawl.return_value = []
    mocker.patch("main.LotteCinemaCrawler").return_value.crawl.return_value = []
    mocker.patch("main.StorageService", return_value=storage)
    mocker.patch("main.ArchiveService").return_value.run.return_value = None
    mocker.patch("main.SENDER_EMAIL", "sender@gmail.com")
    mocker.patch("main.SENDER_KEY", "key")
    mocker.patch("main.RECEIVER_EMAILS", ["recipient@example.com"])

    with patch("smtplib.SMTP_SSL", side_effect=Exception("SMTP 연결 실패")):
        from main import main
        main()

    assert storage.load_sent_ids() == set()
