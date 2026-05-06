import json
import zipfile
from datetime import date
from pathlib import Path

import pytest

from services.archive_service import ArchiveService


@pytest.fixture
def svc(tmp_path):
    return ArchiveService(
        data_file=tmp_path / "sent_events.json",
        archive_dir=tmp_path / "archive",
    )


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


# ── archive_previous_month ─────────────────────────────────────────────────

def test_archive_creates_zip_for_previous_month(svc, mocker):
    _write_json(svc.data_file, {"sent": [
        {"id": "a", "title": "영화", "theater": "CGV", "date": "2025-04-01",
         "event_type": "무대인사", "sent_at": "2025-04-01T09:00:00"},
    ]})
    mocker.patch.object(svc, "_today", return_value=date(2025, 5, 15))
    svc.archive_previous_month()
    assert (svc.archive_dir / "2025-04.zip").exists()


def test_archive_removes_entries_from_main_file(svc, mocker):
    _write_json(svc.data_file, {"sent": [
        {"id": "a", "title": "4월영화", "theater": "CGV", "date": "2025-04-01",
         "event_type": "무대인사", "sent_at": "2025-04-01T09:00:00"},
        {"id": "b", "title": "5월영화", "theater": "CGV", "date": "2025-05-01",
         "event_type": "무대인사", "sent_at": "2025-05-01T09:00:00"},
    ]})
    mocker.patch.object(svc, "_today", return_value=date(2025, 5, 15))
    svc.archive_previous_month()

    remaining = json.loads(svc.data_file.read_text(encoding="utf-8"))["sent"]
    assert len(remaining) == 1
    assert remaining[0]["id"] == "b"


def test_archive_zip_contains_correct_data(svc, mocker):
    _write_json(svc.data_file, {"sent": [
        {"id": "a", "title": "영화", "theater": "CGV", "date": "2025-04-01",
         "event_type": "무대인사", "sent_at": "2025-04-01T09:00:00"},
    ]})
    mocker.patch.object(svc, "_today", return_value=date(2025, 5, 15))
    svc.archive_previous_month()

    with zipfile.ZipFile(svc.archive_dir / "2025-04.zip") as zf:
        content = json.loads(zf.read("2025-04.json"))
    assert content["sent"][0]["id"] == "a"


def test_archive_skips_if_zip_already_exists(svc, mocker):
    _write_json(svc.data_file, {"sent": [
        {"id": "a", "title": "영화", "theater": "CGV", "date": "2025-04-01",
         "event_type": "무대인사", "sent_at": "2025-04-01T09:00:00"},
    ]})
    svc.archive_dir.mkdir(parents=True, exist_ok=True)
    (svc.archive_dir / "2025-04.zip").touch()
    mocker.patch.object(svc, "_today", return_value=date(2025, 5, 15))
    svc.archive_previous_month()

    remaining = json.loads(svc.data_file.read_text(encoding="utf-8"))["sent"]
    assert len(remaining) == 1  # 삭제 안 됨


def test_archive_does_nothing_when_no_file(svc):
    svc.archive_previous_month()  # should not raise


def test_archive_does_nothing_when_no_prev_month_data(svc, mocker):
    _write_json(svc.data_file, {"sent": [
        {"id": "b", "title": "5월영화", "theater": "CGV", "date": "2025-05-01",
         "event_type": "무대인사", "sent_at": "2025-05-01T09:00:00"},
    ]})
    mocker.patch.object(svc, "_today", return_value=date(2025, 5, 15))
    svc.archive_previous_month()
    assert not (svc.archive_dir / "2025-04.zip").exists()


# ── cleanup_old_archives ───────────────────────────────────────────────────

def test_cleanup_deletes_archives_older_than_retention(svc, mocker):
    svc.archive_dir.mkdir(parents=True, exist_ok=True)
    old = svc.archive_dir / "2025-01.zip"
    keep = svc.archive_dir / "2025-04.zip"
    old.touch()
    keep.touch()

    mocker.patch.object(svc, "_today", return_value=date(2025, 5, 15))
    svc.cleanup_old_archives()

    assert not old.exists()
    assert keep.exists()


def test_cleanup_keeps_archives_within_retention(svc, mocker):
    svc.archive_dir.mkdir(parents=True, exist_ok=True)
    recent = svc.archive_dir / "2025-03.zip"
    recent.touch()

    mocker.patch.object(svc, "_today", return_value=date(2025, 5, 15))
    svc.cleanup_old_archives()

    assert recent.exists()


def test_cleanup_does_nothing_when_no_archive_dir(svc):
    svc.cleanup_old_archives()  # should not raise
