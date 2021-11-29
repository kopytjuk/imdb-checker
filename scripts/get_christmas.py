import sys

sys.path.append(".")

from logic.main import get_media_from_watchlist_url


medialist = get_media_from_watchlist_url("https://www.imdb.com/list/ls000096828/")

medialist.to_csv("medialists/christmas.csv")
