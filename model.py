import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

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