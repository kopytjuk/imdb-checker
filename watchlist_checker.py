import click
import pandas as pd
from tabulate import tabulate

from werstreamtes import availability_table
from imdb import get_watchlist

@click.command()
@click.argument("url", type=click.STRING)
def main(url: str):

    movie_df = get_watchlist(url)

    print("Looking for %d movies." % len(movie_df))

    movies = movie_df["Title"].tolist()

    avail_df = availability_table(movies)

    print(tabulate(avail_df, headers='keys', tablefmt='psql'))


if __name__ == "__main__":
    main()