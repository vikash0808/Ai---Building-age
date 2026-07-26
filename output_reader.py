from pathlib import Path
import pandas as pd

def read_csv(output_folder:str):
    csv=Path(output_folder)/"eplusout.csv"
    if not csv.exists():
        raise FileNotFoundError(csv)
    return pd.read_csv(csv)

def summarize(df):
    return {
        "rows":len(df),
        "columns":list(df.columns),
        "numeric_summary":df.describe(include="all").to_dict()
    }
