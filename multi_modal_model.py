from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Concatenate
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import sys
sys.path.append("d:/dr.crops")  # Ensure import requests.py is importable
import importlib
city_module = importlib.import_module("import requests")  # import requests.py as a module

# 1. Load pre-extracted image features and environmental data
# Assume image_features.shape = (num_samples, 256)
# Assume env_data.shape = (num_samples, 2) -> [temperature, humidity]
# Assume labels.shape = (num_samples,) -> disease class

image_features = np.load("image_features.npy")
env_data = np.load("env_data.npy")
labels = np.load("labels.npy")

# 2. Preprocess
scaler = MinMaxScaler()
env_scaled = scaler.fit_transform(env_data)

y = to_categorical(labels)  # one-hot encode labels

# 3. Train-test split
X_img_train, X_img_test, X_env_train, X_env_test, y_train, y_test = train_test_split(
    image_features, env_scaled, y, test_size=0.2, random_state=42
)

# 4. Define model
image_input = Input(shape=(256,), name="image_input")
x1 = Dense(128, activation='relu')(image_input)
x1 = Dense(64, activation='relu')(x1)

env_input = Input(shape=(2,), name="env_input")
x2 = Dense(32, activation='relu')(env_input)
x2 = Dense(16, activation='relu')(x2)

combined = Concatenate()([x1, x2])
z = Dense(64, activation='relu')(combined)
z = Dense(32, activation='relu')(z)
output = Dense(y.shape[1], activation='softmax')(z)

model = Model(inputs=[image_input, env_input], outputs=output)
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# 5. Train
model.fit([X_img_train, X_env_train], y_train, validation_data=([X_img_test, X_env_test], y_test), epochs=50, batch_size=16)

# 6. Evaluate
loss, accuracy = model.evaluate([X_img_test, X_env_test], y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")
print(f"Test Loss: {loss:.4f}")

# 7. Save model
model.save("multi_modal_tomato_model.h5")


def predict_for_city(city_name):
    # Get weather data using your city disease detector logic
    weather_data, location, country, state = city_module.get_weather_by_city(city_name)
    temp = weather_data["temp"]
    humidity = weather_data["humidity"]
    print(f"\n📍 City: {location}, {country} | Temp: {temp}°C | Humidity: {humidity}%")

    # Scale environmental data using the same scaler as training
    env_input = city_module.np.array([[temp, humidity]])
    env_input_scaled = scaler.transform(env_input)

    # For demonstration, use a random image feature (or you can select one)
    # In practice, you should extract image features for a real image
    img_input = image_features[0].reshape(1, -1)  # Example: use the first image feature

    # Predict using the multi-modal model
    pred = model.predict([img_input, env_input_scaled])
    predicted_class = np.argmax(pred, axis=1)[0]
    print(f"Model Prediction: Class {predicted_class} (probabilities: {pred[0]})")

    # Also print city disease detector's risk analysis
    disease_risks = city_module.check_disease_risks(weather_data)
    if disease_risks:
        print("\n🚨 Disease Warnings (City Detector):")
        for r in disease_risks:
            print(f"🌿 {r['disease']}: {r['risk']} RISK ({r['probability']}% chance)")
    else:
        print("✅ No high-risk diseases based on current conditions.")

# --- Example usage ---
if __name__ == "__main__":
    city = input("Enter city name for multi-modal prediction: ")
    predict_for_city(city)
