import logging

import pytest

from config.logger import ColorFormatter, setup_logger


def _make_record(level: int, message: str) -> logging.LogRecord:
    record = logging.LogRecord(
        name="test",
        level=level,
        pathname="",
        lineno=0,
        msg=message,
        args=(),
        exc_info=None,
    )
    return record


def test_color_formatter_applies_yellow_to_warning():
    formatter = ColorFormatter("%(message)s")
    record = _make_record(logging.WARNING, "경고 메시지")
    result = formatter.format(record)
    assert result.startswith("\033[33m")
    assert result.endswith("\033[0m")


def test_color_formatter_applies_red_to_error():
    formatter = ColorFormatter("%(message)s")
    record = _make_record(logging.ERROR, "에러 메시지")
    result = formatter.format(record)
    assert result.startswith("\033[31m")
    assert result.endswith("\033[0m")


def test_color_formatter_does_not_apply_color_to_info():
    formatter = ColorFormatter("%(message)s")
    record = _make_record(logging.INFO, "정보 메시지")
    result = formatter.format(record)
    assert result == "정보 메시지"


def test_setup_logger_returns_logger_with_info_level(tmp_path):
    log_dir = str(tmp_path / "logs")
    logger = logging.getLogger("movie_preview")
    logger.handlers.clear()

    result = setup_logger(log_dir=log_dir)

    assert result.level == logging.INFO


def test_setup_logger_does_not_duplicate_handlers_on_second_call(tmp_path):
    # logger 이름을 유니크하게 해서 다른 테스트와 충돌 방지
    log_dir = str(tmp_path / "logs")
    logger = logging.getLogger("movie_preview")
    # 혹시 이전 테스트가 세팅했을 수 있으니 초기화
    logger.handlers.clear()

    setup_logger(log_dir=log_dir)
    handler_count_after_first = len(logger.handlers)

    setup_logger(log_dir=log_dir)
    handler_count_after_second = len(logger.handlers)

    assert handler_count_after_second == handler_count_after_first
