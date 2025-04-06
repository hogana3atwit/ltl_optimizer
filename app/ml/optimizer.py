import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Example ML logic: Predict trailer utilization based on weight and cube

MODEL_PATH = "app/ml/trailer_util_model.pkl"

def train_utilization_model(data_path: str):
    data = pd.read_csv(data_path)

    # Expecting columns: weight, cube, utilization
    X = data[["weight", "cube"]]
    y = data["utilization"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)

    print(f"Model trained. MSE on test set: {mse:.4f}")
    joblib.dump(model, MODEL_PATH)
    return model

def load_model():
    return joblib.load(MODEL_PATH)

def predict_utilization(model, weight: float, cube: float):
    return model.predict([[weight, cube]])[0]
