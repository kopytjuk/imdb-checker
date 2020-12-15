import io
from typing import List
import math

import requests
from bs4 import BeautifulSoup
import pandas as pd

from .watchlist_provider import BaseWatchlistGetter, WatchlistElement, WatchlistError


class IMDbWatchlistGetter(BaseWatchlistGetter):

    def get_media_from_url(self, url: str) -> List[WatchlistElement]:

        try:
            df = _get_watchlist(_get_pageId(url))
        except:
            raise WatchlistError(url)

        watchlist_elements = list()

        for _, element in df.iterrows():
            year = None
            if not math.isnan(element["Year"]):
                year = int(element["Year"])
            watchlist_elements.append(WatchlistElement(element["Title"], year, element["Const"]))
        
        return watchlist_elements


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
    df["IMDB_ID"] = df["URL"].map(get_imdb_id_from_url)
    return df


def get_imdb_id_from_url(url: str) -> str:
    return url.split("/")[-2]


def get_watchlist(url: str) -> pd.DataFrame:
    return _get_watchlist(_get_pageId(url))

