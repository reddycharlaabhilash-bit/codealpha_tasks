
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

print("Starting Exploratory Data Analysis...")

# File paths
input_file = Path("cleaned_books_dataset.csv")
output_file = Path("cleaned_books_dataset.csv")

# Check whether dataset exists
if not input_file.exists():
    raise FileNotFoundError(
        "cleaned_books_dataset.csv not found. "
        "Run scraper.py and prepare the cleaned dataset first."
    )

# Load dataset
df = pd.read_csv(input_file)

print("\n===== DATASET OVERVIEW =====")
print("Total records:", len(df))
print("Total columns:", len(df.columns))
print("\nColumn names:")
print(df.columns.tolist())

# Check required columns
required_columns = ["Title", "Price (£)", "Availability"]

missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

# Clean title and availability text
df["Title"] = df["Title"].astype("string").str.strip()
df["Availability"] = (
    df["Availability"].astype("string").str.strip()
)

# Convert price into numeric format
df["Price (£)"] = pd.to_numeric(
    df["Price (£)"]
    .astype("string")
    .str.replace("£", "", regex=False)
    .str.replace("Â", "", regex=False)
    .str.strip(),
    errors="coerce"
)

# Check and report missing values
print("\n===== MISSING VALUES BEFORE CLEANING =====")
print(df.isnull().sum())

# Remove duplicate records
duplicates = df.duplicated().sum()
print("\nDuplicate rows found:", duplicates)

df = df.drop_duplicates()

# Remove rows with missing essential information
df = df.dropna(
    subset=["Title", "Price (£)", "Availability"]
)

# Remove invalid prices
df = df[df["Price (£)"] >= 0]

# Save cleaned dataset
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\n===== CLEANING SUMMARY =====")
print("Records after cleaning:", len(df))
print("Records removed:", "Check original count above")

# Dataset structure and data types
print("\n===== DATA TYPES =====")
print(df.dtypes)

# Missing values after cleaning
print("\n===== MISSING VALUES AFTER CLEANING =====")
print(df.isnull().sum())

# Price analysis
prices = df["Price (£)"]

if prices.empty:
    raise ValueError("No valid book prices found in the dataset.")

print("\n===== PRICE STATISTICS =====")
print(prices.describe())

print("\nAverage price (£):", round(prices.mean(), 2))
print("Median price (£):", round(prices.median(), 2))
print("Minimum price (£):", round(prices.min(), 2))
print("Maximum price (£):", round(prices.max(), 2))
print("Unique prices:", prices.nunique())

# Lowest-priced books
print("\n===== FIVE LOWEST-PRICED BOOKS =====")
print(
    df.nsmallest(5, "Price (£)")[
        ["Title", "Price (£)"]
    ].to_string(index=False)
)

# Highest-priced books
print("\n===== FIVE HIGHEST-PRICED BOOKS =====")
print(
    df.nlargest(5, "Price (£)")[
        ["Title", "Price (£)"]
    ].to_string(index=False)
)

# Outlier detection using the IQR method
q1 = prices.quantile(0.25)
q3 = prices.quantile(0.75)
iqr = q3 - q1

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = df[
    (df["Price (£)"] < lower_bound)
    | (df["Price (£)"] > upper_bound)
]

print("\n===== OUTLIER ANALYSIS =====")
print("Lower bound (£):", round(lower_bound, 2))
print("Upper bound (£):", round(upper_bound, 2))
print("Potential price outliers:", len(outliers))

# Availability summary
print("\n===== AVAILABILITY SUMMARY =====")
print(df["Availability"].value_counts().to_string())

# Save price statistics to a CSV file
stats = prices.describe().rename_axis("Statistic").reset_index()
stats.to_csv(
    "price_statistics.csv",
    index=False,
    encoding="utf-8-sig"
)

# Create a box plot to inspect price spread and outliers
plt.figure(figsize=(9, 5))
plt.boxplot(prices, orientation="horizontal")
plt.title("Box Plot of Book Prices")
plt.xlabel("Price (£)")
plt.tight_layout()
plt.savefig("book_price_boxplot.png", dpi=300)
plt.close()

print("\n===== EDA COMPLETED =====")
print("Updated dataset: cleaned_books_dataset.csv")
print("Price statistics: price_statistics.csv")
print("Box plot: book_price_boxplot.png")
