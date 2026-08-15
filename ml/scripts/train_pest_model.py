import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os
import json

DATASET_PATH = "../datasets/raw/pest_images"
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 6


train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

class_names = train_ds.class_names
num_classes = len(class_names)
print(f"Training on {num_classes} classes: {class_names}")


train_ds = train_ds.map(lambda x, y: (preprocess_input(x), y))
val_ds = val_ds.map(lambda x, y: (preprocess_input(x), y))

train_ds = train_ds.cache().prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.cache().prefetch(tf.data.AUTOTUNE)


base_model = MobileNetV2(input_shape=(128, 128, 3), include_top=False, weights="imagenet")
base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation="relu")(x)
x = Dropout(0.3)(x)
predictions = Dense(num_classes, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=predictions)
model.compile(optimizer=Adam(learning_rate=0.001), loss="sparse_categorical_crossentropy", metrics=["accuracy"])


print("\nStarting training...\n")
history = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)


val_loss, val_accuracy = model.evaluate(val_ds)
print(f"\n🏆 Final validation accuracy: {val_accuracy * 100:.2f}%")


os.makedirs("../models", exist_ok=True)
model.save("../models/pest_prediction_model.keras")

label_map = {i: name for i, name in enumerate(class_names)}
with open("../models/pest_class_labels.json", "w") as f:
    json.dump(label_map, f, indent=2)

print("✅ Saved model to ml/models/pest_prediction_model.keras")
print("✅ Saved class labels to ml/models/pest_class_labels.json")