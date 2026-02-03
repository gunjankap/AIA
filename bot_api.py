from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
import joblib

app = FastAPI(title="Dr Crops AI Bot")

# Load model
model = load_model("prioritized_multimodal_model.h5")

# Dummy image feature extractor
# (Replace this with real CNN feature extractor later)
def extract_image_features(image: Image.Image):
    img = image.resize((224, 224))
    arr = np.array(img) / 255.0
    return np.random.rand(256)  # placeholder

@app.post("/predict")
async def predict(
    image: UploadFile = File(...),
    temperature: float = 25.0,
    humidity: float = 60.0
):
    # Read image
    contents = await image.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")

    # Prepare inputs
    img_features = extract_image_features(img).reshape(1, 256)
    env_features = np.array([[temperature, humidity]])

    # Predict
    prediction = model.predict([img_features, env_features])
    class_id = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    return {
        "predicted_class": class_id,
        "confidence": round(confidence, 3)
    }
