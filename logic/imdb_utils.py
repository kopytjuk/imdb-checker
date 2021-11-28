import io
from typing import List, Union
import math

import requests
from bs4 import BeautifulSoup
import pandas as pd
import imdb

from .datatypes import MediaElement, MediaList


class WatchlistError(Exception):
    """Base class for other exceptions"""
    def __init__(self, url: str):
        message = "Watchlist '%s' is not supported." % url
        super().__init__(message)


ia = imdb.IMDb()


def get_media_from_watchlist_url(url: str) -> MediaList:

    try:
        df = _get_watchlist(_get_pageId(url))
    except Exception:
        raise ValueError("Watchlist URL is not public or not valid.")

    watchlist_elements = list()

    for _, element in df.iterrows():
        year = None
        if not math.isnan(element["Year"]):
            year = int(element["Year"])
        watchlist_elements.append(MediaElement(element["Title"], year, element["Const"]))

    media_list = MediaList("userlist", watchlist_elements)

    return media_list


def _get_pageId(url: str) -> str:

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    pageId = soup.find("meta", attrs={"property": "pageId"}).attrs["content"]

    return pageId


def _get_watchlist(pageId: str) -> Union[pd.DataFrame, None]:

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


def get_top_250() -> MediaList:
    top_movies = ia.get_top250_movies()

    elems = [MediaElement(mov["title"], mov["year"], "tt%s" % mov.getID())
           for mov in top_movies]
    return MediaList("IMDb Top 250", elems)
