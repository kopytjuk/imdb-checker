import pytest

from logic.main import check_imdb_user_watchlist, check_medialist
from logic.config import default_config


WATCHLISTS = [
    "https://www.imdb.com/user/ur58171394/watchlist",
    "https://www.imdb.com/user/ur5205364/watchlist",  # large
    "https://www.imdb.com/user/ur85031360/watchlist",
]

LOCATIONS = [
    "de_DE",
    "en_GB",
    "en_US"
]

default_config.request_cooldown_time = 0.2


@pytest.mark.parametrize("location_code", LOCATIONS)
@pytest.mark.parametrize("url", WATCHLISTS)
def test_imdb_user_watchlist(url: str, location_code: str):

    results = check_imdb_user_watchlist(url, location_code, None)

    assert len(results) > 0


MEDIALISTS = [
    "imdb_top_250",
    "christmas_list"
]


@pytest.mark.parametrize("medialist", MEDIALISTS)
@pytest.mark.parametrize("location_code", LOCATIONS)
def test_check_medialist(medialist: str, location_code: str):

    results = check_medialist(medialist, location_code)
    assert len(results) > 10
