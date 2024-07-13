import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

class AnomalyDetectionModel:
    def __init__(self):
        self.model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
        self.data = []

    def collect_data(self, data_point):
        self.data.append(data_point)

    def train_model(self):
        if len(self.data) > 0:
            X = np.array(self.data)
            self.model.fit(X)
            print("Model trained successfully.")
        else:
            print("No data available for training.")

    def predict(self, data_point):
        return self.model.predict([data_point])

    def save_model(self, file_path):
        joblib.dump(self.model, file_path)
        print(f"Model saved to {file_path}.")

    def load_model(self, file_path):
        if os.path.exists(file_path):
            self.model = joblib.load(file_path)
            print(f"Model loaded from {file_path}.")
        else:
            print(f"Model file {file_path} does not exist.")

# Example usage
if __name__ == "__main__":
    model = AnomalyDetectionModel()
    # Collect some example data points
    model.collect_data([0.1, 0.2, 0.3])
    model.collect_data([0.4, 0.5, 0.6])
    model.collect_data([0.7, 0.8, 0.9])
    # Train the model
    model.train_model()
    # Predict an anomaly
    prediction = model.predict([0.1, 0.2, 0.3])
    print(f"Prediction: {prediction}")
    # Save the model
    model.save_model("anomaly_detection_model.pkl")
    # Load the model
    model.load_model("anomaly_detection_model.pkl")
