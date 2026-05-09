import html as html_module
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from models.event import Event

logger = logging.getLogger("movie_preview")

_BADGE_CLASS = {
    "무대인사": "badge-stage",
    "시사회": "badge-preview",
    "커튼콜": "badge-stage",
}
_THEATER_COLOR = {
    "Megabox": "#3f51b5",
    "LotteCinema": "#e65100",
    "CGV": "#e74c3c",
}
_TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "email_template.html"


class EmailService:
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 465

    def __init__(
        self,
        sender_email: str,
        sender_key: str,
        receiver_emails: list[str],
    ):
        self.sender_email = sender_email
        self.sender_key = sender_key
        self.receiver_emails = receiver_emails

    def send(self, events: list[Event]) -> bool:
        if not events:
            logger.info("발송할 새 이벤트가 없습니다.")
            return False

        html = self._build_html(events)
        msg = MIMEMultipart("alternative")
        msg["From"] = self.sender_email
        msg["To"] = ", ".join(self.receiver_emails)
        msg["Subject"] = f"[영화 알림] 무대인사/시사회 {len(events)}건"
        msg.attach(MIMEText(html, "html", "utf-8"))

        try:
            with smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_PORT) as server:
                server.login(self.sender_email, self.sender_key)
                server.sendmail(self.sender_email, self.receiver_emails, msg.as_string())
            logger.info(f"이메일 발송 완료: {len(events)}건 → {len(self.receiver_emails)}명")
            return True
        except Exception as e:
            logger.error(f"이메일 발송 실패: {e}")
            return False

    def _build_html(self, events: list[Event]) -> str:
        template = _TEMPLATE_PATH.read_text(encoding="utf-8")

        groups: dict[str, list[Event]] = {}
        for event in events:
            groups.setdefault(event.theater, []).append(event)

        groups_html = "".join(self._render_group(theater, evts) for theater, evts in groups.items())

        return (
            template
            .replace("{{events}}", groups_html)
            .replace("{{count}}", str(len(events)))
        )

    def _render_group(self, theater: str, events: list[Event]) -> str:
        color = _THEATER_COLOR.get(theater, "#555555")
        theater_escaped = html_module.escape(theater)
        cards_html = "".join(self._render_event(e) for e in events)
        return f"""
      <div class="theater-group">
        <div class="theater-title" style="border-left-color:{color}; color:{color};">🎫 {theater_escaped}</div>
        <div class="grid">{cards_html}</div>
      </div>"""

    def _render_event(self, event: Event) -> str:
        badge_class = _BADGE_CLASS.get(event.event_type, "badge-other")
        title = html_module.escape(event.title)
        date = html_module.escape(event.date)
        time_part = f" {html_module.escape(event.time)}" if event.time else ""
        location_part = f" · {html_module.escape(event.location)}" if event.location else ""

        actors_html = ""
        if event.actors:
            escaped_actors = ", ".join(html_module.escape(a) for a in event.actors)
            actors_html = f'<p class="actors">👥 {escaped_actors}</p>'

        booking_html = ""
        if event.booking_url:
            booking_html = f'<a class="btn" href="{html_module.escape(event.booking_url)}">예매하기</a>'

        return f"""
        <div class="card">
          <span class="badge {badge_class}">{event.event_type}</span>
          <p class="title">{title}</p>
          <p class="info">📅 {date}{time_part}</p>
          <p class="info">📍 {html_module.escape(event.theater)}{location_part}</p>
          {actors_html}
          {booking_html}
        </div>"""
