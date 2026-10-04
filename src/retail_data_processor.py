"""Pipeline load, cleaning, revenue analysis và RFM segmentation."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import numpy as np
import pandas as pd

from .utils import (
    assign_rfm_segment,
    calculate_revenue,
    get_order_month,
    is_cancelled,
)


class RetailDataProcessor:
    """Đóng gói pipeline xử lý dataset UCI Online Retail."""

    REQUIRED_COLUMNS = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
    ]

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)
        self.raw_data: Optional[pd.DataFrame] = None
        self.df: Optional[pd.DataFrame] = None

    def load_data(self, sheet_name: Union[str, int] = 0) -> pd.DataFrame:
        """Đọc Excel/CSV và kiểm tra các cột bắt buộc."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Không tìm thấy file dữ liệu: {self.file_path}")

        suffix = self.file_path.suffix.lower()
        if suffix == ".xlsx":
            data = pd.read_excel(
                self.file_path,
                sheet_name=sheet_name,
                engine="openpyxl",
            )
        elif suffix == ".csv":
            data = pd.read_csv(self.file_path, encoding="ISO-8859-1")
        else:
            raise ValueError("Chỉ hỗ trợ file .xlsx hoặc .csv")

        missing_columns = [
            column for column in self.REQUIRED_COLUMNS if column not in data.columns
        ]
        if missing_columns:
            raise ValueError(f"Dữ liệu thiếu các cột bắt buộc: {missing_columns}")

        self.raw_data = data
        print(f"Loaded: {len(data):,} rows")
        return data

    def clean_data(self) -> pd.DataFrame:
        """Áp dụng các quy tắc cleaning đã thống nhất trong báo cáo."""
        if self.raw_data is None:
            raise RuntimeError("Phải gọi load_data() trước khi clean_data().")

        data = self.raw_data.drop_duplicates().copy()
        data = data[data["UnitPrice"] > 0].copy()

        data["IsCancelled"] = data["InvoiceNo"].apply(is_cancelled)

        invalid_quantity = (data["Quantity"] < 0) & (~data["IsCancelled"])
        data = data[~invalid_quantity].copy()

        data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"])
        data["OrderMonth"] = data["InvoiceDate"].apply(get_order_month)
        data["Revenue"] = calculate_revenue(
            data["Quantity"],
            data["UnitPrice"],
        )

        self.df = data.reset_index(drop=True)
        print(f"After cleaning: {len(self.df):,} rows")
        return self.df

    def _require_clean_data(self) -> pd.DataFrame:
        if self.df is None:
            raise RuntimeError("Phải gọi clean_data() trước bước phân tích.")
        return self.df

    def create_basic_structures(self):
        """Minh họa List, Dict, Set và Tuple bằng dữ liệu đã làm sạch."""
        data = self._require_clean_data()

        invoice_records = data.head(10).to_dict("records")
        sales = data[~data["IsCancelled"]]
        country_summary = sales.groupby("Country")["Revenue"].sum().to_dict()
        product_codes = set(data["StockCode"].astype(str))
        date_range = (data["InvoiceDate"].min(), data["InvoiceDate"].max())

        return invoice_records, country_summary, product_codes, date_range

    def analyze_revenue(self):
        """Tổng hợp gross sales theo tháng, quốc gia và sản phẩm."""
        data = self._require_clean_data()
        sales = data[~data["IsCancelled"]].copy()

        revenue_by_month = sales.groupby("OrderMonth")["Revenue"].sum()
        revenue_by_country = (
            sales.groupby("Country")["Revenue"].sum().sort_values(ascending=False)
        )
        revenue_by_product = (
            sales.groupby(["StockCode", "Description"])["Revenue"]
            .sum()
            .sort_values(ascending=False)
        )

        return revenue_by_month, revenue_by_country, revenue_by_product

    def create_customer_segments(self) -> pd.DataFrame:
        """Tạo bảng RFM, trong đó Monetary đã trừ giá trị cancellation."""
        data = self._require_clean_data()
        customer_data = data[data["CustomerID"].notna()].copy()
        sales = customer_data[~customer_data["IsCancelled"]].copy()

        reference_date = sales["InvoiceDate"].max() + pd.Timedelta(days=1)
        rfm = (
            sales.groupby("CustomerID")
            .agg(
                Recency=(
                    "InvoiceDate",
                    lambda values: (reference_date - values.max()).days,
                ),
                Frequency=("InvoiceNo", "nunique"),
                GrossMonetary=("Revenue", "sum"),
            )
            .reset_index()
        )

        cancellations = customer_data[customer_data["IsCancelled"]]
        cancelled_value = (
            cancellations.groupby("CustomerID")["Revenue"]
            .sum()
            .abs()
            .rename("CancelledValue")
            .reset_index()
        )

        rfm = rfm.merge(cancelled_value, on="CustomerID", how="left")
        rfm["CancelledValue"] = rfm["CancelledValue"].fillna(0)
        rfm["Monetary"] = rfm["GrossMonetary"] - rfm["CancelledValue"]

        r_percentile = rfm["Recency"].rank(method="average", pct=True)
        rfm["R_Score"] = (5 - np.ceil(r_percentile * 4)).astype(int)

        f_percentile = rfm["Frequency"].rank(method="average", pct=True)
        rfm["F_Score"] = np.ceil(f_percentile * 4).clip(1, 4).astype(int)

        m_percentile = rfm["Monetary"].rank(method="average", pct=True)
        rfm["M_Score"] = np.ceil(m_percentile * 4).clip(1, 4).astype(int)

        rfm["Segment"] = rfm.apply(
            lambda row: assign_rfm_segment(
                row["R_Score"],
                row["F_Score"],
                row["M_Score"],
            ),
            axis=1,
        )
        return rfm

    def export_results(
        self,
        cleaned_file: Union[str, Path],
        customer_file: Union[str, Path],
        customer_segments: Optional[pd.DataFrame] = None,
    ) -> None:
        """Xuất dữ liệu sạch và customer segments."""
        data = self._require_clean_data()
        cleaned_path = Path(cleaned_file)
        customer_path = Path(customer_file)
        cleaned_path.parent.mkdir(parents=True, exist_ok=True)
        customer_path.parent.mkdir(parents=True, exist_ok=True)

        data.to_csv(cleaned_path, index=False)
        if customer_segments is None:
            customer_segments = self.create_customer_segments()
        customer_segments.to_csv(customer_path, index=False)

        print(f"Exported: {cleaned_path}")
        print(f"Exported: {customer_path}")

