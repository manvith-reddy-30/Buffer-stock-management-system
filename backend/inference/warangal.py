import numpy as np
import joblib
from tensorflow.keras.models import load_model
from pathlib import Path

# Paths to model and scaler
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "lstms" / "warangal-tomato_price_prediction_model.h5"
SCALER_PATH = BASE_DIR / "scaler" / "warangal.save"

# Load model and scaler
model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


def predict_next_7_days(prices: list[float]) -> list[float]:
    """
    Predict the next 7 days of tomato prices using LSTM for Warangal.

    Args:
        prices (list[float]): Last 30 tomato prices (oldest to newest).

    Returns:
        list[float]: Predicted prices for next 7 days.
    """
    if len(prices) != 30:
        raise ValueError("Exactly 30 prices are required as input.")

    predictions = []

    # Make a copy of input and reshape for model
    input_seq = np.array(prices).reshape(-1, 1)
    input_scaled = scaler.transform(input_seq)

    for _ in range(7):
        model_input = input_scaled[-30:].reshape(1, 30, 1)
        next_pred_scaled = model.predict(model_input, verbose=0)
        next_pred = scaler.inverse_transform(next_pred_scaled)[0][0]

        predictions.append(round(next_pred, 2))

        # Append new prediction to sequence
        next_pred_scaled_reshaped = next_pred_scaled.reshape(1, 1)
        input_scaled = np.append(input_scaled, next_pred_scaled_reshaped, axis=0)

    return [float(x) for x in predictions]
