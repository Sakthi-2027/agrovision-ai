import os
import shutil

RAW_PATH = "../datasets/raw"
PEST_PATH = "../datasets/raw/pest_images"
PEST_CLASSES = ["ants", "bees", "beetle", "catterpillar", "earthworms", "earwig",
                 "grasshopper", "moth", "slug", "snail", "wasp", "weevil"]

os.makedirs(PEST_PATH, exist_ok=True)

for class_name in PEST_CLASSES:
    source = os.path.join(RAW_PATH, class_name)
    destination = os.path.join(PEST_PATH, class_name)

    if os.path.exists(source) and not os.path.exists(destination):
        shutil.move(source, destination)
        print(f"Moved {class_name} -> pest_images/{class_name}")
    elif os.path.exists(destination):
        print(f"{class_name} already organized, skipping")
    else:
        print(f"⚠️ {class_name} not found in raw/")

print("\n✅ All pest folders now organized under ml/datasets/raw/pest_images/")