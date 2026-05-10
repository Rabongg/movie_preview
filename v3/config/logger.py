import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

_COLORS = {
    "WARNING": "\033[33m",   # yellow
    "ERROR": "\033[31m",     # red
    "CRITICAL": "\033[1;31m", # bold red
}
_RESET = "\033[0m"


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        color = _COLORS.get(record.levelname)
        return f"{color}{msg}{_RESET}" if color else msg


def setup_logger(log_dir: str = "logs") -> logging.Logger:
    Path(log_dir).mkdir(exist_ok=True)

    logger = logging.getLogger("movie_preview")
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    fmt_str = "[%(asctime)s] %(levelname)s - %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    file_handler = RotatingFileHandler(
        f"{log_dir}/app.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(ColorFormatter(fmt_str, datefmt=datefmt))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter(fmt_str, datefmt=datefmt))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
