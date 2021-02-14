from joblib import Memory
from pydantic import (
    BaseSettings,
    Field,
)


class AppSettings(BaseSettings):

    OMDB_API_KEY: str = Field(..., env='OMDB_API_KEY')

    # Telegram
    TELEGRAM_BOT_TOKEN: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID: int = Field(..., env='TELEGRAM_CHAT_ID')

    # Celery
    CELERY_BROKER_URL: str = Field('amqp://localhost', env='CELERY_BROKER_URL')
    CELERY_RESULT_URL: str = Field('db+sqlite:///results.sqlite',
                                   env='CELERY_RESULT_URL')
    CELERY_BROKER_POOL_LIMIT: int = Field(10, env='CELERY_BROKER_POOL_LIMIT')

    # Internals
    request_cooldown_time: float = Field(0.1, env='REQUEST_COOLDOWN_TIME')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


default_config = AppSettings()

SUPPORTED_LOCATION_CODES = ["de_DE", "de_AT", "de_CH", "en_GB", "fr_FR",
                            "ru_RU", "en_US", "en_NL"]

# 100MB cache
memory = Memory(".cache", verbose=0, bytes_limit=1024*1024*100)
