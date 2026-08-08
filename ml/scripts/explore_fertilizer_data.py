import pandas as pd

df = pd.read_csv("../datasets/raw/Fertilizer Prediction.csv")

print("=" * 50)
print("SHAPE (rows, columns):", df.shape)
print("=" * 50)

print("\nCOLUMN NAMES:")
print(df.columns.tolist())

print("\nFIRST 5 ROWS:")
print(df.head())

print("\n" + "=" * 50)
print("COLUMN INFO (types + missing values):")
print("=" * 50)
print(df.info())

print("\n" + "=" * 50)
print("MISSING VALUES PER COLUMN:")
print("=" * 50)
print(df.isnull().sum())
print("\n" + "=" * 50)
print("FERTILIZER CLASS DISTRIBUTION:")
print("=" * 50)
print(df['Fertilizer Name'].value_counts())

print("\n" + "=" * 50)
print("SOIL TYPE VALUES:", df['Soil Type'].unique())
print("CROP TYPE VALUES:", df['Crop Type'].unique())