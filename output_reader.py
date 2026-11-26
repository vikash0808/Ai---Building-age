"""Reader and statistical summarizer for EnergyPlus simulation CSV outputs."""

import csv
from pathlib import Path
from typing import Any, Dict, List

try:
    import pandas as pd
except ImportError:  # pragma: no cover - falls back cleanly to Python stdlib csv
    pd = None  # type: ignore


def read_csv(output_folder: str, filename: str = "eplusout.csv") -> Any:
    """Read an EnergyPlus output CSV as a Pandas DataFrame (or list of dicts fallback)."""
    csv_path = Path(output_folder) / filename
    if not csv_path.exists():
        raise FileNotFoundError(f"Simulation output CSV not found: {csv_path}")

    if pd is not None:
        return pd.read_csv(csv_path)

    with open(csv_path, "r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def summarize(data: Any) -> Dict[str, Any]:
    """Compute row count, column names, and numeric summary metrics (min, max, mean)."""
    if pd is not None and isinstance(data, pd.DataFrame):
        numeric_summary: Dict[str, Dict[str, float]] = {}
        for col in data.select_dtypes(include="number").columns:
            series = data[col].dropna()
            if len(series) > 0:
                numeric_summary[col] = {
                    "count": int(len(series)),
                    "min": round(float(series.min()), 4),
                    "max": round(float(series.max()), 4),
                    "mean": round(float(series.mean()), 4),
                }
        return {
            "rows": int(len(data)),
            "columns": list(data.columns),
            "numeric_summary": numeric_summary,
        }

    rows: List[Dict[str, Any]] = list(data)
    columns = list(rows[0].keys()) if rows else []
    numeric_summary = {}

    for col in columns:
        nums: List[float] = []
        for row in rows:
            raw = row.get(col)
            if raw is None or str(raw).strip() == "":
                continue
            try:
                nums.append(float(raw))
            except (TypeError, ValueError):
                nums = []
                break
        if nums:
            numeric_summary[col] = {
                "count": len(nums),
                "min": round(min(nums), 4),
                "max": round(max(nums), 4),
                "mean": round(sum(nums) / len(nums), 4),
            }

    return {
        "rows": len(rows),
        "columns": columns,
        "numeric_summary": numeric_summary,
    }
