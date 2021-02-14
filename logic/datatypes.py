from typing import Dict, List, Optional
from dataclasses import dataclass

from pydantic import BaseModel

from .config import SUPPORTED_LOCATION_CODES


class UserRequest(BaseModel):

    method: str
    location_code: str
    url: Optional[str]


@dataclass
class MediaElement:
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

