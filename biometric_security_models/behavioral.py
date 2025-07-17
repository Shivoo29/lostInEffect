import os
import cv2
import numpy as np
import joblib

class BehavioralAnalytics:
    """
    ML-focused behavioral analytics module.
    Uses a trained model to analyze fingerprint image data for anomalies.
    """
    def __init__(self):
        self.model = None
        self.IMG_SIZE = (96, 96) # Must match the size used during training
        self._load_model()

    def _load_model(self):
        model_path = os.path.join(os.path.dirname(__file__), "fingerprint_anomaly_model.joblib")
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                print(f"Successfully loaded fingerprint anomaly model from {model_path}")
            except Exception as e:
                print(f"Error loading model from {model_path}: {e}")
                self.model = None
        else:
            print(f"Warning: Model file not found at {model_path}. Please train the model first.")

    def _preprocess_image(self, image_path):
        """Loads an image, converts to grayscale, and resizes it."""
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f"Could not load image {image_path}")
        img = cv2.resize(img, self.IMG_SIZE)
        return img

    def _extract_features(self, image):
        """
        Extracts features from a preprocessed image.
        Must match the feature extraction used during training.
        """
        return image.flatten()

    def analyze_fingerprint_image(self, image_path):
        """
        Analyzes a fingerprint image for anomalies using the trained ML model.

        Args:
            image_path (str): The file path to the fingerprint image.

        Returns:
            dict: A dictionary with the analysis score and anomaly status.
        """
        if self.model is None:
            return {
                "behavioral_score": 0.5, # Neutral score if model not loaded
                "is_anomaly": False,
                "details": {
                    "analysis_reasons": ["ML model not loaded. Using default behavioral score."]
                }
            }

        try:
            img = self._preprocess_image(image_path)
            features = self._extract_features(img)
            
            # Reshape for single prediction
            features = features.reshape(1, -1)

            # Predict probability of being anomalous (class 1)
            # Assuming the model is trained to output probabilities
            anomaly_probability = self.model.predict_proba(features)[0][1] # Probability of class 1 (altered)

            is_anomaly = anomaly_probability > 0.5 # Threshold for anomaly
            
            reasons = []
            if is_anomaly:
                reasons.append(f"High probability of being an anomalous fingerprint ({anomaly_probability:.2f}).")
            else:
                reasons.append(f"Low probability of being an anomalous fingerprint ({anomaly_probability:.2f}).")

            return {
                "behavioral_score": 1.0 - anomaly_probability, # Higher score for less anomalous
                "is_anomaly": is_anomaly,
                "details": {
                    "analysis_reasons": reasons
                }
            }
        except FileNotFoundError as e:
            return {
                "behavioral_score": 0.0,
                "is_anomaly": True,
                "details": {
                    "analysis_reasons": [str(e), "File not found, cannot analyze."]
                }
            }
        except Exception as e:
            return {
                "behavioral_score": 0.0,
                "is_anomaly": True,
                "details": {
                    "analysis_reasons": [f"Error during analysis: {e}"]
                }
            }