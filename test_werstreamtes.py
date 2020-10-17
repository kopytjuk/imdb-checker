import pytest
from typing import Union
import pandas as pd

from werstreamtes import get_movie_id, check_availability, availability_table


@pytest.mark.parametrize("movie,expected_id", [("John Wick 2", "776859"), ("BlaBlubBlib", None)])
def test_get_movie_id(movie: str, expected_id: Union[str, None]):

    movie_id = get_movie_id(movie)
    assert movie_id == expected_id


def test_check_availability():
    avail = check_availability("776859")
    assert avail["Netflix"]


def test_availability_table():

    movies = ["John Wick", "John Wick 2"]

    avail_df = availability_table(movies)

    assert isinstance(avail_df, pd.DataFrame)
    assert len(avail_df) == 2
