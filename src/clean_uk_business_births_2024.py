"""
Cleaning pipeline for UK Business Births 2024 dataset.

Source: ONS Business Demography 2024 (Table 1.1d)
Outputs a clean table with clear readable column titles.
"""

from pathlib import Path
import pandas as pd


def load_births_2024(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_births_2024(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Drop fully empty rows
    df = df.dropna(how="all")

    # Keep only useful columns (first 3 meaningful columns)
    df = df.iloc[:, :3]

    # Drop top metadata rows (keep rows starting with region codes or names)
    df = df[df.iloc[:, 0].notna()]

    # Rename to temporary logical names
    df.columns = ["code", "region", "births_2024"]

    # Remove weird rows like headers inside table
    df = df[df["region"].notna()]
    df = df[df["code"] != "Code"]

    # Clean numeric formatting
    df["births_2024"] = (
        df["births_2024"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace(":", "", regex=False)
    )
    df["births_2024"] = pd.to_numeric(df["births_2024"], errors="coerce")

    # Final reset
    df = df.dropna(subset=["births_2024"]).reset_index(drop=True)

    # Professional Column Titles
   
    df = df.rename(
        columns={
            "code": "Geography Code",
            "region": "Geography Name",
            "births_2024": "Number of Business Births (2024)"
        }
    )

    return df


def save_births_2024(df: pd.DataFrame, output_path: str | Path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    raw = PROJECT_ROOT / "data" / "raw" / "uk_business_births_2024.csv"
    out = PROJECT_ROOT / "data" / "processed" / "uk_business_births_2024_clean.csv"

    raw_df = load_births_2024(raw)
    clean_df = clean_births_2024(raw_df)
    save_births_2024(clean_df, out)

    print("Saved:", out)
