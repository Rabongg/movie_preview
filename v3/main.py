import logging

from config.logger import setup_logger
from config.settings import RECEIVER_EMAILS, SENDER_EMAIL, SENDER_KEY
from crawlers.lotte_cinema import LotteCinemaCrawler
from crawlers.megabox import MegaboxCrawler
from models.event import Event
from services.archive_service import ArchiveService
from services.crawler_health_service import CrawlerHealthService
from services.email_service import EmailService
from services.storage_service import StorageService

ZERO_ALERT_THRESHOLD = 5


def main() -> None:
    logger = setup_logger()
    logger.info("=" * 40)
    logger.info("Movie Preview Alarm 시작")

    ArchiveService().run()

    crawlers = [MegaboxCrawler(), LotteCinemaCrawler()]
    all_events: list[Event] = []
    health = CrawlerHealthService()
    email_service = EmailService(SENDER_EMAIL, SENDER_KEY, RECEIVER_EMAILS)

    for crawler in crawlers:
        name = crawler.__class__.__name__
        events = crawler.crawl()
        logger.info(f"{name}: {len(events)}건 수집")
        if events:
            health.record_success(name)
            all_events.extend(events)
        else:
            count = health.record_zero(name)
            if count >= ZERO_ALERT_THRESHOLD:
                logger.warning(f"{name} {count}회 연속 0건 — 알림 발송")
                email_service.send_alert(name, count)

    logger.info(f"전체 수집: {len(all_events)}건")

    storage = StorageService()
    new_events = storage.filter_new(all_events)
    logger.info(f"신규 이벤트: {len(new_events)}건")

    if not new_events:
        logger.info("발송할 새 이벤트 없음. 종료.")
        return

    if email_service.send(new_events):
        storage.save(new_events)
        logger.info(f"저장 완료: {len(new_events)}건")

    logger.info("Movie Preview Alarm 완료")
    logger.info("=" * 40)


if __name__ == "__main__":
    main()
