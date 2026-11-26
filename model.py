import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
import matplotlib.pyplot as plt

data = pd.read_csv("data/processed/hourly.csv", index_col="time", parse_dates=True)

data["yesterday"] = data["demand_mw"].shift(24)
data["last_week"] = data["demand_mw"].shift(168)
data["hour"] = data.index.hour
data["is_weekend"] = data.index.day_of_week >= 5
data["month"] = data.index.month

data = data.dropna()

train = data[data.index < "2023-01-01"]
test = data[data.index >= "2023-01-01"]

features = ["yesterday", "hour", "is_weekend", "temp_c", "month", "last_week"]

X_train = train[features]
y_train = train["demand_mw"]
X_test = test[features]
y_test = test["demand_mw"]

print(X_train.head())

error_yesterday = (abs(test["demand_mw"] - test["yesterday"]) / test["demand_mw"]).mean()*100
error_last_week = (abs(test["demand_mw"] - test["last_week"]) / test["demand_mw"]).mean()*100

print("Train:", train.index.min(), "to", train.index.max(), len(train), "rows")
print("Test: ", test.index.min(), "to", test.index.max(), len(test), "rows")


print(f"Same as yesterday: {error_yesterday:.1f}% average error")
print(f"Same as last week: {error_last_week:.1f}% average error")

model = HistGradientBoostingRegressor(random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

error_model = (abs(y_test - predictions)/y_test).mean()*100

print(f"Model:             {error_model:.1f}% average error")

results = test[["demand_mw"]].copy()
results["forecast"] = predictions
results["error_pct"] = abs(results["demand_mw"] - results["forecast"])/results["demand_mw"] * 100

print(results.head())

week = results.loc["2023-02-06":"2023-02-12"]
week[["demand_mw", "forecast"]].plot(figsize=(12,4))
plt.title("Forecast vs actual demand, 6–12 Feb 2023")
plt.ylabel("Demand (MW)")
plt.show()

results["hour"] = results.index.hour
results["is_weekend"] = results.index.day_of_week >= 5

print("Average error by hour:")
print(results.groupby("hour")["error_pct"].mean().round(1))

print("Average error, weekday vs weekend:")
print(results.groupby("is_weekend")["error_pct"].mean().round(1))
