import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor

from preprocess import preprocess_data

# Load dataset
df = pd.read_csv("data/student_data.csv")

# Preprocess data
X, y = preprocess_data(df, is_training=True)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

# Regression models (CORRECT)
models = {
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "KNN": KNeighborsRegressor(n_neighbors=7),
    "Random Forest": RandomForestRegressor(
        n_estimators=300,
        random_state=42
    )
}

best_model = None
best_score = float("inf")
best_model_name = ""

# Train & evaluate
for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print(f"{name} MAE: {mae:.2f} | R2 Score: {r2:.2f}")

    if mae < best_score:
        best_score = mae
        best_model = model
        best_model_name = name

# Save best model
joblib.dump(best_model, "models/student_model.pkl")

print("\nBest Model:", best_model_name)
print("Best MAE:", best_score)
print("Best model saved successfully!")
