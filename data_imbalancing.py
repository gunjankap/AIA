import os
import cv2
import numpy as np
import imgaug.augmenters as iaa
from shutil import copy2

# Path to your dataset
dataset_path = r"D:\dr.crops\dataset\colour"

# Get class distribution
class_counts = {cls: len(os.listdir(os.path.join(dataset_path, cls))) for cls in os.listdir(dataset_path)}
max_count = max(class_counts.values())

# Define augmentation pipeline
augmenters = iaa.Sequential([
    iaa.Fliplr(0.5),  # Flip horizontally with 50% probability
    iaa.Affine(rotate=(-20, 20)),  # Rotate images randomly
    iaa.GaussianBlur(sigma=(0, 1.0))  # Apply slight blur
])

# Augment images in underrepresented classes
for cls, count in class_counts.items():
    class_path = os.path.join(dataset_path, cls)
    
    if count < max_count:
        images = [cv2.imread(os.path.join(class_path, img)) for img in os.listdir(class_path)]
        images = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in images if img is not None]

        i = 0
        while len(os.listdir(class_path)) < max_count:
            img = images[i % len(images)]  # Cycle through available images
            aug_img = augmenters.augment_image(img)
            aug_img = cv2.cvtColor(aug_img, cv2.COLOR_RGB2BGR)

            aug_filename = f"aug_{len(os.listdir(class_path))}.jpg"
            cv2.imwrite(os.path.join(class_path, aug_filename), aug_img)
            i += 1

print("Dataset balanced successfully!")
