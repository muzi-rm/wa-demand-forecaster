import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("data/processed/hourly.csv", index_col="time", parse_dates=True)

print(data.head())
      
daily = data["demand_mw"].resample("D").mean()

daily.plot(figsize=(12,4))
plt.title("Average daily electrical demand in WA from 2019 to 2023")
plt.ylabel("Demand (MW)")
plt.show()

plt.figure(figsize=(6,6))
plt.scatter(data["temp_c"], data["demand_mw"], s=1, alpha=0.3, c=data.index.hour, cmap="twilight")
plt.colorbar(label = "Hour of the day")
plt.ylabel("Demand (MW)")
plt.xlabel("Temperature (°C)")
plt.title("Hourly Demand vs Temperature")
plt.show()