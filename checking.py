import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# Path to dataset and model
DATASET_PATH = r"D:\dr.crops\dataset\colour"
MODEL_PATH = "tomato_disease_model.h5"

# Image size & batch size
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Data Augmentation for Validation
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

# Validation Set
val_generator = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# Load the saved model
model = tf.keras.models.load_model(MODEL_PATH)

# Evaluate model on validation data
val_loss, val_accuracy = model.evaluate(val_generator)
print(f"\nValidation Loss: {val_loss:.4f}")
print(f"Validation Accuracy: {val_accuracy * 100:.2f}%")
