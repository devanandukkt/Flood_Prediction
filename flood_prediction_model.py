import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load Dataset
df = pd.read_csv("FloodDataset.csv")

# Features
features = [
    "Max_Temp",
    "Min_Temp",
    "Rainfall",
    "Relative_Humidity",
    "Wind_Speed",
]

X = df[features]

# Target Column Cleaning
y = df["Flood?"]

# Data preprocessing
y = y.replace({
    "Yes": 1,
    "No": 0,
    "YES": 1,
    "NO": 0,
    "Flood": 1,
    "No Flood": 0
})
y = pd.to_numeric(y, errors="coerce")
y = y.fillna(0)
y = y.astype(int)
X = X.apply(pd.to_numeric, errors='coerce')
X = X.fillna(0)

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Accuracy
pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, pred))

# Save Model
joblib.dump(model, "flood_model.pkl")
print("Model saved as flood_model.pkl")