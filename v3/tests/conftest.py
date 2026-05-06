import pytest

from models.event import Event


@pytest.fixture
def sample_event():
    return Event(
        theater="CGV",
        event_type="무대인사",
        title="어벤져스",
        date="2025-06-01",
        time="14:00",
        location="CGV 강남",
        actors=["배우1"],
        booking_url="https://example.com/book/1",
    )


@pytest.fixture
def sample_events():
    return [
        Event(
            theater="CGV", event_type="무대인사", title="어벤져스",
            date="2025-06-01", location="CGV 강남", actors=["배우1"],
        ),
        Event(
            theater="Megabox", event_type="시사회", title="인터스텔라",
            date="2025-06-02", location="메가박스 코엑스",
        ),
    ]
