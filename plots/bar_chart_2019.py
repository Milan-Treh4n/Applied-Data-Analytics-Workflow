import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "uk_business_births_2019_clean.csv"
PLOTS_DIR = PROJECT_ROOT / "plots"

df = pd.read_csv(DATA_PATH)

# choose top 15 regions by births (or fewer if not enough rows)
top_n = min(15, len(df))
df_top = df.sort_values("Number of Business Births (2019)", ascending=False).head(top_n)

plt.figure(figsize=(10, 6))
plt.bar(df_top["Geography Name"], df_top["Number of Business Births (2019)"])
plt.xlabel("Region")
plt.ylabel("Number of Business Births")
plt.title(f"Top {top_n} Regions – Business Births in the UK (2019)")
plt.xticks(rotation=45)
plt.tight_layout()

PLOTS_DIR.mkdir(exist_ok=True)
plt.savefig(PLOTS_DIR / "business_births_top_regions_2019.png", dpi=300)
plt.show()

