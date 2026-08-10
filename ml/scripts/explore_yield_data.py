import pandas as pd

df = pd.read_csv("../datasets/raw/yield_df.csv")

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
print(f"UNIQUE AREAS (countries): {df['Area'].nunique()}")
print(df['Area'].unique()[:15], "...")

print(f"\nUNIQUE CROPS (Item): {df['Item'].nunique()}")
print(df['Item'].unique())

print(f"\nYEAR RANGE: {df['Year'].min()} to {df['Year'].max()}")

print("\nYIELD STATISTICS:")
print(df['hg/ha_yield'].describe())