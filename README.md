# Retail Analytics Project (PSD301M)

Phân tích khách hàng và sản phẩm trong bán lẻ online bằng dataset UCI Online Retail.

Phiên bản này kết hợp:

- logic cleaning, RFM, outlier và các kết quả đã chạy từ phiên bản phân tích;
- cấu trúc thư mục, đường dẫn tương đối, README và requirements từ phiên bản được tổ chức lại.

## Cấu trúc dự án

```text
project_fixed/
├── data/
│   ├── raw/
│   │   └── Online_Retail.xlsx
│   └── processed/
│       ├── cleaned_retail.csv
│       ├── customer_segments.csv
│       ├── outlier_summary.csv
│       └── outliers_detected.csv
├── notebooks/
│   └── NoteBook.md
├── src/
│   ├── __init__.py
│   ├── utils.py
│   ├── retail_data_processor.py
│   ├── outlier_analysis.py
│   └── validation.py
├── main.py
├── requirements.txt
└── README.md
```

## Phần đã triển khai

- Data profiling và quy tắc data cleaning.
- Loại exact duplicates.
- Loại `UnitPrice <= 0`.
- Giữ cancellation có `InvoiceNo` bắt đầu bằng `C`.
- Loại `Quantity < 0` nếu không phải cancellation.
- Giữ missing `CustomerID` trong transaction data và loại khỏi RFM.
- Tạo `OrderMonth`, `Revenue` và `IsCancelled`.
- Phân tích doanh thu theo tháng, quốc gia và sản phẩm.
- RFM customer segmentation.
- Thống kê NumPy và phát hiện outlier bằng IQR.
- Validation cho cleaned data và customer segments.

Chi tiết phương pháp và kết quả hiện tại nằm trong `notebooks/NoteBook.md`.

## Cài đặt

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Chạy pipeline

Từ thư mục gốc của project:

```bash
python main.py
```

Pipeline sẽ đọc `data/raw/Online_Retail.xlsx` và ghi lại bốn file trong
`data/processed/`.

## Trạng thái các yêu cầu còn lại

Các nội dung dưới đây có trong yêu cầu ban đầu nhưng chưa được triển khai trong
hai phiên bản nguồn, nên chưa được thêm vào project này:

- Jupyter Notebook `.ipynb` có code và output.
- Visualization bằng Matplotlib.
- Fake Store API.
- Web scraping Books to Scrape.
- EDA hoàn chỉnh trả lời tám câu hỏi nghiên cứu và phần kết luận cuối.

Không tạo file rỗng cho các phần trên. Chỉ bổ sung sau khi nhóm thống nhất phạm
vi và cách triển khai.

