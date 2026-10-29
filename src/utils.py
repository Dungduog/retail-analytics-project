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
    """Gán segment dựa trên ý nghĩa riêng của điểm R, F và M.

    Thứ tự kiểm tra quan trọng — điều kiện cụ thể hơn đứng trước:
      Champions     : gần đây + mua nhiều + chi nhiều
      Loyal Customers: gần đây + mua nhiều, nhưng monetary chưa đến ngưỡng top
      At Risk       : lâu không quay lại nhưng từng có frequency/monetary tốt
      Lost          : lâu không quay lại, frequency và monetary đều thấp
      Regular       : còn lại (mua gần đây nhưng ít lần / monetary thấp)
    """
    if r_score >= 3 and f_score >= 3 and m_score >= 3:
        return "Champions"
    if r_score >= 3 and f_score >= 3:
        return "Loyal Customers"          # r,f tốt nhưng m chưa đủ top
    if r_score <= 2 and (f_score >= 3 or m_score >= 3):
        return "At Risk"                  # lâu không quay lại, nhưng từng valuable
    if r_score <= 2 and f_score <= 2 and m_score <= 2:
        return "Lost"                     # r kém, f và m đều thấp
    return "Regular Customers"            # gần đây nhưng tần suất / giá trị thấp

