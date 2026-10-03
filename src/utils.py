"""
utils.py
--------
4 hàm cơ bản (Built-in Data Structures) cho dự án "Phân tích khách hàng và
sản phẩm trong bán lẻ online" (PSD301M) — Tuần 2, phụ trách: Trí Dũng.

Đây là các PURE FUNCTION: nhận input -> trả output, không phụ thuộc state
của class nào cả, nên có thể test độc lập và tái sử dụng ở nhiều nơi
(RetailDataProcessor.clean_data(), notebook EDA, main.py...).

Ngoài 4 hàm chính, file còn minh họa đúng yêu cầu cấu trúc dữ liệu của đề bài:
    - list  : chứa các invoice records  -> tham số `records: List[dict]`
    - dict  : tổng hợp country summary  -> summarize_revenue_by_country()
    - set   : lấy unique product codes  -> get_unique_product_codes()
    - tuple : lưu cấu hình date range   -> DATE_RANGE_CONFIG
"""

from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple, Union

import pandas as pd

# ----------------------------------------------------------------------
# TUPLE — cấu hình date range của dataset UCI Online Retail.
# Dùng tuple vì đây là cấu hình cố định, không nên bị chỉnh sửa (immutable).
# ----------------------------------------------------------------------
DATE_RANGE_CONFIG: Tuple[str, str] = ("2010-12-01", "2011-12-09")


# ----------------------------------------------------------------------
# HÀM CƠ BẢN 1 — tính doanh thu từ record
# ----------------------------------------------------------------------
def calculate_revenue(record: Dict[str, Any]) -> float:
    """
    Tính doanh thu từ một record (dict) đại diện cho 1 dòng hóa đơn.

    Revenue = Quantity * UnitPrice

    Parameters
    ----------
    record : dict
        Phải có 2 khóa 'Quantity' và 'UnitPrice'.

    Returns
    -------
    float
        Doanh thu tính được. Trả về 0.0 nếu thiếu dữ liệu hoặc dữ liệu không hợp lệ.
    """
    quantity = record.get("Quantity", 0)
    unit_price = record.get("UnitPrice", 0)
    try:
        return float(quantity) * float(unit_price)
    except (TypeError, ValueError):
        return 0.0


# ----------------------------------------------------------------------
# HÀM CƠ BẢN 2 — nhận diện đơn hủy
# ----------------------------------------------------------------------
def is_cancelled_invoice(invoice_no: Union[str, int]) -> bool:
    """
    Kiểm tra một hóa đơn có bị hủy hay không, dựa trên quy ước của UCI dataset:
    mã InvoiceNo bắt đầu bằng ký tự 'C'.

    Parameters
    ----------
    invoice_no : str | int

    Returns
    -------
    bool
        True nếu là hóa đơn hủy, False nếu ngược lại.
    """
    return str(invoice_no).strip().upper().startswith("C")


# ----------------------------------------------------------------------
# HÀM CƠ BẢN 3 — bóc tách tháng đơn hàng
# ----------------------------------------------------------------------
def extract_order_month(invoice_date: Any) -> Union[str, None]:
    """
    Bóc tách tháng đặt hàng từ InvoiceDate, trả về chuỗi định dạng 'YYYY-MM'.

    Parameters
    ----------
    invoice_date : datetime-like | str | None
        Có thể là pandas.Timestamp, datetime.datetime, chuỗi ngày, hoặc NaT/None.

    Returns
    -------
    str | None
        Chuỗi 'YYYY-MM', hoặc None nếu invoice_date rỗng/không hợp lệ.
    """
    if invoice_date is None or (hasattr(pd, "isna") and pd.isna(invoice_date)):
        return None

    if isinstance(invoice_date, str):
        invoice_date = pd.to_datetime(invoice_date, errors="coerce")
        if pd.isna(invoice_date):
            return None

    return f"{invoice_date.year:04d}-{invoice_date.month:02d}"


# ----------------------------------------------------------------------
# HÀM CƠ BẢN 4 — gán nhãn phân khúc RFM đơn giản
# ----------------------------------------------------------------------
def assign_rfm_segment(recency_days: float, frequency: int, monetary: float) -> str:
    """
    Gán nhãn phân khúc khách hàng dựa trên 3 chỉ số RFM thô (rule-based,
    ngưỡng cố định) — dùng để demo ở Tuần 2.

    Ở Tuần 3, khi đã có đầy đủ dữ liệu toàn bộ khách hàng, nhóm có thể thay
    ngưỡng cố định này bằng ngưỡng tính theo quantile (vd: pd.qcut) để phân
    khúc công bằng hơn giữa các khách hàng.

    Parameters
    ----------
    recency_days : float
        Số ngày kể từ lần mua cuối cùng đến ngày chốt dữ liệu.
    frequency : int
        Tổng số hóa đơn/lần mua hàng.
    monetary : float
        Tổng số tiền đã chi tiêu.

    Returns
    -------
    str
        Một trong: "Champions", "Loyal Customers", "At Risk", "Lost".
    """
    if recency_days <= 30 and frequency >= 5 and monetary >= 1000:
        return "Champions"
    elif recency_days <= 90 and frequency >= 2:
        return "Loyal Customers"
    elif recency_days > 180:
        return "Lost"
    else:
        return "At Risk"


# ----------------------------------------------------------------------
# Hàm phụ trợ — minh họa thêm list / dict / set theo đúng yêu cầu đề bài
# (không bắt buộc, nhưng cho thấy cách 4 hàm trên phối hợp với nhau)
# ----------------------------------------------------------------------
def summarize_revenue_by_country(records: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Nhận một LIST các invoice records (list of dict), trả về một DICT
    tổng hợp doanh thu theo từng quốc gia.

    Minh họa: list chứa invoice records + dict để tổng hợp country summary.
    """
    summary: Dict[str, float] = {}
    for record in records:
        country = record.get("Country", "Unknown")
        revenue = calculate_revenue(record)
        summary[country] = summary.get(country, 0.0) + revenue
    return summary


def get_unique_product_codes(records: List[Dict[str, Any]]) -> Set[str]:
    """
    Nhận một LIST các invoice records, trả về một SET các StockCode duy nhất.

    Minh họa: set để lấy unique product codes.
    """
    return {record.get("StockCode") for record in records if record.get("StockCode")}


def dataframe_to_records(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Tiện ích: chuyển một DataFrame thành list of dict (invoice records)."""
    return df.to_dict(orient="records")


# ----------------------------------------------------------------------
# Self-test nhanh: chạy trực tiếp `python src/utils.py` để kiểm tra 4 hàm
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # --- Test calculate_revenue ---
    r1 = {"Quantity": 6, "UnitPrice": 2.55}
    assert abs(calculate_revenue(r1) - 15.3) < 1e-9, "calculate_revenue sai!"
    assert calculate_revenue({"Quantity": "x", "UnitPrice": 2}) == 0.0, "calculate_revenue phải trả 0.0 khi lỗi!"
    print("✅ calculate_revenue PASS:", calculate_revenue(r1))

    # --- Test is_cancelled_invoice ---
    assert is_cancelled_invoice("C536366") is True
    assert is_cancelled_invoice("536365") is False
    assert is_cancelled_invoice(536365) is False
    print("✅ is_cancelled_invoice PASS")

    # --- Test extract_order_month ---
    assert extract_order_month(pd.Timestamp("2010-12-01 08:26:00")) == "2010-12"
    assert extract_order_month("2011-03-15") == "2011-03"
    assert extract_order_month(None) is None
    assert extract_order_month(pd.NaT) is None
    print("✅ extract_order_month PASS")

    # --- Test assign_rfm_segment ---
    assert assign_rfm_segment(10, 8, 2000) == "Champions"
    assert assign_rfm_segment(60, 3, 500) == "Loyal Customers"
    assert assign_rfm_segment(200, 1, 50) == "Lost"
    assert assign_rfm_segment(100, 1, 100) == "At Risk"
    print("✅ assign_rfm_segment PASS")

    # --- Test cấu trúc list/dict/set/tuple ---
    sample_records = [
        {"InvoiceNo": "536365", "StockCode": "85123A", "Quantity": 6, "UnitPrice": 2.55, "Country": "United Kingdom"},
        {"InvoiceNo": "536365", "StockCode": "71053", "Quantity": 6, "UnitPrice": 3.39, "Country": "United Kingdom"},
        {"InvoiceNo": "536367", "StockCode": "85123A", "Quantity": 2, "UnitPrice": 2.55, "Country": "France"},
    ]
    country_summary = summarize_revenue_by_country(sample_records)
    unique_codes = get_unique_product_codes(sample_records)
    print("✅ summarize_revenue_by_country:", country_summary)
    print("✅ get_unique_product_codes:", unique_codes)
    print("✅ DATE_RANGE_CONFIG (tuple):", DATE_RANGE_CONFIG)

    print("\n🎉 Tất cả test PASS — utils.py sẵn sàng để clean_data() sử dụng.")
