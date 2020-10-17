import io

import requests
from bs4 import BeautifulSoup
import pandas as pd


def _get_pageId(url: str) -> str:

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    pageId = soup.find("meta", attrs={"property": "pageId"}).attrs["content"]

    return pageId


def _get_watchlist(pageId: str) -> pd.DataFrame:

    response = requests.get("https://www.imdb.com/list/{:s}/export".format(pageId))

    content = response.content

    content_stream = io.BytesIO(content)
    content_stream.seek(0)

    df = pd.read_csv(content_stream, sep=",", encoding="cp1252")
    return df


def get_watchlist(url: str) -> pd.DataFrame:
    return _get_watchlist(_get_pageId(url))
