import os
import joblib
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load the trained model + metadata once, at startup
MODEL = joblib.load("model.pkl")
META = joblib.load("columns.pkl")
FEATURE_COLS = META["feature_cols"]
ENCODERS = META["encoders"]
TRAIN_YEAR = META["current_year_used_for_training"]


def build_feature_row(payload: dict):
    """Turn raw input (JSON or form data) into the numeric row the model expects."""
    car_age = TRAIN_YEAR - int(payload["year"])

    raw = {
        "Present_Price": float(payload["present_price"]),
        "Kms_Driven": float(payload["kms_driven"]),
        "Fuel_Type": payload["fuel_type"],
        "Seller_Type": payload["seller_type"],
        "Transmission": payload["transmission"],
        "Owner": int(payload["owner"]),
        "Car_Age": car_age,
    }

    row = []
    for col in FEATURE_COLS:
        val = raw[col]
        if col in ENCODERS:
            val = ENCODERS[col].transform([val])[0]
        row.append(val)
    return row


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        fuel_types=list(ENCODERS["Fuel_Type"].classes_),
        seller_types=list(ENCODERS["Seller_Type"].classes_),
        transmissions=list(ENCODERS["Transmission"].classes_),
        prediction=None,
    )


@app.route("/predict", methods=["POST"])
def predict_form():
    """Handles the HTML form submission."""
    try:
        row = build_feature_row(request.form)
        pred = MODEL.predict([row])[0]
        prediction = f"{pred:.2f} lakhs"
    except Exception as e:
        prediction = f"Error: {e}"

    return render_template(
        "index.html",
        fuel_types=list(ENCODERS["Fuel_Type"].classes_),
        seller_types=list(ENCODERS["Seller_Type"].classes_),
        transmissions=list(ENCODERS["Transmission"].classes_),
        prediction=prediction,
    )


@app.route("/api/predict", methods=["POST"])
def predict_api():
    """JSON API: POST the same fields as JSON, get back a JSON prediction."""
    try:
        payload = request.get_json(force=True)
        row = build_feature_row(payload)
        pred = MODEL.predict([row])[0]
        return jsonify({"selling_price_lakhs": round(float(pred), 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
