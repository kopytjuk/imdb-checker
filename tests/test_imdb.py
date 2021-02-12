from collections import namedtuple

import pytest

from logic.imdb_provider import _get_pageId, _get_watchlist


TestCase = namedtuple("TestCase", ["url", "pageId"])

test_cases = [
    TestCase("https://www.imdb.com/user/ur58171394/watchlist", "ls073803218"),
    TestCase("https://www.imdb.com/user/ur85031360/watchlist", "ls021228741"),
]

@pytest.mark.parametrize("url,pageId", [(tc.url, tc.pageId) for tc in test_cases])
def test_get_pageId(url: str, pageId: str):

    pageId_ = _get_pageId(url)

    assert pageId == pageId_


@pytest.mark.parametrize("pageId", [tc.pageId for tc in test_cases])
def test_get_watchlist(pageId):

    df = _get_watchlist(pageId)

    assert len(df) > 1
    assert "Title" in df.columns
