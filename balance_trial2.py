import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
import scipy.special
import os

# ✅ Paths
DATASET_PATH = r"D:\dr.crops\dataset\colour"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# ✅ Data Augmentation
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

train_generator = datagen.flow_from_directory(
    DATASET_PATH, target_size=IMG_SIZE, batch_size=BATCH_SIZE,
    class_mode='categorical', subset='training'
)

val_generator = datagen.flow_from_directory(
    DATASET_PATH, target_size=IMG_SIZE, batch_size=BATCH_SIZE,
    class_mode='categorical', subset='validation'
)

# ✅ Base Model
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
for layer in base_model.layers[-50:]:
    layer.trainable = True

# ✅ Head for Deep Feature Learning
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)           # 🔥 More expressive power
x = BatchNormalization()(x)
x = Dropout(0.4)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.3)(x)

# ✅ Classification Layer
disease_output = Dense(len(train_generator.class_indices), activation='softmax', name='disease_output')(x)

# ✅ Model Assembly
model = Model(inputs=base_model.input, outputs=disease_output)

# ✅ Compile
optimizer = Adam(learning_rate=1e-4)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# ✅ Summary
model.summary()

# ✅ Training
EPOCHS = 15
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS,
    steps_per_epoch=len(train_generator),
    validation_steps=len(val_generator),
)

# ✅ Save
model.save("tomato_disease_model.h5")

# ✅ Evaluation
val_loss, val_accuracy = model.evaluate(val_generator)
print(f"\nFinal Disease Classification Accuracy: {val_accuracy * 100:.2f}%")
print(f"Final Validation Loss: {val_loss:.4f}")

# ✅ Plot Accuracy
plt.figure(figsize=(8, 6))
plt.plot(history.history['accuracy'], label='Train Accuracy', marker='o')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy', marker='o')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.title('Training vs Validation Accuracy')
plt.grid()
plt.show()