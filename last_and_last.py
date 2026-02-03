import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
import os

# Path to the dataset
DATASET_PATH = r"D:\dr.crops2\plantvillage dataset\color"

# Image size and batch size
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Data augmentation generator
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=50,  
    zoom_range=0.4,     
    horizontal_flip=True,
    vertical_flip=True,  
    width_shift_range=0.4,  
    height_shift_range=0.4,
    brightness_range=[0.5, 1.5],  
    fill_mode='nearest',
    validation_split=0.2
)

# Exclude 'target_spot' class and use the rest of the classes
all_labels = os.listdir(DATASET_PATH)
all_labels.remove('Tomato___Target_Spot')  # Exclude 'target_spot' label

# Training and validation generators
train_generator = datagen.flow_from_directory(
    DATASET_PATH, 
    target_size=IMG_SIZE, 
    batch_size=BATCH_SIZE, 
    class_mode='categorical', 
    subset='training', 
    classes=all_labels  # Use the filtered labels
)

val_generator = datagen.flow_from_directory(
    DATASET_PATH, 
    target_size=IMG_SIZE, 
    batch_size=BATCH_SIZE, 
    class_mode='categorical', 
    subset='validation', 
    classes=all_labels  # Use the filtered labels
)

# Load pre-trained MobileNetV2 base model
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))

# Fine-tuning the pre-trained model
for layer in base_model.layers[-50:]:  # Fine-tune the last 50 layers
    layer.trainable = True

# Add custom layers on top of MobileNetV2
x = base_model.output
x = GlobalAveragePooling2D()(x)

# Add more dense layers for improved learning capacity
x = Dense(1024, activation='relu')(x)  # Added a dense layer with 1024 units
x = BatchNormalization()(x)           # Added batch normalization to stabilize training
x = Dropout(0.5)(x)                   # Dropout to prevent overfitting

x = Dense(512, activation='relu')(x)   # Added another dense layer
x = BatchNormalization()(x)
x = Dropout(0.5)(x)

# Output layer for disease classification
disease_output = Dense(len(all_labels), activation='softmax', name='disease_output')(x)

# Compile the model
model = Model(inputs=base_model.input, outputs=disease_output)
optimizer = Adam(learning_rate=1e-4)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Print model summary
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

# Save the trained model
model.save("tomato_disease_model_finetuned.h5")

# Evaluate the model on the validation set
val_loss, val_accuracy = model.evaluate(val_generator)
print(f"\nFinal Disease Classification Accuracy: {val_accuracy * 100:.2f}%")
print(f"Final Validation Loss: {val_loss:.4f}")

# Plot the training and validation accuracy
plt.figure(figsize=(8, 6))
plt.plot(history.history['accuracy'], label='Train Accuracy', marker='o')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy', marker='o')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training vs Validation Accuracy')
plt.grid()
plt.show()
