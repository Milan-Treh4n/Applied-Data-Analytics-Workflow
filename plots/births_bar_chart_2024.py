import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Define project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

births_2019 = pd.read_csv(
    PROJECT_ROOT / "data" / "processed" / "uk_business_births_2019_clean.csv"
)
births_2024 = pd.read_csv(
    PROJECT_ROOT / "data" / "processed" / "uk_business_births_2024_clean.csv"
)

# Exclude top 4 non-regions
b19 = births_2019.sort_values("Number of Business Births (2019)", ascending=False).iloc[4:]
b24 = births_2024.sort_values("Number of Business Births (2024)", ascending=False).iloc[4:]

# Merge datasets on Geography Name
merged = b19[["Geography Name", "Number of Business Births (2019)"]].merge(
    b24[["Geography Name", "Number of Business Births (2024)"]],
    on="Geography Name",
    how="inner",
)

# top 15 by total births across both years
merged["Total"] = (
    merged["Number of Business Births (2019)"] +
    merged["Number of Business Births (2024)"]
)
merged = merged.sort_values("Total", ascending=False).head(15)

# Configure Plot
regions = merged["Geography Name"]
births19 = merged["Number of Business Births (2019)"]
births24 = merged["Number of Business Births (2024)"]

x = np.arange(len(regions))
width = 0.4

plt.figure(figsize=(12, 6))
plt.bar(x - width / 2, births19, width, label="2019", color='darkblue')
plt.bar(x + width / 2, births24, width, label="2024", color='skyblue')

plt.title("Business Births by Region – 2019 vs 2024 (Top 15 Regions)")
plt.xlabel("Region")
plt.ylabel("Number of Business Births")
plt.xticks(x, regions, rotation=45, ha="right")
plt.legend()
plt.tight_layout()

# Save Plot
plots = PROJECT_ROOT / "plots"
plots.mkdir(exist_ok=True)
out_path = plots / "business_births_2019_2024_comparison.png"
plt.savefig(out_path, dpi=300)
plt.show()

