import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

# 1. Load dataset
df = pd.read_csv("balanced_environmental_data.csv")

# 2. Encode target
le = LabelEncoder()
df['disease_label'] = le.fit_transform(df['Predicted_Disease'])

# 3. Split features and target
X = df[['temperature', 'humidity']]
y = to_categorical(df['disease_label'])

# 4. Normalize features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# 5. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 6. Build model
model = Sequential([
    Dense(64, activation='relu', input_shape=(2,)),
    Dense(32, activation='relu'),
    Dense(y.shape[1], activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 7. Train
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=16)

# 8. Evaluate on test data
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"\n✅ Test Accuracy: {test_accuracy * 100:.2f}%")
print(f"❌ Test Loss: {test_loss:.4f}")

# 9. Save model
model.save("env_only_disease_model.h5")
