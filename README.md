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
│   ├── eda_retail_analysis.ipynb
│   └── NoteBook.md
├── reports/
│   ├── eda_results.md
│   ├── insight_report.md
│   ├── figures/
│   └── tables/
├── src/
│   ├── __init__.py
│   ├── book_scraper.py
│   ├── build_web.py
│   ├── eda_analysis.py
│   ├── utils.py
│   ├── retail_data_processor.py
│   ├── outlier_analysis.py
│   └── validation.py
├── web/
│   ├── index.html
│   ├── data.js
│   └── assets/figures/
├── main.py
├── requirements.txt
└── README.md
```

## Phần đã triển khai

- **Data Profiling & Data Cleaning Pipeline:**
  - Chuẩn hóa kiểu dữ liệu (`StockCode` uppercase, cắt khoảng trắng chuỗi).
  - Loại bỏ 5,268 dòng duplicate hoàn toàn.
  - Loại bỏ 2,512 dòng `UnitPrice <= 0`.
  - Giữ lại cancellation có `InvoiceNo` bắt đầu bằng `C`.
  - Tách cờ `IsNonProduct` cho 10 mã dịch vụ/phí vận chuyển (`DOT`, `POST`, `M`, `AMAZONFEE`,...).
  - Giữ missing `CustomerID` trong transaction data và loại khỏi RFM.
  - Tạo thuộc tính `OrderMonth`, `Revenue`, `IsCancelled`, `IsNonProduct`.
- **Customer Segmentation bằng RFM:**
  - Tính toán Recency, Frequency, GrossMonetary, CancelledValue và Monetary ròng.
  - Giữ Monetary thực sau hoàn hủy, kể cả âm; gắn cờ `HasNegativeMonetary` và dùng Monetary thực để chấm điểm.
  - Phân loại 5 nhóm khách hàng: *Champions*, *Loyal Customers*, *Regular Customers*, *At Risk*, *Lost*.
  - Heatmap Pearson trên R/F/M gốc; scatter dùng log1p để hiển thị và ghi chú số khách Monetary âm không được vẽ.
- **Phân tích giữ chân khách hàng (Cohort Retention):**
  - Xây dựng ma trận retention theo tháng mua đầu tiên quan sát được.
  - CSV lưu tỷ lệ 0–1; heatmap hiển thị %, phân biệt 0%, kỳ chưa quan sát và tháng chưa đủ.
- **Thống kê NumPy & Outlier Detection:**
  - Tính Mean, Median, Std, Q1, Q3, IQR cho `Revenue`, `Quantity`, `UnitPrice`.
  - Xuất `outlier_summary.csv` và `outliers_detected.csv`.
- **Kiểm định chất lượng dữ liệu (Validation):**
  - 18 phép kiểm tra trên dữ liệu sạch và RFM, gồm công thức Monetary, cờ âm và độ bao phủ khách hàng.
  - Pipeline dừng nếu validation có lỗi; trước khi xuất dashboard còn đối chiếu doanh thu ròng và số khách.
- **Phân tích EDA & Trực quan hóa dữ liệu:**
  - Trả lời đầy đủ 8 câu hỏi nghiên cứu và xuất 12 bảng số liệu trong `reports/tables/`.
  - Phân tích chi tiết so sánh thị trường nội địa vs quốc tế: `uk_vs_nonuk_monthly.png` và `uk_vs_nonuk_monthly.csv`.
  - Gom theo `StockCode`: bảng Top mã hàng gồm phí/dịch vụ; góc nhìn Top hàng hóa trong notebook và báo cáo loại `IsNonProduct`.
  - Xếp hạng hoàn hủy độc lập theo số hóa đơn chứa mã hàng và theo giá trị hủy. Số đếm không phải tỷ lệ hủy.
- **Tài liệu & Báo cáo:**
  - Jupyter Notebook gọi cùng pipeline với CLI và trình bày các bảng, ảnh, nhận xét từ một nguồn.
  - Tài liệu chi tiết phương pháp luận: `notebooks/NoteBook.md`.
  - Báo cáo `reports/eda_results.md` và `reports/insight_report.md` được tạo lại từ kết quả tính.
- **Thực hành Web Scraping:**
  - Script Books to Scrape (`src/book_scraper.py`) thực hành HTTP GET, HTML parsing với BeautifulSoup, xử lý pagination và xuất `data/external/books_scraped.csv`.

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

Pipeline đọc `data/raw/Online_Retail.xlsx`, xuất dữ liệu đã xử lý, kiểm định,
tạo EDA, báo cáo, biểu đồ và cập nhật dashboard.

Mở `notebooks/eda_retail_analysis.ipynb` với kernel của môi trường vừa cài
và chọn **Run All** để chạy cùng quy trình. Mục scraping dùng HTML mẫu offline
theo mặc định; bật `LIVE_DEMO` nếu muốn thử một HTTP GET thật.

## Xem dashboard tĩnh

Mở [`web/index.html`](web/index.html) bằng trình duyệt. Khi nộp bài, giữ nguyên
cả thư mục `web/` để trang đọc được CSS, JavaScript và ảnh. Có thể mở trực
tiếp từ ổ đĩa khi không có Internet.

Dashboard hiển thị doanh thu ròng sau hoàn hủy. Các khoản hoàn hủy được ghi
nhận vào tháng phát sinh hóa đơn hủy. Xếp hạng theo doanh thu và tỷ trọng UK
vẫn dùng doanh thu gross.

Để tạo lại `web/data.js` và sao chép ảnh từ các báo cáo đã có, chạy:

```bash
python src/build_web.py
```

`data.js` là tệp sinh tự động từ `reports/tables/`. Nếu cần cập nhật các bảng
`dashboard_*.csv` từ hai CSV đã xử lý có sẵn, chạy
`python src/build_web.py --refresh-tables`.

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

Các nội dung cần chuẩn bị cho buổi báo cáo:

- Chuẩn bị Slide thuyết trình dựa trên `reports/insight_report.md` và `notebooks/NoteBook.md`.
- Luyện tập thuyết trình demo trên `notebooks/eda_retail_analysis.ipynb`.

Fake Store API không nằm trong phạm vi yêu cầu của giảng viên theo thông tin nhóm cung cấp.

