"""Các hàm cơ bản được sử dụng trong pipeline bán lẻ."""

from __future__ import annotations

from typing import Any


def calculate_revenue(quantity: Any, unit_price: Any) -> Any:
    """Tính Revenue = Quantity * UnitPrice cho scalar hoặc pandas Series."""
    return quantity * unit_price


def is_cancelled(invoice_no: Any) -> bool:
    """InvoiceNo bắt đầu bằng C được xem là cancellation."""
    return str(invoice_no).strip().upper().startswith("C")


def get_order_month(invoice_date: Any) -> str:
    """Chuyển InvoiceDate sang chuỗi YYYY-MM."""
    return invoice_date.strftime("%Y-%m")


def assign_rfm_segment(r_score: int, f_score: int, m_score: int) -> str:
    """Gán segment dựa trên ý nghĩa riêng của điểm R, F và M."""
    if r_score >= 3 and f_score >= 3 and m_score >= 3:
        return "Champions"
    if r_score <= 2 and (f_score >= 3 or m_score >= 3):
        return "At Risk"
    if f_score >= 3 and r_score >= 3:
        return "Loyal Customers"
    if r_score == 1 and f_score <= 2 and m_score <= 2:
        return "Lost"
    return "Regular Customers"

