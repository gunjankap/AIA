import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
import scipy.special

# Path to dataset
DATASET_PATH = r"D:\dr.crops\dataset\colour"

# Image size & batch size
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Enhanced Data Augmentation
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=50,  # More rotation
    zoom_range=0.4,     # More zoom
    horizontal_flip=True,
    vertical_flip=True,  # Flip vertically too
    width_shift_range=0.4,  # Bigger shift
    height_shift_range=0.4,
    brightness_range=[0.5, 1.5],  # Change brightness
    fill_mode='nearest',
    validation_split=0.2
)

# Training Set (Disease Classification)
train_generator = datagen.flow_from_directory(
    DATASET_PATH, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='categorical', subset='training'
)

# Validation Set (Disease Classification)
val_generator = datagen.flow_from_directory(
    DATASET_PATH, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='categorical', subset='validation'
)

# Load MobileNetV2 (without top layer)
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

# Unfreeze last 20 layers for fine-tuning
for layer in base_model.layers[-50:]:
    layer.trainable = True

# Add custom layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation='relu')(x)
x = BatchNormalization()(x)
x = Dropout(0.5)(x)

# Output for Disease Classification (Multi-Class)
disease_output = Dense(len(train_generator.class_indices), activation='softmax', name='disease_output')(x)

# Define model
model = Model(inputs=base_model.input, outputs=disease_output)

# Compile model
optimizer = Adam(learning_rate=1e-4)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Model Summary
model.summary()

# Train the model
EPOCHS = 15
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS,
    steps_per_epoch=len(train_generator),
    validation_steps=len(val_generator),
)

# Save the fine-tuned model
model.save("tomato_disease_model.h5")

# Evaluate Validation Accuracy & Loss
val_loss, val_accuracy = model.evaluate(val_generator)
print(f"\nFinal Disease Classification Accuracy: {val_accuracy * 100:.2f}%")
print(f"Final Validation Loss: {val_loss:.4f}")

# Plot Training vs Validation Accuracy
plt.figure(figsize=(8, 6))
plt.plot(history.history['accuracy'], label='Train Accuracy', marker='o')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy', marker='o')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training vs Validation Accuracy')
plt.grid()
plt.show()

# Confidence Calibration for Predictions
def calibrated_softmax(logits, temp=2.0):  
    logits_scaled = logits / temp  
    return scipy.special.softmax(logits_scaled)

# Test with a New Image
from tensorflow.keras.preprocessing import image

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    
    logits = model.predict(img_array)[0]  # Get raw logits
    scaled_probs = calibrated_softmax(logits, temp=2.0)
    
    disease_pred = np.argmax(scaled_probs)
    print(f"Predicted Disease: {list(train_generator.class_indices.keys())[disease_pred]} (Confidence: {scaled_probs[disease_pred] * 100:.2f}%)")

# Example Usage
# predict_image("D:/dr.crops/test_image.jpg")