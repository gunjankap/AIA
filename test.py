import requests
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Load dataset for scaler and label encoder
df = pd.read_csv("updated_environmental_with_images.csv")

# Label Encoding
label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['Predicted_Disease'])

# Scaling environmental features
scaler = MinMaxScaler()
scaler.fit(df[['temperature', 'humidity']])  # fit using the training data

# Load models
multimodal_model = load_model("multimodal_tomato_disease_model.h5")
cnn_model = load_model("tomato_disease_model.h5")
feature_extractor = Model(inputs=cnn_model.input, outputs=cnn_model.layers[-2].output)

# Your OpenWeatherMap API key
API_KEY = "6baa0aacc2d49d0b2a39aefa2472d414"

def get_weather_data(city_name, api_key=API_KEY):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        return temperature, humidity
    else:
        raise Exception(f"Weather API Error {response.status_code}: {response.text}")

def extract_image_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    features = feature_extractor.predict(img_array, verbose=0)
    return features

def predict_disease(img_path, city):
    # Step 1: Get weather info
    temp, humidity = get_weather_data(city)
    print(f"🌡 Temperature: {temp:.2f} °C")
    print(f"💧 Humidity: {humidity:.2f} %")

    # Step 2: Prepare inputs
    env_features = scaler.transform([[temp, humidity]])
    img_features = extract_image_features(img_path)

    # Step 3: Prediction
    prediction = multimodal_model.predict([img_features, env_features], verbose=0)
    predicted_index = np.argmax(prediction)
    predicted_label = label_encoder.inverse_transform([predicted_index])[0]
    confidence = prediction[0][predicted_index] * 100

    print(f"🩺 Predicted Disease: {predicted_label}")
    print(f"📊 Confidence: {confidence:.2f}%")

    return predicted_label, temp, humidity

# Run the script only if it's the main module
if __name__ == "__main__":
    image_path = r"D:\dr.crops\dataset\colour\Tomato___Leaf_Mold\0ae36892-5cb1-476e-8a51-b7fd8183a535___Crnl_L.Mold 6728.JPG"
    city_name = "Hisar"

    predicted_disease, temp, humidity = predict_disease(image_path, city_name)

    print("\n✅ Final Result")
    print("🌱 Predicted Disease:", predicted_disease)
    print("🌡  Temperature:", temp, "°C")
    print("💧 Humidity:", humidity, "%")
