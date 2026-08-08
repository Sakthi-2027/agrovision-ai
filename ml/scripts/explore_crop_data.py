import pandas as pd

# Load the dataset
df = pd.read_csv("../datasets/raw/Crop_recommendation.csv")

print("=" * 50)
print("SHAPE (rows, columns):", df.shape)
print("=" * 50)

print("\nFIRST 5 ROWS:")
print(df.head())

print("\n" + "=" * 50)
print("COLUMN INFO (types + missing values):")
print("=" * 50)
print(df.info())

print("\n" + "=" * 50)
print("STATISTICAL SUMMARY:")
print("=" * 50)
print(df.describe())

print("\n" + "=" * 50)
print("MISSING VALUES PER COLUMN:")
print("=" * 50)
print(df.isnull().sum())

print("\n" + "=" * 50)
print("CROP CLASS DISTRIBUTION (is it balanced?):")
print("=" * 50)
print(df['label'].value_counts())