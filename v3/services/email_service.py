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

        # 2열 table 레이아웃 (이메일 클라이언트 호환)
        rows = ""
        for i in range(0, len(events), 2):
            left = self._render_event(events[i])
            right = self._render_event(events[i + 1]) if i + 1 < len(events) else "<td></td>"
            rows += f"<tr><td style='padding:4px;vertical-align:top;width:50%;'>{left}</td><td style='padding:4px;vertical-align:top;width:50%;'>{right}</td></tr>"

        return f"""
      <div style="margin-bottom:24px;">
        <div style="font-size:13px; font-weight:bold; color:{color}; border-left:3px solid {color}; padding-left:8px; margin-bottom:10px; letter-spacing:0.5px;">🎫 {theater_escaped}</div>
        <table width="100%" cellpadding="0" cellspacing="0" border="0">{rows}</table>
      </div>"""

    def _render_event(self, event: Event) -> str:
        badge_color = {"무대인사": "#c0392b", "커튼콜": "#c0392b", "시사회": "#1a6fa8"}.get(event.event_type, "#7f8c8d")
        title = html_module.escape(event.title)
        date = html_module.escape(event.date)
        time_part = f" {html_module.escape(event.time)}" if event.time else ""
        location_part = f" · {html_module.escape(event.location)}" if event.location else ""

        actors_html = ""
        if event.actors:
            escaped_actors = ", ".join(html_module.escape(a) for a in event.actors)
            actors_html = f'<div style="font-size:12px;color:#666;margin-top:6px;">👥 {escaped_actors}</div>'

        booking_html = ""
        if event.booking_url:
            booking_html = f'<a href="{html_module.escape(event.booking_url)}" style="display:inline-block;margin-top:10px;padding:6px 14px;background:#1a1a2e;color:white;text-decoration:none;border-radius:6px;font-size:12px;font-weight:bold;">예매하기</a>'

        return f"""<div style="background:white;border-radius:10px;padding:14px;box-shadow:0 1px 6px rgba(0,0,0,0.07);">
          <span style="display:inline-block;padding:2px 10px;border-radius:20px;font-size:11px;color:white;font-weight:bold;background:{badge_color};margin-bottom:8px;">{html_module.escape(event.event_type)}</span>
          <div style="font-size:13px;font-weight:bold;color:#1a1a2e;line-height:1.4;margin-bottom:6px;">{title}</div>
          <div style="font-size:12px;color:#666;margin-bottom:2px;">📅 {date}{time_part}</div>
          {actors_html}
          {booking_html}
        </div>"""
