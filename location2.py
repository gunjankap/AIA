import requests
import numpy as np
import pandas as pd
import joblib

from tensorflow.keras.models import load_model, Model, Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing import image
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# === Load and Prepare Data ===
df = pd.read_csv("updated_environmental_with_images.csv")
label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['Predicted_Disease'])

scaler = MinMaxScaler()
scaler.fit(df[['temperature', 'humidity']])

# === Load Models ===
cnn_model = load_model("tomato_disease_model_finetuned.h5")
env_model = load_model("env_only_disease_model.h5")
multi_model = load_model("multimodal_tomato_disease_model.h5")
xgb_model = joblib.load("xgboost_disease_model.pkl")
rf_model = joblib.load("random_forest_disease_model.pkl")

# CNN Feature Extractor and Reducer
feature_extractor = Model(inputs=cnn_model.input, outputs=cnn_model.layers[-2].output)
feature_reducer = Sequential([Dense(256, input_shape=(512,), activation='relu')])

# === Weather API ===
API_KEY = "6baa0aacc2d49d0b2a39aefa2472d414"

def get_weather_data(city, api_key=API_KEY):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {'q': city, 'appid': api_key, 'units': 'metric'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['main']['temp'], data['main']['humidity']
    else:
        raise Exception(f"Weather API Error {response.status_code}: {response.text}")

# === Image Preprocessing ===
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

# === Prediction Function ===
def predict_disease_with_ensemble(img_path, city):
    # Get weather data
    temp, humidity = get_weather_data(city)
    X_env = scaler.transform([[temp, humidity]])

    # Preprocess image and extract features
    img_array = preprocess_image(img_path)
    img_features = feature_extractor.predict(img_array, verbose=0)
    img_features_256 = feature_reducer.predict(img_features, verbose=0)

    # Individual Predictions
    pred_cnn = cnn_model.predict(img_array, verbose=0)
    pred_env = env_model.predict(X_env, verbose=0)
    pred_multi = multi_model.predict([img_features_256, X_env], verbose=0)
    pred_xgb = xgb_model.predict_proba(X_env)
    pred_rf = rf_model.predict_proba(X_env)

    # Ensemble Weighted Average
    final_probs = (
        0.6 * pred_cnn +
        0.1 * pred_env +
        0.1 * pred_multi +
        0.1 * pred_xgb +
        0.1 * pred_rf
    )

    pred_idx = np.argmax(final_probs)
    predicted_label = label_encoder.inverse_transform([pred_idx])[0]

    return predicted_label, temp, humidity

# === Test ===
if __name__ == "__main__":
    image_path = r"D:\dr.crops3\plantvillage dataset\color\Tomato___Bacterial_spot\0a6d40e4-75d6-4659-8bc1-22f47cdb2ca8___GCREC_Bact.Sp 6247.JPG"
    city_name = "Hisar"

    predicted_disease, temp, humidity = predict_disease_with_ensemble(image_path, city_name)

    print("✅ Predicted Disease:", predicted_disease)
    print("🌡️ Temperature:", temp, "°C")
    print("💧 Humidity:", humidity, "%")
