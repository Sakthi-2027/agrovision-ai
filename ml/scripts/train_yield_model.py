import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import joblib
import os
import numpy as np


df = pd.read_csv("../datasets/raw/yield_df.csv")
df = df.drop(columns=["Unnamed: 0"])  # leftover index column from the CSV export, not useful


area_encoder = LabelEncoder()
item_encoder = LabelEncoder()

df["Area_Encoded"] = area_encoder.fit_transform(df["Area"])
df["Item_Encoded"] = item_encoder.fit_transform(df["Item"])


feature_columns = ["Area_Encoded", "Item_Encoded", "Year", "average_rain_fall_mm_per_year", "pesticides_tonnes", "avg_temp"]
X = df[feature_columns]
y = df["hg/ha_yield"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")


models = {
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Linear Regression": LinearRegression()
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    r2 = r2_score(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    mae = mean_absolute_error(y_test, predictions)

    results[name] = (model, r2)
    print(f"\n{'=' * 50}")
    print(f"{name}")
    print(f"{'=' * 50}")
    print(f"R² Score: {r2:.4f}")
    print(f"RMSE: {rmse:.2f} hg/ha")
    print(f"MAE: {mae:.2f} hg/ha")


best_name = max(results, key=lambda name: results[name][1])
best_model, best_r2 = results[best_name]
print(f"\n🏆 Best model: {best_name} (R² = {best_r2:.4f})")


os.makedirs("../models", exist_ok=True)
joblib.dump({
    "model": best_model,
    "area_encoder": area_encoder,
    "item_encoder": item_encoder,
    "feature_columns": feature_columns
}, "../models/yield_prediction_model.pkl")

print("✅ Saved to ml/models/yield_prediction_model.pkl")