import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# 1. Load data
df = pd.read_csv("../datasets/raw/Crop_recommendation.csv")

# 2. Split features (X) and target (y)
X = df.drop("label", axis=1)
y = df["label"]

# 3. Train/test split (80/20), stratify keeps class balance equal in both sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training samples: {len(X_train)}, Testing samples: {len(X_test)}")

# 4. Train multiple models and compare
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
    print(classification_report(y_test, predictions))


best_name = max(results, key=lambda name: results[name][1])
best_model, best_accuracy = results[best_name]
print(f"\n🏆 Best model: {best_name} ({best_accuracy * 100:.2f}% accuracy)")


os.makedirs("../models", exist_ok=True)
joblib.dump(best_model, "../models/crop_recommendation_model.pkl")
print(f"✅ Saved to ml/models/crop_recommendation_model.pkl")