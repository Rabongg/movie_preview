import json
import logging
import zipfile
from datetime import date, timedelta
from pathlib import Path

logger = logging.getLogger("movie_preview")


class ArchiveService:
    def __init__(
        self,
        data_file: Path = Path("data/sent_events.json"),
        archive_dir: Path = Path("data/archive"),
        retention_months: int = 2,
    ):
        self.data_file = data_file
        self.archive_dir = archive_dir
        self.retention_months = retention_months

    def _today(self) -> date:
        return date.today()

    def run(self) -> None:
        try:
            self.archive_previous_month()
            self.cleanup_old_archives()
        except Exception as e:
            logger.error(f"Archive process failed: {e}")

    def archive_previous_month(self) -> None:
        if not self.data_file.exists():
            return

        today = self._today()
        prev_month = today.replace(day=1) - timedelta(days=1)
        target_ym = prev_month.strftime("%Y-%m")

        self.archive_dir.mkdir(parents=True, exist_ok=True)
        zip_path = self.archive_dir / f"{target_ym}.zip"
        if zip_path.exists():
            return

        with open(self.data_file, encoding="utf-8") as f:
            data = json.load(f)

        prev_entries = [
            e for e in data.get("sent", [])
            if e.get("sent_at", "").startswith(target_ym)
        ]
        if not prev_entries:
            return

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(
                f"{target_ym}.json",
                json.dumps({"sent": prev_entries}, ensure_ascii=False, indent=2),
            )

        data["sent"] = [
            e for e in data["sent"]
            if not e.get("sent_at", "").startswith(target_ym)
        ]
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Archived {len(prev_entries)} events → {zip_path.name}")

    def cleanup_old_archives(self) -> None:
        if not self.archive_dir.exists():
            return

        today = self._today()
        for zip_file in self.archive_dir.glob("*.zip"):
            try:
                file_date = date(
                    int(zip_file.stem[:4]), int(zip_file.stem[5:7]), 1
                )
                months_diff = (
                    (today.year - file_date.year) * 12
                    + (today.month - file_date.month)
                )
                if months_diff > self.retention_months:
                    zip_file.unlink()
                    logger.info(f"Deleted old archive: {zip_file.name}")
            except (ValueError, IndexError):
                continue
