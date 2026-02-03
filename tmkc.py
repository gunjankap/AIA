import numpy as np
from tensorflow.keras.models import load_model, Model, Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
import joblib
import pandas as pd
from tensorflow.keras.preprocessing import image
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb

# === Load Models ===
cnn_model = load_model("tomato_disease_model_finetuned.h5")
env_model = load_model("env_only_disease_model.h5")
multi_model = load_model("multimodal_tomato_disease_model.h5")
xgb_model = joblib.load("xgboost_disease_model.pkl")
rf_model = joblib.load("random_forest_disease_model.pkl")

# === Load label encoder ===
label_encoder = joblib.load("label_encoder.pkl")

# === Load and preprocess input ===
img_path = r"D:\dr.crops3\test\Leaf_Mold\0ac36661-a47d-47ff-8948-42edec033b87___Crnl_L.Mold 9127.JPG"
temperature = 25.0
humidity = 65.0

# Preprocess image for CNN and multimodal
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

img_array = preprocess_image(img_path)

# Feature extractor from CNN
feature_extractor = Model(inputs=cnn_model.input, outputs=cnn_model.layers[-2].output)
img_features = feature_extractor.predict(img_array)

# 🔧 Fix shape using temporary Dense layer
feature_reducer = Sequential([Dense(256, input_shape=(img_features.shape[1],), activation='relu')])
img_features_256 = feature_reducer.predict(img_features)

# Normalize environmental features
scaler = joblib.load("scaler.pkl")  # Pre-fitted MinMaxScaler
X_env = scaler.transform([[temperature, humidity]])

# === Get Predictions ===

# CNN prediction
pred_cnn = cnn_model.predict(img_array)

# Environmental model
pred_env = env_model.predict(X_env)

# Multimodal model (with reduced image feature)
pred_multi = multi_model.predict([img_features_256, X_env])

# XGBoost
X_combined = np.concatenate([img_features_256, X_env], axis=1)
pred_xgb = xgb_model.predict_proba(X_env)

# Random Forest
pred_rf = rf_model.predict_proba(X_env)

# === Weighted Average Ensemble ===
w_cnn = 0.6
w_env = 0.1
w_multi = 0.1
w_xgb = 0.1
w_rf = 0.1

final_probs = (
    w_cnn * pred_cnn +
    w_env * pred_env +
    w_multi * pred_multi +
    w_xgb * pred_xgb +
    w_rf * pred_rf
)

predicted_class = np.argmax(final_probs)
predicted_label = label_encoder.inverse_transform([predicted_class])[0]

print("✅ Final Ensemble Prediction:", predicted_label)
