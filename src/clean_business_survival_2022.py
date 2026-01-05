"""
Cleaning pipeline for Business Survival (2022 cohort).
"""
from pathlib import Path
import pandas as pd


def load_survival_2022(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_survival_2022(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Drop fully empty rows
    df = df.dropna(how="all")

    # Keep main useful columns only
    df = df.iloc[:, :5]

    # Remove metadata rows
    df = df[df.iloc[:, 0].notna()]

    # Temporary logical headers
    df.columns = [
        "code",
        "region",
        "births_2022",
        "one_year_survivals",
        "one_year_survival_rate"
    ]

    df = df[df["region"].notna()]
    df = df[df["code"] != "Code"]

    # Clean numeric formatting
    for col in ["births_2022", "one_year_survivals"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace(":", "", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Survival rate (percent)
    df["one_year_survival_rate"] = (
        df["one_year_survival_rate"]
        .astype(str)
        .str.replace(":", "", regex=False)
    )
    df["one_year_survival_rate"] = pd.to_numeric(
        df["one_year_survival_rate"], errors="coerce"
    )

    df = df.dropna(subset=["births_2022"]).reset_index(drop=True)

    # -----------------------
    # Professional Titles
    # -----------------------
    df = df.rename(
        columns={
            "code": "Geography Code",
            "region": "Geography Name",
            "births_2022": "Number of Business Births (2022)",
            "one_year_survivals": "Number Still Alive After 1 Year",
            "one_year_survival_rate": "1-Year Survival Rate (%)"
        }
    )

    return df


def save_survival_2022(df: pd.DataFrame, output_path: str | Path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    raw = PROJECT_ROOT / "data" / "raw" / "business_survival_2022.csv"
    out = PROJECT_ROOT / "data" / "processed" / "business_survival_2022_clean.csv"

    raw_df = load_survival_2022(raw)
    clean_df = clean_survival_2022(raw_df)
    save_survival_2022(clean_df, out)

    print("Saved:", out)
