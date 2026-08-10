import os

DATASET_PATH = "../datasets/raw/PlantVillage"

print("=" * 50)
print("DISEASE CLASSES FOUND:")
print("=" * 50)

class_folders = sorted(os.listdir(DATASET_PATH))
total_images = 0

for class_name in class_folders:
    class_path = os.path.join(DATASET_PATH, class_name)
    if os.path.isdir(class_path):
        image_count = len([
            f for f in os.listdir(class_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ])
        total_images += image_count
        print(f"{class_name}: {image_count} images")

print("=" * 50)
print(f"TOTAL CLASSES: {len([c for c in class_folders if os.path.isdir(os.path.join(DATASET_PATH, c))])}")
print(f"TOTAL IMAGES: {total_images}")
print("=" * 50)