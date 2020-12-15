import abc
from collections import namedtuple
from typing import List


WatchlistElement = namedtuple("WatchlistElement", ["name", "year", "imdb_id"])


class BaseWatchlistGetter(abc.ABC):
    @abc.abstractmethod
    def get_media_from_url(self, url: str) -> List[WatchlistElement]:
        pass


class WatchlistError(Exception):
    """Base class for other exceptions"""
    def __init__(self, url: str):
        message = "Watchlist '%s' is not supported."
        super().__init__(message)
