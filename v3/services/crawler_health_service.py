import json
from datetime import datetime
from pathlib import Path


class CrawlerHealthService:
    def __init__(self, data_file: Path = Path("data/crawler_health.json")):
        self.data_file = data_file

    def _load(self) -> dict:
        if not self.data_file.exists():
            return {}
        with open(self.data_file, encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: dict) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def record_zero(self, crawler_name: str) -> int:
        data = self._load()
        entry = data.get(crawler_name, {"consecutive_zeros": 0})
        entry["consecutive_zeros"] += 1
        entry["last_updated"] = datetime.now().isoformat(timespec="seconds")
        data[crawler_name] = entry
        self._save(data)
        return entry["consecutive_zeros"]

    def record_success(self, crawler_name: str) -> None:
        data = self._load()
        data[crawler_name] = {"consecutive_zeros": 0, "last_updated": datetime.now().isoformat(timespec="seconds")}
        self._save(data)

    def get_consecutive_zeros(self, crawler_name: str) -> int:
        return self._load().get(crawler_name, {}).get("consecutive_zeros", 0)
