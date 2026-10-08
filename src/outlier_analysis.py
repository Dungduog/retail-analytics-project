"""Phân tích outlier bằng NumPy và phương pháp IQR."""

from __future__ import annotations

from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd


def analyze_outliers(
    input_file: Union[str, Path],
    summary_file: Union[str, Path],
    outlier_file: Union[str, Path],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Phân tích Revenue, Quantity và UnitPrice trên normal sales."""
    data = pd.read_csv(input_file)
    cancelled = data["IsCancelled"].astype(str).str.lower().eq("true")
    sales = data[~cancelled].copy()

    summary_results = []
    all_outliers = []

    for column in ["Revenue", "Quantity", "UnitPrice"]:
        values = sales[column].to_numpy()
        mean = np.mean(values)
        median = np.median(values)
        std = np.std(values)
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = sales[
            (sales[column] < lower_bound) | (sales[column] > upper_bound)
        ].copy()

        summary_results.append(
            {
                "Column": column,
                "Mean": mean,
                "Median": median,
                "Std": std,
                "Q1_25Percent": q1,
                "Q3_75Percent": q3,
                "IQR": iqr,
                "LowerBound": lower_bound,
                "UpperBound": upper_bound,
                "OutlierCount": len(outliers),
                "OutlierPercent": len(outliers) / len(sales) * 100,
            }
        )

        outliers["OutlierColumn"] = column
        outliers["OutlierValue"] = outliers[column]
        outliers["LowerBound"] = lower_bound
        outliers["UpperBound"] = upper_bound
        all_outliers.append(outliers)

        print(f"{column}: {len(outliers):,} outliers")

    summary = pd.DataFrame(summary_results)
    details = pd.concat(all_outliers, ignore_index=True)

    summary_path = Path(summary_file)
    details_path = Path(outlier_file)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    details_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(summary_path, index=False)
    details.to_csv(details_path, index=False)

    return summary, details

