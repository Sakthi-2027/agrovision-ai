import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os


df = pd.read_csv("../datasets/raw/Fertilizer Prediction.csv")
df = df.rename(columns={"Temparature": "temperature", "Humidity ": "humidity"})


soil_encoder = LabelEncoder()
crop_encoder = LabelEncoder()

df["Soil_Type_Encoded"] = soil_encoder.fit_transform(df["Soil Type"])
df["Crop_Type_Encoded"] = crop_encoder.fit_transform(df["Crop Type"])

feature_columns = ["temperature", "humidity", "Moisture", "Soil_Type_Encoded", "Crop_Type_Encoded", "Nitrogen", "Potassium", "Phosphorous"]
X = df[feature_columns]
y = df["Fertilizer Name"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")


models = {
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42)
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    results[name] = (model, accuracy)
    print(f"\n{'=' * 50}")
    print(f"{name}: {accuracy * 100:.2f}% accuracy")
    print(f"{'=' * 50}")
    print(classification_report(y_test, predictions, zero_division=0))


best_name = max(results, key=lambda name: results[name][1])
best_model, best_accuracy = results[best_name]
print(f"\n🏆 Best model: {best_name} ({best_accuracy * 100:.2f}% accuracy)")


os.makedirs("../models", exist_ok=True)
joblib.dump({
    "model": best_model,
    "soil_encoder": soil_encoder,
    "crop_encoder": crop_encoder,
    "feature_columns": feature_columns
}, "../models/fertilizer_recommendation_model.pkl")

print("✅ Saved to ml/models/fertilizer_recommendation_model.pkl")
print(f"\nSoil types the model knows: {list(soil_encoder.classes_)}")
print(f"Crop types the model knows: {list(crop_encoder.classes_)}")