import os

# OMDB
OMDB_API_KEY = os.environ.get("OMDB_API_KEY")

# Telegram notification
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = int(os.environ.get("TELEGRAM_CHAT_ID"))

# Celery
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'amqp://localhost')
CELERY_RESULT_URL = os.environ.get(
    'CELERY_RESULT_URL', 'db+sqlite:///results.sqlite')
CELERY_BROKER_POOL_LIMIT = os.environ.get('CELERY_BROKER_POOL_LIMIT', '10')


SUPPORTED_LOCATION_CODES = ["de_DE", "de_AT", "de_CH", "en_GB", "fr_FR",
                            "ru_RU", "en_US", "en_NL"]
