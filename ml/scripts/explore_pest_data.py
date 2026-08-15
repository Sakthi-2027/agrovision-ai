import os

DATASET_PATH = "../datasets/raw"
PEST_CLASSES = ["ants", "bees", "beetle", "catterpillar", "earthworms", "earwig",
                 "grasshopper", "moth", "slug", "snail", "wasp", "weevil"]

print("=" * 50)
print("PEST CLASSES FOUND:")
print("=" * 50)

total_images = 0
for class_name in PEST_CLASSES:
    class_path = os.path.join(DATASET_PATH, class_name)
    if os.path.isdir(class_path):
        image_count = len([
            f for f in os.listdir(class_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ])
        total_images += image_count
        print(f"{class_name}: {image_count} images")
    else:
        print(f"{class_name}: FOLDER NOT FOUND")

print("=" * 50)
print(f"TOTAL IMAGES: {total_images}")
print("=" * 50)