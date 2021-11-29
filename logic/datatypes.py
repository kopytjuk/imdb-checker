"""Dataclasses used across the backend."""

from typing import List, Optional
from enum import Enum
from dataclasses import dataclass, asdict
import datetime

from pydantic import BaseModel
import pandas as pd

class TaskInfo(BaseModel):
    task_id: str


class Reason(Enum):
    BUG = 1
    FEATURE = 2
    OTHER = 3


class UserMessage(BaseModel):
    """Feedback message from /send_feedback_message GET
    """
    timestamp: datetime.datetime
    name: str
    email: str
    reason: Reason
    message: str


class UserRequest(BaseModel):
    """Is received from the client. Start a celery job based on the method.
    """
    method: str  # one of "_imdb_watchlist", "imdb_top_250", "oscars_2021"
    location_code: str
    url: Optional[str]  # only used for '_imdb_watchlist'


@dataclass
class MediaElement:
    """Single unit of a movie/series. Usually an element in a list, e.g. "Top 250"
    """
    name: str
    year: int
    imdb_id: str


@dataclass
class ResultElement:
    """This object is returned by availability checker to the frontend.
    """
    name: str
    year: str
    availability: dict
    poster: str
    description: str
    num_available: int


class Results(BaseModel):
    """This object is returned by availability checker to the frontend.
    """
    result: List[ResultElement]


@dataclass
class MediaList:

    name: str
    elements: List[MediaElement]

    def __len__(self) -> int:
        return len(self.elements)

    def to_csv(self, path: str):
        df = self.to_dataframe()
        df.to_csv(path, index=False)

    def to_dataframe(self) -> pd.DataFrame:
        records = list()
        for elem in self.elements:
            records.append(asdict(elem))
        df = pd.DataFrame(records)
        return df

    @classmethod
    def from_csv(cls, name: str, path: str) -> "MediaList":

        df = pd.read_csv(path)

        elements = list()
        for _, row in df.iterrows():
            elements.append(MediaElement(row["name"], row["year"], row["imdb_id"]))

        return MediaList(name, elements)
