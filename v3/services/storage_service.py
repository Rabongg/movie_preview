import json
from datetime import datetime
from pathlib import Path

from models.event import Event


class StorageService:
    def __init__(self, data_file: Path = Path("data/sent_events.json")):
        self.data_file = data_file

    def _load_raw(self) -> dict:
        if not self.data_file.exists():
            return {"sent": []}
        with open(self.data_file, encoding="utf-8") as f:
            return json.load(f)

    def load_sent_ids(self) -> set[str]:
        return {item["id"] for item in self._load_raw().get("sent", [])}

    def filter_new(self, events: list[Event]) -> list[Event]:
        sent_ids = self.load_sent_ids()
        return [e for e in events if e.event_id not in sent_ids]

    def save(self, events: list[Event]) -> None:
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        data = self._load_raw()
        now = datetime.now().isoformat(timespec="seconds")
        for event in events:
            data["sent"].append({
                "id": event.event_id,
                "title": event.title,
                "theater": event.theater,
                "date": event.date,
                "event_type": event.event_type,
                "sent_at": now,
            })
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
