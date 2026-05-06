import logging

import requests

from crawlers.base_crawler import BaseCrawler
from models.event import Event

logger = logging.getLogger("movie_preview")

# TODO: evntCtgryMclsCd 값을 실제 API에서 시사회(GV) 코드 포함하도록 확인 필요
CGV_URL = (
    "https://event-mobile.cgv.co.kr/evt/evt/evt/searchEvtListForPage"
    "?coCd=A420&evntCtgryLclsCd=03&evntCtgryMclsCd=033"
    "&sscnsChoiYn=N&expnYn=N&expoChnlCd=01&startRow=0&listCount=50"
)


class CGVCrawler(BaseCrawler):
    def __init__(self, url: str = CGV_URL):
        self.url = url

    def _fetch_data(self) -> dict:
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        return response.json()

    def _parse(self, data: dict) -> list[Event]:
        events = []
        for item in data.get("data", {}).get("list", []):
            title = item.get("evntNm", "")
            if not title:
                continue

            start = item.get("evntStartDt", "").split()[0]
            end = item.get("evntEndDt", "").split()[0]
            date_str = f"{start} ~ {end}" if start != end else start

            # TODO: 실제 CGV API 응답의 필드명 검증 필요 (prtcpntNm, cinemaName, mblLnkUrl)
            actors_raw = item.get("prtcpntNm", "") or ""
            actors = [a.strip() for a in actors_raw.split(",") if a.strip()]

            evnt_no = item.get("evntNo", "")
            booking_url = item.get("mblLnkUrl", "") or (
                f"https://m.cgv.co.kr/event/detail?evntNo={evnt_no}" if evnt_no else ""
            )

            events.append(Event(
                theater="CGV",
                event_type=self._extract_event_type(title),
                title=title,
                date=date_str,
                location=item.get("cinemaName", "") or "",
                actors=actors,
                booking_url=booking_url,
            ))
        return events

    def crawl(self) -> list[Event]:
        try:
            return self._parse(self._fetch_data())
        except Exception as e:
            logger.error(f"CGV 크롤링 실패: {e}")
            return []
