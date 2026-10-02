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
        Dữ liệu đã làm sạch — sẽ được gán giá trị trong clean_data() ở Tuần 2.
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
        self.clean_data_: Optional[pd.DataFrame] = None  # dùng ở Tuần 2

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
    # Khung sườn cho Tuần 2–4 — chưa triển khai, để sẵn chữ ký method
    # ------------------------------------------------------------------
    def clean_data(self) -> pd.DataFrame:
        """(Tuần 2) Lọc Quantity/UnitPrice <= 0, xử lý hóa đơn hủy, missing CustomerID, tính Revenue."""
        raise NotImplementedError("clean_data() sẽ được triển khai ở Tuần 2.")

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
    df = processor.load_data()

    print("\n--- 5 dòng đầu tiên ---")
    print(df.head())

    print("\n--- Kiểu dữ liệu từng cột ---")
    print(df.dtypes)

    print("\n--- Số lượng giá trị thiếu theo cột ---")
    print(df.isna().sum())
