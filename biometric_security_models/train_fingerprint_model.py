
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import glob

# Define paths
DATASET_ROOT = "/home/skj/Documents/projects/lostInEffect/datasets/Sokoto_conventry_Fingerprint_Dataset/SOCOFing/"
REAL_DIR = os.path.join(DATASET_ROOT, "Real")
ALTERED_DIR = os.path.join(DATASET_ROOT, "Altered")

# Model save path
MODEL_PATH = "/home/skj/Documents/projects/lostInEffect/biometric_security_models/fingerprint_anomaly_model.joblib"

# Image preprocessing parameters
IMG_SIZE = (96, 96) # Resize images to a fixed size

def load_and_preprocess_image(image_path):
    """Loads an image, converts to grayscale, and resizes it."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Warning: Could not load image {image_path}")
        return None
    img = cv2.resize(img, IMG_SIZE)
    return img

def extract_features(image):
    """
    Extracts simple features from a preprocessed image.
    For simplicity, we'll flatten the pixel values.
    In a real-world scenario, more advanced feature extraction (e.g., Gabor filters, minutiae)
    or a CNN would be used.
    """
    return image.flatten()

def load_dataset(limit=None):
    """
    Loads images from the dataset, extracts features, and assigns labels.
    :param limit: Optional. Limit the number of images loaded from each category for faster testing.
    """
    data = []
    labels = []

    print("Loading real fingerprints...")
    real_images = glob.glob(os.path.join(REAL_DIR, "*.BMP"))
    if limit:
        real_images = real_images[:limit]
    for i, img_path in enumerate(real_images):
        if i % 100 == 0:
            print(f"  Processing real image {i+1}/{len(real_images)}")
        img = load_and_preprocess_image(img_path)
        if img is not None:
            features = extract_features(img)
            data.append(features)
            labels.append(0) # 0 for real

    print("Loading altered fingerprints...")
    # Iterate through subdirectories of Altered
    altered_subdirs = ["Altered-Easy", "Altered-Medium", "Altered-Hard"]
    for subdir in altered_subdirs:
        current_dir = os.path.join(ALTERED_DIR, subdir)
        altered_images = glob.glob(os.path.join(current_dir, "*.BMP"))
        if limit:
            altered_images = altered_images[:limit]
        for i, img_path in enumerate(altered_images):
            if i % 100 == 0:
                print(f"  Processing altered image {i+1}/{len(altered_images)} from {subdir}")
            img = load_and_preprocess_image(img_path)
            if img is not None:
                features = extract_features(img)
                data.append(features)
                labels.append(1) # 1 for altered

    return np.array(data), np.array(labels)

def train_model():
    """Trains and saves the RandomForestClassifier model."""
    # Load a subset of the data for demonstration purposes
    # Adjust 'limit' based on your system's memory and desired training time
    X, y = load_dataset(limit=500) # Load 500 real and 500 altered images

    if len(X) == 0:
        print("No data loaded. Exiting training.")
        return

    print(f"Total samples loaded: {len(X)}")
    print(f"Feature dimension: {X.shape[1]}")

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Training RandomForestClassifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    print("Training complete.")

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=["Real", "Altered"]))

    # Save the trained model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
