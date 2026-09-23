import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import settings

logger = logging.getLogger(__name__)


def send_email(to: str, subject: str, body: str) -> bool:
    """Kirim email via SMTP. Return False kalau SMTP belum dikonfigurasi."""
    if not settings.smtp_enabled:
        logger.info("SMTP tidak dikonfigurasi - email tidak terkirim: %s", subject)
        return False

    msg = MIMEMultipart()
    msg["From"] = settings.smtp_user
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password_decoded)
            server.send_message(msg)
        logger.info("Email terkirim ke %s: %s", to, subject)
        return True
    except Exception as exc:  # noqa: BLE001
        logger.warning("Gagal kirim email ke %s: %s", to, exc)
        return False