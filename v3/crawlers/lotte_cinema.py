import logging

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from crawlers.base_crawler import BaseCrawler
from crawlers.driver import get_driver
from models.event import Event

logger = logging.getLogger("movie_preview")

LOTTE_URL = "https://www.lottecinema.co.kr/NLCHS/Event/DetailList?code=40"
BASE_URL = "https://www.lottecinema.co.kr"


class LotteCinemaCrawler(BaseCrawler):
    def _fetch_page(self) -> str:
        driver = get_driver()
        try:
            driver.get(LOTTE_URL)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "img_lst_wrap"))
            )
            return driver.page_source
        finally:
            driver.quit()

    def _parse(self, html: str) -> list[Event]:
        soup = BeautifulSoup(html, "html.parser")
        events = []

        for li in soup.select(".img_lst_wrap li"):
            img_tag = li.find("img")
            title = (img_tag.get("alt") or "").strip() if img_tag else ""
            if not title:
                continue

            date_tag = li.select_one("div.itm_date")
            date_str = date_tag.get_text(strip=True) if date_tag else ""

            events.append(Event(
                theater="LotteCinema",
                event_type=self._extract_event_type(title),
                title=title,
                date=date_str,
                location="",
                actors=[],
                booking_url="",
            ))
        return events

    def crawl(self) -> list[Event]:
        try:
            return self._parse(self._fetch_page())
        except Exception as e:
            logger.error(f"Lotte Cinema 크롤링 실패: {e}")
            return []
