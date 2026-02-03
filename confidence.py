import cv2
import tensorflow as tf
import numpy as np

# Load the trained model
MODEL_PATH = "tomato_disease_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Define class labels
class_names = ['Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Healthy', 'Tomato_Late_blight', 'Tomato_Leaf_Mold']

# Function to predict the disease from an image
def predict_image(image_path):
    # Read and preprocess the image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    img = cv2.resize(img, (224, 224))  # Resize to match model input
    img = np.expand_dims(img, axis=0) / 255.0  # Normalize

    # Make prediction
    prediction = model.predict(img)
    confidence_scores = prediction[0] * 100  # Convert to percentage

    # Print confidence scores for all classes
    for i, class_name in enumerate(class_names):
        print(f"{class_name}: {confidence_scores[i]:.2f}%")

    # Get highest confidence prediction
    class_idx = np.argmax(prediction)
    class_label = class_names[class_idx]
    confidence = confidence_scores[class_idx]

    print(f"Prediction: {class_label}, Confidence: {confidence:.2f}%")
    return class_label, confidence

# Example usage
image_path = r"D:\dr.crops\dataset\colour\Tomato___Bacterial_spot\0a6d40e4-75d6-4659-8bc1-22f47cdb2ca8___GCREC_Bact.Sp 6247.JPG"  # ✅ Use raw string (r"") to avoid issues with backslashes
predict_image(image_path)
