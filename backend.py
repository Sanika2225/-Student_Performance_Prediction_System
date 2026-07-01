from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import sys
sys.path.insert(0, '.')
from src.predict import predict_performance

app = Flask(__name__)
CORS(app)   # 🔥 THIS IS MANDATORY

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Backend is running"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        print("RAW INPUT DATA:", data)
        
        # Call the predict_performance function with the input data
        prediction = predict_performance(data)
        
        if prediction <= 6:
            level = "Poor (At Risk)"
        elif prediction <= 10:
            level = "Average"
        else:
            level = "Good"
        
        return jsonify({
            "predicted_grade": int(prediction),
            "performance_level": level
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400

if __name__ == "__main__":
    app.run(debug=False, port=5000)
