# Retail Analytics Project (PSD301M)

Phân tích khách hàng và sản phẩm trong bán lẻ online bằng dataset UCI Online Retail.

Phiên bản này kết hợp:

- logic cleaning, RFM, outlier và các kết quả đã chạy từ phiên bản phân tích;
- cấu trúc thư mục, đường dẫn tương đối, README và requirements từ phiên bản được tổ chức lại.

## Cấu trúc dự án

```text
retail-analytics-project/
├── data/
│   ├── raw/
│   │   └── Online_Retail.xlsx
│   ├── external/
│   │   └── books_scraped.csv
│   └── processed/
│       ├── cleaned_retail.csv
│       ├── customer_segments.csv
│       ├── outlier_summary.csv
│       └── outliers_detected.csv
├── notebooks/
│   └── NoteBook.md
├── reports/
│   ├── eda_results.md
│   ├── figures/
│   └── tables/
├── src/
│   ├── __init__.py
│   ├── book_scraper.py
│   ├── eda_analysis.py
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
- EDA trả lời tám câu hỏi nghiên cứu bằng dữ liệu đã làm sạch.
- Biểu đồ doanh thu tháng, top sản phẩm, phân khúc giá, giá trị đơn hàng và quốc gia.
- Script Books to Scrape để thực hành HTTP GET, HTML, BeautifulSoup và pagination.

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
`data/processed/`, các bảng EDA trong `reports/tables/` và biểu đồ trong
`reports/figures/`.

## Thực hành web scraping

Chạy riêng từ thư mục gốc của project (cần Internet):

```bash
python src/book_scraper.py
```

Script theo liên kết `next` đến trang cuối, sau đó xuất
`data/external/books_scraped.csv`. Muốn chạy demo nhanh trên hai trang:

```bash
python src/book_scraper.py --max-pages 2
```

Cả hai lệnh ghi cùng một file CSV; bản demo thay thế kết quả đầy đủ bằng dữ liệu
của hai trang. Chạy lại lệnh không có `--max-pages` để lấy toàn bộ danh sách.
Đường dẫn output tính từ vị trí script nên không phụ thuộc thư mục terminal.

Các cột CSV: `Title`, `PriceGBP`, `Rating`, `Availability`, `ProductURL`,
`PageNumber`. Script lấy thông tin từ trang danh sách, không tải ảnh sản phẩm.

Quy trình: HTTP GET → kiểm tra status code → parse HTML → chọn thẻ →
đọc text/attributes → pagination → DataFrame → CSV.

| HTML / selector | Nội dung được đọc |
|---|---|
| `article.product_pod` | Khối của từng sản phẩm, lấy bằng `find_all()` |
| `h3 a` | Thuộc tính `title` chứa tên đầy đủ và `href` chứa link |
| `p.price_color` | Text giá, lấy bằng `find()` rồi chuyển thành số |
| `p.star-rating` | Thuộc tính `class` chứa mức rating One–Five |
| `p.instock.availability` | Text trạng thái tồn kho |
| `li.next a` | Thuộc tính `href` dẫn sang trang tiếp theo |

`select_one()` lấy thẻ đầu tiên khớp CSS selector; `get_text()` lấy nội dung chữ.
`urljoin()` chuyển link tương đối thành URL đầy đủ.
HTTP request có timeout 30 giây và kiểm tra lỗi bằng `raise_for_status()`.
Script chờ 0,5 giây giữa các trang và chỉ ghi CSV sau khi cào thành công.

Website là sandbox luyện scraping; giá và rating được gán ngẫu nhiên.
Dữ liệu sách phục vụ thực hành kỹ thuật, được lưu riêng với UCI Online Retail.
Pipeline `main.py` vẫn chạy độc lập với script này.

Tài liệu học:

- [Books to Scrape](https://books.toscrape.com/)
- [Thông tin sandbox](https://sites.toscrape.com/)
- [Requests Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/)
- [Beautiful Soup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Các phần còn lại

Các nội dung cần hoàn thiện cho bài nộp:

- Jupyter Notebook `.ipynb` có code và output.
- Phần kết luận cuối của toàn bộ project.
- Slide thuyết trình.

Fake Store API không nằm trong phạm vi yêu cầu của giảng viên theo thông tin nhóm cung cấp.

