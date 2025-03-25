import os
import random
import shutil

images_folder = "./images" 
annotations_folder = "./annotations"
output_folder = "./staged"

train_ratio = 0.8
random_seed = 42

train_images_folder = os.path.join(output_folder, "images/train")
val_images_folder = os.path.join(output_folder, "images/val")
train_labels_folder = os.path.join(output_folder, "labels/train")
val_labels_folder = os.path.join(output_folder, "labels/val")

os.makedirs(train_images_folder, exist_ok=True)
os.makedirs(val_images_folder, exist_ok=True)
os.makedirs(train_labels_folder, exist_ok=True)
os.makedirs(val_labels_folder, exist_ok=True)

# Get list of image files and corresponding annotation files
image_files = [f for f in os.listdir(images_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]
annotation_files = [f.replace('.jpg', '.txt').replace('.png', '.txt').replace('.jpeg', '.txt') for f in image_files]

# Ensure each image has a corresponding annotation
paired_files = [(img, ann) for img, ann in zip(image_files, annotation_files) if os.path.exists(os.path.join(annotations_folder, ann))]

# Shuffle and split
random.seed(random_seed)
random.shuffle(paired_files)
train_count = int(len(paired_files) * train_ratio)
train_files = paired_files[:train_count]
val_files = paired_files[train_count:]

# Move files to train/val folders
for img, ann in train_files:
    shutil.copy(os.path.join(images_folder, img), os.path.join(train_images_folder, img))
    shutil.copy(os.path.join(annotations_folder, ann), os.path.join(train_labels_folder, ann))

for img, ann in val_files:
    shutil.copy(os.path.join(images_folder, img), os.path.join(val_images_folder, img))
    shutil.copy(os.path.join(annotations_folder, ann), os.path.join(val_labels_folder, ann))

print(f"Dataset split complete!")
print(f"Training set: {len(train_files)} images")
print(f"Validation set: {len(val_files)} images")