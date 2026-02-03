import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
from sklearn.utils.class_weight import compute_class_weight

# Path to dataset
DATASET_PATH = r"D:\dr.crops\dataset\colour"

# Image size & batch size
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Data Augmentation
datagen = ImageDataGenerator(
    rescale=1./255, rotation_range=40, zoom_range=0.3, horizontal_flip=True, 
    width_shift_range=0.3, height_shift_range=0.3, validation_split=0.2
)

# Training Set
train_generator = datagen.flow_from_directory(
    DATASET_PATH, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='categorical', subset='training'
)

# Validation Set
val_generator = datagen.flow_from_directory(
    DATASET_PATH, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode='categorical', subset='validation'
)

# Get class names & class counts
class_names = list(train_generator.class_indices.keys())
print("Class Labels:", class_names)

# Compute Class Weights to handle imbalance
class_counts = train_generator.classes
class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(class_counts), y=class_counts)
class_weight_dict = {i: class_weights[i] for i in range(len(class_names))}
print("Class Weights:", class_weight_dict)

# Load MobileNetV2 (without top layer)
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

# Unfreeze some layers for fine-tuning
for layer in base_model.layers[-20:]:  # Unfreeze last 20 layers
    layer.trainable = True

# Add custom layers
x = base_model.output
x = GlobalAveragePooling2D()(x)  # Convert feature maps to vector
x = Dense(256, activation='relu')(x)
x = BatchNormalization()(x)  # Normalization for stable training
x = Dropout(0.5)(x)  # Increased dropout to prevent overfitting
output = Dense(len(class_names), activation='softmax')(x)  # Output layer

# Define model
model = Model(inputs=base_model.input, outputs=output)

# Compile model with lower learning rate
optimizer = Adam(learning_rate=1e-4)  # Lower learning rate for fine-tuning
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Model Summary
model.summary()

# Train the model with class weights
EPOCHS = 15  # Increased epochs for better fine-tuning
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS,
    class_weight=class_weight_dict  # Applying class weights
)

# Save the fine-tuned model
model.save("tomato_disease_model_finetuned.h5")

# -------------------------------
# *Check Validation Accuracy*
# -------------------------------
val_loss, val_accuracy = model.evaluate(val_generator)
print(f"\nFinal Validation Accuracy: {val_accuracy * 100:.2f}%")

# -------------------------------
# *Plot Training vs Validation Accuracy*
# -------------------------------
plt.figure(figsize=(8, 6))
plt.plot(history.history['accuracy'], label='Train Accuracy', marker='o')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy', marker='o')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training vs Validation Accuracy')
plt.grid()
plt.show()

