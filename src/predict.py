import joblib
import pandas as pd
from src.preprocess import preprocess_data

# Load trained model
model = joblib.load("models/student_model.pkl")

def predict_performance(input_data):
    """
    Predict student performance given input features.
    input_data should be a dictionary with the required features from the dataset.
    """
    # Create a DataFrame from the input
    df = pd.DataFrame([input_data])
    
    # Use the same preprocessing as training, with is_training=False
    # This will use the saved preprocessor
    X, _ = preprocess_data(df, is_training=False)
    
    # Make prediction
    prediction = model.predict(X)
    return int(prediction[0])
