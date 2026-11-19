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

weather = pd.read_csv("data/raw/perth_temperature.csv", skiprows=3)
weather.columns = ["time", "temp_c"]
weather["time"] = pd.to_datetime(weather["time"])
weather = weather.set_index("time")

demand_hourly = df.resample("h").mean()

data = demand_hourly.join(weather, how="inner")


print("WEATHER")
print(weather.shape)
print(weather.head())

print("JOINED")
print(data.shape)
print(data.head())
print(data.isna().sum())

data.to_csv("data/processed/hourly.csv")
print("Saved!")

# print(df.shape)
# print("BREAK")
# print(df.head())
# print("BREAK")
# print(df.tail())
# print("BREAK")
# print("Duplicate times:", df.index.duplicated().sum())
