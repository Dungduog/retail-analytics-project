"""
RetailDataProcessor
--------------------
Class trung tâm của pipeline cho dự án "Phân tích khách hàng và sản phẩm
trong bán lẻ online" (PSD301M).

Luồng xử lý đầy đủ (4 tuần):
    load_data() -> clean_data() -> analyze_revenue() -> export_results()

Tuần 1: chỉ triển khai load_data(). Các method còn lại được khai báo sẵn
(raise NotImplementedError) để main.py và notebook có thể import class này
ngay từ bây giờ mà không bị lỗi, và cả nhóm biết rõ còn thiếu gì.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import pandas as pd

# Hỗ trợ cả 2 cách chạy: `python src/retail_data_processor.py` (script độc lập)
# và `from src.retail_data_processor import RetailDataProcessor` (import như package,
# ví dụ từ notebook ở notebooks/ hoặc từ main.py ở thư mục gốc).
try:
    from .utils import calculate_revenue, is_cancelled_invoice, extract_order_month
except ImportError:
    from utils import calculate_revenue, is_cancelled_invoice, extract_order_month


class RetailDataProcessor:
    """
    Đóng gói toàn bộ pipeline xử lý dữ liệu bán lẻ UCI Online Retail.

    Thuộc tính
    ----------
    file_path : Path
        Đường dẫn tới file dữ liệu gốc (.xlsx hoặc .csv).
    raw_data : pd.DataFrame | None
        Dữ liệu thô sau khi load_data() chạy xong. None nếu chưa load.
    clean_data_ : pd.DataFrame | None
        Dữ liệu đã làm sạch (BAO GỒM cả hóa đơn hủy, đánh dấu qua cột
        IsCancelled — xem get_cancelled_orders() nếu cần lọc riêng).
    """

    # Các cột bắt buộc phải có trong dataset UCI Online Retail.
    # Dùng để validate ngay sau khi đọc file, tránh lỗi âm thầm ở các bước sau.
    REQUIRED_COLUMNS = [
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "UnitPrice", "CustomerID", "Country",
    ]

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)
        self.raw_data: Optional[pd.DataFrame] = None
        self.clean_data_: Optional[pd.DataFrame] = None

    # ------------------------------------------------------------------
    # TUẦN 1 — load_data()
    # ------------------------------------------------------------------
    def load_data(self, sheet_name: Union[str, int] = 0) -> pd.DataFrame:
        """
        Đọc file dữ liệu gốc (Excel hoặc CSV) vào self.raw_data.

        Parameters
        ----------
        sheet_name : str | int, default 0
            Tên hoặc index sheet cần đọc (chỉ áp dụng cho file .xlsx).

        Returns
        -------
        pd.DataFrame
            Dữ liệu thô vừa đọc được (cũng được lưu vào self.raw_data).

        Raises
        ------
        FileNotFoundError
            Nếu không tìm thấy file tại self.file_path.
        ValueError
            Nếu định dạng file không được hỗ trợ, hoặc dữ liệu thiếu cột bắt buộc.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Không tìm thấy file dữ liệu tại: {self.file_path}\n"
                f"→ Kiểm tra lại đường dẫn, hoặc đặt file vào data/raw/ theo đúng cấu trúc đã thống nhất."
            )

        suffix = self.file_path.suffix.lower()

        if suffix == ".xlsx":
            df = pd.read_excel(self.file_path, sheet_name=sheet_name, engine="openpyxl")
        elif suffix == ".csv":
            # Dataset UCI gốc khi xuất sang .csv thường dùng encoding ISO-8859-1,
            # đọc bằng utf-8 mặc định sẽ báo lỗi UnicodeDecodeError.
            df = pd.read_csv(self.file_path, encoding="ISO-8859-1")
        else:
            raise ValueError(
                f"Định dạng file '{suffix}' chưa được hỗ trợ. Chỉ hỗ trợ .xlsx hoặc .csv."
            )

        self._validate_columns(df)

        self.raw_data = df
        print(f"✅ load_data() thành công: {df.shape[0]:,} dòng, {df.shape[1]} cột.")
        return self.raw_data

    def _validate_columns(self, df: pd.DataFrame) -> None:
        """Kiểm tra dataframe có đủ các cột bắt buộc của UCI Online Retail không."""
        missing = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            raise ValueError(
                f"Dữ liệu thiếu các cột bắt buộc: {missing}\n"
                f"→ Kiểm tra lại file gốc có đúng định dạng UCI Online Retail không."
            )

    # ------------------------------------------------------------------
    # TUẦN 2 — clean_data()
    # ------------------------------------------------------------------
    def clean_data(self) -> pd.DataFrame:
        """
        Làm sạch dữ liệu thô (self.raw_data) theo đúng pipeline 7.1–7.8 đã mô tả
        trong báo cáo Data Profiling & Cleaning của nhóm:

            7.1  Loại bỏ duplicate hoàn toàn (drop_duplicates)
            7.2  Loại UnitPrice <= 0 khỏi dataset chính
            7.3  Đánh dấu cancellation -> cột IsCancelled (True/False), GIỮ LẠI
                 trong cùng dataset (không tách riêng) để phục vụ phân tích hoàn trả
            7.4  Xử lý Quantity theo 3 nhánh:
                   - Quantity > 0                        -> giữ (bán hàng bình thường)
                   - Quantity < 0 và IsCancelled = True   -> giữ (cancellation hợp lệ)
                   - Quantity < 0 và IsCancelled = False  -> loại (lỗi/điều chỉnh nội bộ)
                   - Quantity == 0 (hiếm/không xảy ra trên dataset thật) -> loại,
                     vì không khớp cả 2 trường hợp hợp lệ ở trên
            7.5  Giữ nguyên missing CustomerID (KHÔNG xóa, KHÔNG thay giá trị) —
                 các dòng này vẫn hữu ích cho phân tích doanh thu/sản phẩm, chỉ bị
                 loại khi làm RFM ở Tuần 3 (RFM cần gắn với từng khách hàng cụ thể)
            7.6  Convert InvoiceDate -> datetime
            7.7  Tạo OrderMonth dạng "YYYY-MM"
            7.8  Tạo Revenue = Quantity × UnitPrice (âm với cancellation — đúng ý nghĩa
                 phần doanh thu bị hoàn trả/hủy)

        Returns
        -------
        pd.DataFrame
            Dữ liệu đã làm sạch — BAO GỒM cả hóa đơn hủy (đánh dấu IsCancelled=True).
            Cũng được lưu vào self.clean_data_.

        Raises
        ------
        RuntimeError
            Nếu chưa gọi load_data() trước đó.
        """
        if self.raw_data is None:
            raise RuntimeError("Phải gọi load_data() trước khi gọi clean_data().")

        df = self.raw_data.copy()
        rows_raw = len(df)

        # 7.1 — Loại bỏ duplicate hoàn toàn (toàn bộ cột giống hệt nhau)
        df = df.drop_duplicates()
        rows_removed_duplicates = rows_raw - len(df)

        # 7.2 — Loại UnitPrice <= 0 khỏi dataset chính (áp dụng cho MỌI dòng,
        # kể cả dòng sẽ là cancellation, đúng theo báo cáo — không có ngoại lệ)
        rows_before_price = len(df)
        df = df[df["UnitPrice"] > 0]
        rows_removed_price = rows_before_price - len(df)

        # 7.3 — Đánh dấu cancellation bằng hàm cơ bản is_cancelled_invoice(),
        # GIỮ NGUYÊN trong df chính (không tách bảng riêng)
        df["IsCancelled"] = df["InvoiceNo"].astype(str).apply(is_cancelled_invoice)

        # 7.4 — Xử lý Quantity theo 3 nhánh
        valid_normal_sale = df["Quantity"] > 0
        valid_cancellation = (df["Quantity"] < 0) & (df["IsCancelled"])
        rows_before_qty = len(df)
        df = df[valid_normal_sale | valid_cancellation]
        rows_removed_quantity = rows_before_qty - len(df)

        # 7.5 — Missing CustomerID: không xử lý gì cả, giữ nguyên NaN
        missing_customer_count = df["CustomerID"].isna().sum()

        # 7.6 — Chuẩn hóa InvoiceDate sang datetime
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

        # 7.7 — Tạo OrderMonth dạng "YYYY-MM" — dùng lại hàm cơ bản extract_order_month()
        df["OrderMonth"] = df["InvoiceDate"].apply(extract_order_month)

        # 7.8 — Tạo Revenue = Quantity x UnitPrice — dùng lại hàm cơ bản calculate_revenue()
        df["Revenue"] = df.apply(lambda row: calculate_revenue(row.to_dict()), axis=1)

        self.clean_data_ = df.reset_index(drop=True)

        print("✅ clean_data() hoàn tất:")
        print(f"   - Dòng raw ban đầu: {rows_raw:,}")
        print(f"   - Loại do duplicate (7.1): {rows_removed_duplicates:,}")
        print(f"   - Loại do UnitPrice <= 0 (7.2): {rows_removed_price:,}")
        print(f"   - Loại do Quantity < 0 nhưng không phải cancellation (7.4): {rows_removed_quantity:,}")
        print(f"   - CustomerID thiếu, giữ nguyên NaN (7.5): {missing_customer_count:,}")
        print(f"   - Trong đó hóa đơn hủy (IsCancelled=True) được GIỮ LẠI: {int(self.clean_data_['IsCancelled'].sum()):,}")
        print(f"   - Dữ liệu sạch cuối cùng (clean_data_): {len(self.clean_data_):,} dòng")
        return self.clean_data_

    def get_cancelled_orders(self) -> pd.DataFrame:
        """
        Trả về (view lọc, không copy riêng dữ liệu) các dòng cancellation trong
        clean_data_ — tiện dùng khi cần phân tích riêng phần hoàn trả/hủy, mà
        không phải lưu trùng dữ liệu như thiết kế cũ (self.cancelled_orders_).
        """
        if self.clean_data_ is None:
            raise RuntimeError("Phải gọi clean_data() trước khi gọi get_cancelled_orders().")
        return self.clean_data_[self.clean_data_["IsCancelled"]]

    def analyze_revenue(self) -> dict:
        """(Tuần 3) Phân tích doanh thu theo tháng/quốc gia/sản phẩm + tính RFM."""
        raise NotImplementedError("analyze_revenue() sẽ được triển khai ở Tuần 3.")

    def export_results(self, output_dir: Union[str, Path] = "data/processed") -> None:
        """(Tuần 4) Xuất cleaned_retail.csv và customer_segments.csv."""
        raise NotImplementedError("export_results() sẽ được triển khai ở Tuần 4.")


# ----------------------------------------------------------------------
# Self-test: chạy trực tiếp file này (từ thư mục gốc dự án) để kiểm tra
# load_data() hoạt động đúng với file thật của nhóm.
#   python3 src/retail_data_processor.py
# ----------------------------------------------------------------------
if __name__ == "__main__":
    processor = RetailDataProcessor("data/raw/Online_Retail.xlsx")
    processor.load_data()

    cleaned = processor.clean_data()

    print("\n--- 5 dòng đầu tiên của dữ liệu sạch (clean_data_) ---")
    print(cleaned.head())

    print("\n--- Kiểm tra nhanh cột mới (10 dòng đầu) ---")
    print(cleaned[["InvoiceNo", "IsCancelled", "CustomerID", "OrderMonth", "Revenue"]].head(10))

    cancelled = processor.get_cancelled_orders()
    print(f"\n--- Các dòng cancellation vẫn còn trong clean_data_: {len(cancelled):,} dòng (xem 10 dòng đầu) ---")
    print(cancelled.head(10))
