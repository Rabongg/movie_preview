import logging

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from crawlers.base_crawler import BaseCrawler
from crawlers.driver import get_driver
from models.event import Event

logger = logging.getLogger("movie_preview")

MEGABOX_URL = "https://megabox.co.kr/event/curtaincall"
BASE_URL = "https://megabox.co.kr"


class MegaboxCrawler(BaseCrawler):
    def _fetch_page(self) -> str:
        driver = get_driver()
        try:
            driver.get(MEGABOX_URL)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.event-list"))
            )
            return driver.page_source
        finally:
            driver.quit()

    def _parse(self, html: str) -> list[Event]:
        soup = BeautifulSoup(html, "html.parser")
        events = []

        for a_tag in soup.select("a.eventBtn"):
            data_no = a_tag.get("data-no", "")
            booking_url = f"{BASE_URL}/event/curtaincall?no={data_no}" if data_no else ""

            title_tag = a_tag.select_one(".tit")
            title = title_tag.get_text(strip=True) if title_tag else ""
            if not title:
                continue

            date_tag = a_tag.select_one(".date")
            date_str = date_tag.get_text(strip=True) if date_tag else ""

            events.append(Event(
                theater="Megabox",
                event_type=self._extract_event_type(title),
                title=title,
                date=date_str,
                location="",
                actors=[],
                booking_url=booking_url,
            ))
        return events

    def crawl(self) -> list[Event]:
        try:
            return self._parse(self._fetch_page())
        except Exception as e:
            logger.error(f"Megabox 크롤링 실패: {e}")
            return []
