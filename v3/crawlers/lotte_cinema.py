import logging

import requests

from crawlers.base_crawler import BaseCrawler
from models.event import Event

logger = logging.getLogger("movie_preview")

LOTTE_API = "https://www.lottecinema.co.kr/LCWS/Event/EventData.aspx"
LOTTE_DETAIL_URL = "https://www.lottecinema.co.kr/NLCHS/Event/EventTemplateStageGreeting"
PARAM = {
    "MethodName": "GetEventLists",
    "channelType": "HO",
    "osType": "W",
    "osVersion": "Mozilla/5.0",
    "EventClassificationCode": "40",
    "SearchText": "",
    "CinemaID": "",
    "PageNo": 1,
    "PageSize": 30,
    "MemberNo": "0",
}


class LotteCinemaCrawler(BaseCrawler):
    def _fetch_data(self) -> list[dict]:
        import json
        response = requests.post(
            LOTTE_API,
            files={"paramList": (None, json.dumps(PARAM))},
            headers={"Referer": "https://www.lottecinema.co.kr/NLCHS/Event/DetailList?code=40"},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("IsOK") != "true":
            raise ValueError(f"Lotte API 오류: {data.get('ResultMessage')}")
        return data.get("Items", [])

    def _parse(self, items: list[dict]) -> list[Event]:
        events = []
        for item in items:
            title = item.get("EventName", "").strip()
            if not title:
                continue

            event_type = item.get("EventTypeName", "")
            if not event_type:
                event_type = self._extract_event_type(title)

            start = item.get("ProgressStartDate", "")
            end = item.get("ProgressEndDate", "")
            date_str = f"{start} ~ {end}" if start != end else start

            event_id = item.get("EventID", "")
            booking_url = f"{LOTTE_DETAIL_URL}?eventId={event_id}" if event_id else ""

            events.append(Event(
                theater="LotteCinema",
                event_type=event_type,
                title=title,
                date=date_str,
                actors=[],
                booking_url=booking_url,
            ))
        return events

    def crawl(self) -> list[Event]:
        try:
            return self._parse(self._fetch_data())
        except Exception as e:
            logger.error(f"Lotte Cinema 크롤링 실패: {e}")
            return []
