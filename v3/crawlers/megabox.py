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
                EC.presence_of_element_located((By.CLASS_NAME, "event-list"))
            )
            return driver.page_source
        finally:
            driver.quit()

    def _parse(self, html: str) -> list[Event]:
        soup = BeautifulSoup(html, "html.parser")
        events = []

        for li in soup.select("ul.event-list li"):
            a_tag = li.find("a")
            href = (a_tag.get("href") or "") if a_tag else ""
            booking_url = (BASE_URL + href) if href and not href.startswith("http") else href

            title_tag = li.select_one(".tit")
            title = title_tag.get_text(strip=True) if title_tag else ""
            if not title:
                continue

            date_tag = li.select_one(".date")
            date_str = date_tag.get_text(strip=True) if date_tag else ""

            actor_tag = li.select_one(".actor")
            actors_raw = actor_tag.get_text(strip=True) if actor_tag else ""
            actors = [a.strip() for a in actors_raw.split(",") if a.strip()]

            events.append(Event(
                theater="Megabox",
                event_type=self._extract_event_type(title),
                title=title,
                date=date_str,
                location="",
                actors=actors,
                booking_url=booking_url,
            ))
        return events

    def crawl(self) -> list[Event]:
        try:
            return self._parse(self._fetch_page())
        except Exception as e:
            logger.error(f"Megabox 크롤링 실패: {e}")
            return []
