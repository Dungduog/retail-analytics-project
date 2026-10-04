"""Các kiểm tra đã có cho cleaned data và RFM output."""

from __future__ import annotations

from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd


def validate_results(
    cleaned_file: Union[str, Path],
    customer_file: Union[str, Path],
) -> dict[str, int]:
    """Chạy các kiểm tra chất lượng và trả về số lỗi của từng kiểm tra."""
    cleaned = pd.read_csv(cleaned_file, parse_dates=["InvoiceDate"])
    segments = pd.read_csv(customer_file)
    cancelled = cleaned["IsCancelled"].astype(str).str.lower().eq("true")

    expected_revenue = cleaned["Quantity"] * cleaned["UnitPrice"]
    expected_month = cleaned["InvoiceDate"].dt.to_period("M").astype(str)

    checks = {
        "duplicate_rows": int(cleaned.duplicated().sum()),
        "invalid_unit_price": int((cleaned["UnitPrice"] <= 0).sum()),
        "negative_quantity_not_cancelled": int(
            ((cleaned["Quantity"] < 0) & (~cancelled)).sum()
        ),
        "invalid_cancellation_flag": int(
            (cancelled & ~cleaned["InvoiceNo"].astype(str).str.startswith("C")).sum()
        ),
        "wrong_revenue": int((~np.isclose(cleaned["Revenue"], expected_revenue)).sum()),
        "wrong_order_month": int((cleaned["OrderMonth"] != expected_month).sum()),
        "missing_customer_id_in_segments": int(segments["CustomerID"].isna().sum()),
        "duplicate_customer_id": int(segments["CustomerID"].duplicated().sum()),
        "negative_recency": int((segments["Recency"] < 0).sum()),
        "non_positive_frequency": int((segments["Frequency"] <= 0).sum()),
    }

    for column in ["R_Score", "F_Score", "M_Score"]:
        checks[f"invalid_{column.lower()}"] = int(
            (~segments[column].isin([1, 2, 3, 4])).sum()
        )

    checks["inconsistent_frequency_score"] = int(
        (segments.groupby("Frequency")["F_Score"].nunique() > 1).sum()
    )
    checks["inconsistent_recency_score"] = int(
        (segments.groupby("Recency")["R_Score"].nunique() > 1).sum()
    )

    print("Validation results:")
    for name, count in checks.items():
        print(f"- {name}: {count}")
    return checks

