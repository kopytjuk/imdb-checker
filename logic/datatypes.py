from typing import Dict, List

from pydantic import BaseModel


class ResultElement(BaseModel):
    name: str
    year: str
    availability: dict
    poster: str
    description: str
    num_available: int


# is returned to the frontend as json object
class Results(BaseModel):
    result: List[ResultElement]