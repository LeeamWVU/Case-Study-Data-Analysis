import pandas as pd

for y in range(2015, 2020):
    print(y, list(pd.read_csv(f"data/{y}.csv").columns))
