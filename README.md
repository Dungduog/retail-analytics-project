# Retail Analytics Project (PSD301M)

Phân tích khách hàng và sản phẩm trong bán lẻ online — dataset UCI Online Retail.

## Setup nhanh
```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Cấu trúc thư mục
- `data/raw/` — dữ liệu gốc, không chỉnh sửa
- `data/processed/` — dữ liệu đã làm sạch (cleaned_retail.csv, customer_segments.csv)
- `src/` — class RetailDataProcessor + các hàm cơ bản
- `notebooks/` — Jupyter notebook phân tích EDA
- `reports/` — biểu đồ và báo cáo insight
- `main.py` — entry point chạy toàn bộ pipeline

## Chạy pipeline
```bash
python3 main.py
```
