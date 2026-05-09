from abc import ABC, abstractmethod

from models.event import Event


class BaseCrawler(ABC):
    @abstractmethod
    def crawl(self) -> list[Event]:
        """크롤링 결과를 Event 리스트로 반환. 실패 시 빈 리스트."""
        pass

    @staticmethod
    def _extract_event_type(title: str) -> str:
        if "무대인사" in title:
            return "무대인사"
        if "시사" in title:
            return "시사회"
        if "커튼콜" in title:
            return "커튼콜"
        return "기타"
