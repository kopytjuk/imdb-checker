import os

from notifiers import get_notifier
from .config import default_config

token = default_config.TELEGRAM_BOT_TOKEN
chat_id = default_config.TELEGRAM_CHAT_ID

notifier = get_notifier('telegram')


def send_notification(text: str):
    notifier.notify(message=text, token=token, chat_id=chat_id)
