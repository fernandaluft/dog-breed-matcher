import pandas as pd

df = pd.read_csv("data/dog_breeds_api_raw.json")

print(df["weight_metric"].str.split("-", expand=True)[0])

print(df.head(1))