import sys

sys.path.append(".")

from logic.imdb_utils import get_top_250

medialist = get_top_250()

df = medialist.to_dataframe()
print(df.head())

medialist.to_csv("imdb_top_250.csv")

