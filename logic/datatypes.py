"""Dataclasses used across the backend."""

from typing import List, Optional
from enum import Enum
from dataclasses import dataclass
import datetime

from pydantic import BaseModel


class TaskInfo(BaseModel):
    task_id: str


class Reason(Enum):
    BUG = 1
    FEATURE = 2
    OTHER = 3


class UserMessage(BaseModel):
    timestamp: datetime.datetime
    name: str
    email: str
    reason: Reason
    message: str


class UserRequest(BaseModel):
    method: str
    location_code: str
    url: Optional[str]


@dataclass
class MediaElement:
    """Single unit of a movie/series. Usually an element in a list, e.g. "Top 250"
    """
    name: str
    year: int
    imdb_id: str


@dataclass
class ResultElement:
    name: str
    year: str
    availability: dict
    poster: str
    description: str
    num_available: int


# is returned to the frontend as json object
class Results(BaseModel):
    result: List[ResultElement]
