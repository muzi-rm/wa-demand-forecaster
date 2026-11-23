import pandas as pd

data = pd.read_csv("data/processed/hourly.csv", index_col="time", parse_dates=True)

data["yesterday"] = data["demand_mw"].shift(24)
data["last_week"] = data["demand_mw"].shift(168)

train = data[data.index < "2023-01-01"]
test = data[data.index >= "2023-01-01"]

error_yesterday = (abs(test["demand_mw"] - test["yesterday"]) / test["demand_mw"]).mean()*100
error_last_week = (abs(test["demand_mw"] - test["last_week"]) / test["demand_mw"]).mean()*100

print("Train:", train.index.min(), "to", train.index.max(), len(train), "rows")
print("Test: ", test.index.min(), "to", test.index.max(), len(test), "rows")


print(f"Same as yesterday: {error_yesterday:.1f}% average error")
print(f"Same as last week: {error_last_week:.1f}% average error")