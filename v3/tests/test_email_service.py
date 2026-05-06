import pytest
from unittest.mock import MagicMock, patch

from models.event import Event
from services.email_service import EmailService


@pytest.fixture
def service():
    return EmailService(
        sender_email="sender@gmail.com",
        sender_key="test_key",
        receiver_emails=["a@example.com", "b@example.com"],
    )


@pytest.fixture
def events():
    return [
        Event(
            theater="CGV", event_type="무대인사", title="어벤져스",
            date="2025-06-01", time="14:00", location="CGV 강남",
            actors=["배우1", "배우2"], booking_url="https://cgv.co.kr/book/1",
        ),
        Event(
            theater="Megabox", event_type="시사회", title="인터스텔라",
            date="2025-06-02", location="메가박스 코엑스",
        ),
    ]


def test_send_returns_false_for_empty_events(service):
    assert service.send([]) is False


def test_send_calls_smtp_and_returns_true(service, events):
    with patch("smtplib.SMTP_SSL") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        result = service.send(events)

    assert result is True
    mock_server.login.assert_called_once_with("sender@gmail.com", "test_key")
    mock_server.sendmail.assert_called_once()


def test_send_passes_all_recipients(service, events):
    with patch("smtplib.SMTP_SSL") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        service.send(events)

    args = mock_server.sendmail.call_args[0]
    assert args[1] == ["a@example.com", "b@example.com"]


def test_send_returns_false_on_smtp_error(service, events):
    with patch("smtplib.SMTP_SSL", side_effect=Exception("connection refused")):
        result = service.send(events)
    assert result is False


def test_build_html_contains_all_titles(service, events):
    html = service._build_html(events)
    assert "어벤져스" in html
    assert "인터스텔라" in html


def test_build_html_contains_event_types(service, events):
    html = service._build_html(events)
    assert "무대인사" in html
    assert "시사회" in html


def test_build_html_contains_booking_url(service):
    event = Event(
        theater="CGV", event_type="무대인사", title="영화",
        date="2025-06-01", booking_url="https://example.com/book/99",
    )
    html = service._build_html([event])
    assert "https://example.com/book/99" in html


def test_build_html_contains_actors(service):
    event = Event(
        theater="CGV", event_type="무대인사", title="영화",
        date="2025-06-01", actors=["배우A", "배우B"],
    )
    html = service._build_html([event])
    assert "배우A" in html
    assert "배우B" in html


def test_build_html_omits_booking_button_when_no_url(service):
    event = Event(theater="CGV", event_type="무대인사", title="영화", date="2025-06-01")
    html = service._build_html([event])
    assert "예매하기" not in html


def test_build_html_shows_event_count(service, events):
    html = service._build_html(events)
    assert "2건" in html
