from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Concatenate, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# ===== 1. Load Data =====
image_features = np.load("image_features.npy")  # shape (n, 256)
env_data = np.load("env_data.npy")              # shape (n, 2)
labels = np.load("labels.npy")                  # shape (n,)

# ===== 2. Preprocessing =====
scaler = MinMaxScaler()
env_scaled = scaler.fit_transform(env_data)

y = to_categorical(labels)  # one-hot encoding

# ===== 3. Train-Test Split =====
X_img_train, X_img_test, X_env_train, X_env_test, y_train, y_test = train_test_split(
    image_features, env_scaled, y, test_size=0.2, random_state=42
)

# ===== 4. Define Model =====

# 🔵 Image Branch (Priority)
image_input = Input(shape=(256,), name="image_input")
x1 = Dense(256, activation='relu')(image_input)
x1 = Dropout(0.3)(x1)
x1 = Dense(128, activation='relu')(x1)
x1 = Dropout(0.3)(x1)
x1 = Dense(64, activation='relu')(x1)  # deeper and wider = more importance

# 🟢 Environmental Branch (Lightweight)
env_input = Input(shape=(2,), name="env_input")
x2 = Dense(16, activation='relu')(env_input)
x2 = Dense(8, activation='relu')(x2)   # fewer params = less importance

# 🔗 Fusion
combined = Concatenate()([x1, x2])
z = Dense(64, activation='relu')(combined)
z = Dropout(0.3)(z)
z = Dense(32, activation='relu')(z)
output = Dense(y.shape[1], activation='softmax')(z)

# 🧠 Model Compile
model = Model(inputs=[image_input, env_input], outputs=output)
model.compile(optimizer=Adam(learning_rate=1e-4), loss='categorical_crossentropy', metrics=['accuracy'])

# ===== 5. Train =====
model.fit(
    [X_img_train, X_env_train],
    y_train,
    validation_data=([X_img_test, X_env_test], y_test),
    epochs=50,
    batch_size=16
)

# ===== 6. Evaluate =====
loss, accuracy = model.evaluate([X_img_test, X_env_test], y_test)
print(f"✅ Test Accuracy: {accuracy * 100:.2f}%")
print(f"❌ Test Loss: {loss:.4f}")

# ===== 7. Save Model =====
model.save("prioritized_multimodal_model.h5")
