
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

print("Starting visualization...")

file_path = Path("cleaned_books_dataset.csv")
print("Dataset exists:", file_path.exists())

df = pd.read_csv(file_path)
prices = pd.to_numeric(df["Price (£)"], errors="coerce").dropna()

print("Valid prices:", len(prices))

plt.figure(figsize=(9, 5))
plt.hist(prices, bins=10, edgecolor="black")
plt.title("Distribution of Book Prices")
plt.xlabel("Price (£)")
plt.ylabel("Number of Books")
plt.tight_layout()

output_file = Path("book_price_distribution.png").resolve()
plt.savefig(output_file, dpi=300)
plt.close()

print("Chart saved to:", output_file)
