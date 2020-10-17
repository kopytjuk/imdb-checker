import pytest

from imdb import _get_pageId, _get_watchlist

def test_get_pageId():

    url = "https://www.imdb.com/user/ur58171394/watchlist"

    pageId = _get_pageId(url)

    assert pageId == "ls073803218"


def test_get_watchlist():

    pageId = "ls073803218"

    df = _get_watchlist(pageId)

    assert len(df) > 1
    assert "Title" in df.columns