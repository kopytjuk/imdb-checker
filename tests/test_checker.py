import pytest

from logic.watchlist_checker import check
from logic.watchlist_provider import WatchlistError


WATCHLISTS = [
    "https://www.imdb.com/user/ur58171394/watchlist",
    "https://www.imdb.com/user/ur5205364/watchlist",  # large
]

@pytest.mark.parametrize("location_code", ["de_DE", "en_GB", "en_US"])
@pytest.mark.parametrize("url", WATCHLISTS)
def test_main_logic(url: str, location_code: str):

    results = check(url, location_code, None)

    assert len(results) > 0
