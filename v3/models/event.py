from dataclasses import dataclass, field
import hashlib


@dataclass
class Event:
    theater: str
    event_type: str
    title: str
    date: str
    time: str = ""
    location: str = ""
    actors: list[str] = field(default_factory=list)
    booking_url: str = ""

    @property
    def event_id(self) -> str:
        key = f"{self.theater}_{self.title}_{self.date}_{self.event_type}"
        return hashlib.md5(key.encode()).hexdigest()
