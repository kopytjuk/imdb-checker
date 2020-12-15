import os

from notifiers import get_notifier

from .config import TELEGRAM_BOT_TOKEN as token
from .config import TELEGRAM_CHAT_ID as chat_id

notifier = get_notifier('telegram')


def send_notification(text: str):
    notifier.notify(message=text, token=token, chat_id=chat_id)
