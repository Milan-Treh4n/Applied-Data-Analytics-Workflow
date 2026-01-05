"""
Cleaning pipeline for Business Survival (2022 cohort).
"""

from pathlib import Path
import pandas as pd


def clean_survival_2022(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().dropna(how="all").iloc[:, :5]
    df = df[df.iloc[:, 0].notna()]

    df.columns = [
        "code",
        "region",
        "births_2022",
        "one_year_survivals",
        "one_year_survival_rate",
    ]

    df = df[df["region"].notna()]
    df = df[df["code"] != "Code"]

    # Clean numeric formatting
    for col in ["births_2022", "one_year_survivals", "one_year_survival_rate"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace(":", "", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["births_2022"]).reset_index(drop=True)

    # Professional Titles
    return df.rename(
        columns={
            "code": "Geography Code",
            "region": "Geography Name",
            "births_2022": "Number of Business Births (2022)",
            "one_year_survivals": "Number Still Alive After 1 Year",
            "one_year_survival_rate": "1-Year Survival Rate (%)",
        }
    )


def save_survival_2022(df: pd.DataFrame, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    raw_path = PROJECT_ROOT / "data" / "raw" / "business_survival_2022.csv"
    out_path = PROJECT_ROOT / "data" / "processed" / "business_survival_2022_clean.csv"

    raw_df = pd.read_csv(raw_path)
    clean_df = clean_survival_2022(raw_df)
    save_survival_2022(clean_df, out_path)

    print("Saved:", out_path)


