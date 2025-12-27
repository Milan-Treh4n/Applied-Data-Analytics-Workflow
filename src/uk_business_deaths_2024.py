"""
Cleaning pipeline for UK Business Deaths 2024 dataset.

Source: ONS Business Demography 2024 (Table 2.1d)
Outputs a clean dataset with clear readable column titles.
"""

from pathlib import Path
import pandas as pd


def load_deaths_2024(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_deaths_2024(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Drop empty rows
    df = df.dropna(how="all")

    # Keep only first 3 useful columns
    df = df.iloc[:, :3]

    # Remove metadata + blank region rows
    df = df[df.iloc[:, 0].notna()]

    # Rename temp headers
    df.columns = ["code", "region", "deaths_2024"]

    # Remove internal header junk
    df = df[df["region"].notna()]
    df = df[df["code"] != "Code"]

    # Clean numeric values
    df["deaths_2024"] = (
        df["deaths_2024"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace(":", "", regex=False)
    )

    df["deaths_2024"] = pd.to_numeric(df["deaths_2024"], errors="coerce")

    df = df.dropna(subset=["deaths_2024"]).reset_index(drop=True)
    
    # Professional Column Titles
 
    df = df.rename(
        columns={
            "code": "Geography Code",
            "region": "Geography Name",
            "deaths_2024": "Number of Business Deaths (2024)"
        }
    )

    return df


def save_deaths_2024(df: pd.DataFrame, output_path: str | Path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    raw = PROJECT_ROOT / "data" / "raw" / "uk_business_deaths_2024.csv"
    out = PROJECT_ROOT / "data" / "processed" / "uk_business_deaths_2024_clean.csv"

    raw_df = load_deaths_2024(raw)
    clean_df = clean_deaths_2024(raw_df)
    save_deaths_2024(clean_df, out)

    print("Saved:", out)
