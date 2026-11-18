import pandas as pd

years = [2019, 2020, 2021, 2022, 2023]
frames = []

for year in years:
    df = pd.read_csv(f"data/raw/operational-demand-{year}.csv")
    frames.append(df)

df = pd.concat(frames)

df = df[["Trading Interval", "Operational Demand (MW)"]]
df.columns = ["time", "demand_mw"]

df["time"] = pd.to_datetime(df["time"])

df = df.sort_values("time").set_index("time")

print(df.shape)
print("BREAK")
print(df.head())
print("BREAK")
print(df.tail())
print("BREAK")
print("Duplicate times:", df.index.duplicated().sum())
