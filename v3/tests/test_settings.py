import importlib

import config.settings as settings


def test_receiver_emails_parsed_as_list(monkeypatch):
    monkeypatch.setenv("RECEIVER_EMAILS", "a@example.com,b@example.com")
    importlib.reload(settings)
    assert settings.RECEIVER_EMAILS == ["a@example.com", "b@example.com"]


def test_receiver_emails_strips_whitespace(monkeypatch):
    monkeypatch.setenv("RECEIVER_EMAILS", " a@example.com , b@example.com ")
    importlib.reload(settings)
    assert settings.RECEIVER_EMAILS == ["a@example.com", "b@example.com"]


def test_receiver_emails_returns_empty_list_when_env_is_empty(monkeypatch):
    monkeypatch.setenv("RECEIVER_EMAILS", "")
    importlib.reload(settings)
    assert settings.RECEIVER_EMAILS == []


def test_send_hour_morning_defaults_to_9_when_env_not_set(monkeypatch):
    monkeypatch.delenv("SEND_HOUR_MORNING", raising=False)
    importlib.reload(settings)
    assert settings.SEND_HOUR_MORNING == 9
