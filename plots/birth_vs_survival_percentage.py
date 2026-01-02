import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load clean data
df = pd.read_csv(
    PROJECT_ROOT / "data" / "processed" / "business_survival_rates_2019_clean.csv"
)

# Column names
region_col = "Region"
one_year = "1-Year Survival Rate (2019 Cohort, %)"
five_year = "5-Year Survival Rate (2019 Cohort, %)"

# Keep relevant data
df = df[[region_col, one_year, five_year]].dropna()

# Remove total row and duplicates
df = df[df[region_col].str.lower() != "total"]
df = df.groupby(region_col, as_index=False).first()

# Sort by 1-year survival rate (cleaner flow)
df = df.sort_values(one_year, ascending=False)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(df[region_col], df[one_year], marker="o", label="1-Year Survival Rate", color="navy")
plt.plot(df[region_col], df[five_year], marker="o", label="5-Year Survival Rate", color="skyblue")

plt.title("Business Survival Rates by Region (2019 Cohort)")
plt.xlabel("Region")
plt.ylabel("Survival Rate (%)")
plt.xticks(rotation=45, ha="right")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save
plots = PROJECT_ROOT / "plots"
plots.mkdir(exist_ok=True)
out_path = plots / "business_survival_rates_2019_line.png"
plt.savefig(out_path, dpi=300)

# Show locally only
if os.environ.get("CI") != "true":
    plt.show()

print("Saved:", out_path)
