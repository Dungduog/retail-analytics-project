# Phân tích khách hàng và sản phẩm trong bán lẻ online

**PSD301M · Trí Dũng và Tuấn Triển**

Dự án dùng UCI Online Retail để xác định khách hàng và hàng hóa tạo doanh thu cao, đồng thời xem xét giao dịch bất thường và hoàn hủy. Phần Books to Scrape minh họa kỹ thuật thu thập HTML và không tham gia các phép tính UCI.

## Cách đọc và tái tạo kết quả

- [Notebook thực thi](eda_retail_analysis.ipynb) trình bày code, output, bảng và biểu đồ.
- [Kết quả EDA](../reports/eda_results.md) trả lời tám câu hỏi nghiên cứu.
- [Báo cáo insight](../reports/insight_report.md) tổng hợp quan sát, giới hạn và đề xuất kiểm chứng.
- [Dashboard offline](../web/index.html) trình bày số liệu đã tổng hợp.

Chạy `python main.py` hoặc **Run All** trong notebook sau khi cài `requirements.txt`. Cả hai dùng chung pipeline, cùng xuất dữ liệu, biểu đồ và báo cáo. Tài liệu này mô tả phương pháp; các số liệu kết luận nằm trong output được tạo lại.

## 1. Profiling và cleaning

`RetailDataProcessor.load_data()` đọc Excel hoặc CSV và kiểm tra các cột bắt buộc. Notebook hiển thị kích thước, kiểu dữ liệu, số dòng thiếu, trùng, Quantity âm và UnitPrice không dương.

Các quy tắc cleaning:

1. Loại dòng trùng hoàn toàn và dòng có `UnitPrice <= 0`.
2. Chuẩn hóa InvoiceNo, StockCode và khoảng trắng trong Description.
3. Đánh dấu `IsCancelled` khi InvoiceNo bắt đầu bằng C. Giữ dòng hủy, loại Quantity âm không thuộc dòng hủy.
4. Gắn `IsNonProduct` cho mã phí hoặc dịch vụ đã xác định. Cờ này không loại giao dịch khỏi tổng doanh thu.
5. Chuyển InvoiceDate sang datetime, tạo OrderMonth và tính Revenue = Quantity × UnitPrice.
6. Giữ dòng thiếu CustomerID trong phân tích giao dịch; loại khỏi phân tích theo khách.

`cleaned_retail.csv` lưu kết quả. Cleaning log cho biết số dòng bị loại ở từng bước.

## 2. Python và cấu trúc dữ liệu

Lớp `RetailDataProcessor` đóng gói load, cleaning, phân nhóm và export. Các hàm `calculate_revenue`, `is_cancelled`, `get_order_month`, `assign_rfm_segment` minh họa logic trên một giá trị hoặc một bản ghi. Trong pipeline, OrderMonth được tính bằng Pandas vector hóa.

`create_basic_structures()` trả List giao dịch mẫu, Dict doanh thu theo quốc gia, Set mã hàng và Tuple khoảng thời gian. Notebook minh họa cả bốn kiểu dữ liệu trên kết quả thực.

## 3. RFM

Phân nhóm trên khách định danh có ít nhất một hóa đơn bán:

- **Recency:** số ngày từ lần mua cuối đến ngày tham chiếu bằng ngày mua cuối cùng của tập khách cộng một ngày.
- **Frequency:** số InvoiceNo bán khác nhau của khách.
- **Monetary:** GrossMonetary − CancelledValue. Giữ số âm khi giá trị hoàn hủy vượt giá trị bán trong kỳ; `HasNegativeMonetary` ghi nhận trường hợp này.

Điểm từ 1 đến 4 theo percentile; Recency thấp nhận điểm cao. Quy tắc áp dụng theo thứ tự:

| Nhãn | Điều kiện |
|---|---|
| Champions | R ≥ 3, F ≥ 3, M ≥ 3 |
| Loyal Customers | R ≥ 3 và F ≥ 3, sau khi đã xét Champions |
| At Risk | R ≤ 2 và (F ≥ 3 hoặc M ≥ 3) |
| Lost | R ≤ 2, F ≤ 2, M ≤ 2 |
| Regular Customers | Các trường hợp còn lại |

Tổng Monetary RFM chỉ phản ánh tập khách đủ điều kiện; không đồng nhất với doanh thu ròng toàn bộ giao dịch. Tỷ trọng của Champions dùng mẫu số là tổng Monetary của bảng RFM. Nhãn là mô tả trong thời gian quan sát, không dự báo churn. Nếu thử ngưỡng 120 ngày cho chiến dịch win-back, đó là đề xuất kiểm chứng, không phải điều kiện của Lost.

Heatmap tương quan dùng Pearson trên dữ liệu R/F/M gốc. Scatter dùng log1p cho mục đích hiển thị, loại Monetary âm khỏi hình và ghi số điểm không vẽ. Các khách này vẫn nằm trong bảng RFM và phép tính tương quan. Tương quan không xác định nhân quả; màu phân khúc không phải đánh giá một mô hình dự báo.

## 4. NumPy, outlier và validation

Trên dòng bán, `outlier_analysis.py` dùng NumPy tính mean, median, std, Q1 và Q3 của Revenue, Quantity, UnitPrice. Với IQR = Q3 − Q1, cờ outlier được gắn ngoài khoảng Q1 − 1,5×IQR đến Q3 + 1,5×IQR.

`outlier_summary.csv` lưu thống kê, `outliers_detected.csv` lưu chi tiết. Một dòng có thể xuất hiện nhiều lần nếu vượt ngưỡng ở nhiều thuộc tính. Dự án không tự xóa outlier.

Validation kiểm tra cột dẫn xuất, cờ hủy, điểm RFM, độ bao phủ CustomerID và công thức Monetary. Lỗi làm pipeline dừng trước khi tạo EDA/dashboard mới. Khi build dashboard, tổng net được đối chiếu với Revenue có dấu trong dữ liệu sạch và số khách theo segment phải khớp bảng RFM.

## 5. Phạm vi từng kết quả EDA

| Câu hỏi | Kết quả được lấy từ |
|---|---|
| Doanh thu thay đổi thế nào? | `monthly_revenue.csv` dùng gross; dashboard dùng gross − hoàn hủy để trình bày net theo tháng |
| Hàng hóa bán nhiều nhất? | Góc nhìn `top_goods_quantity` từ cùng phép gom StockCode, loại IsNonProduct |
| Hàng hóa tạo doanh thu cao nhất? | Góc nhìn `top_goods_revenue` sau khi loại mã phí; bảng Top mã hàng vẫn giữ phí |
| Phân khúc giá nào có lượng mua lớn nhất? | `price_segments.csv`, dùng tứ phân vị UnitPrice của dòng bán, có thể gồm mã phí |
| Khách chi nhiều và mua thường xuyên? | `top_customers.csv`, Champions xếp theo Monetary thực, kèm Frequency |
| Quốc gia đóng góp nhiều nhất? | `country_revenue.csv` và so sánh UK/Non-UK, đều dùng gross |
| Khách đã lâu không mua? | `inactive_customers.csv`, Lost/At Risk xếp theo Recency |
| Mã hàng nào xuất hiện nhiều trong hóa đơn hủy? | `cancelled_products.csv` đếm hóa đơn; `cancelled_products_by_value.csv` xếp riêng theo giá trị hủy |

Gross giữ doanh thu của lượt bán ban đầu, kể cả khi phát sinh hoàn hủy về sau. Net trên dashboard ghi giá trị hủy vào tháng của hóa đơn hủy. Vì vậy, net theo tháng không phải cách ghép hồi tố mọi lượt hoàn trả về tháng bán ban đầu. Top mã hàng không đồng nghĩa top hàng hóa. Số hóa đơn hủy chứa một sản phẩm không phải tỷ lệ hủy; thiếu mẫu số và lý do hoàn trả thì chưa thể kết luận sản phẩm có rủi ro cao hoặc nguyên nhân từ đóng gói.

## 6. Cohort retention

Một cohort gồm khách có cùng tháng mua đầu tiên **quan sát được**. Ở M+n, tử số là số khách của cohort có mua trong tháng tương ứng; mẫu số là số khách ban đầu của cohort. Mỗi khách được đếm tối đa một lần trong mỗi tháng.

CSV lưu tỷ lệ trong khoảng **0–1**. Ô 0 là tháng đã quan sát nhưng không có khách mua lại. Ô trống, màu xám trên heatmap, là kỳ chưa quan sát. Tháng 12/2011 có dữ liệu đến ngày 09/12, được đánh dấu * và viền xanh, không đem so trực tiếp với tháng đủ.

Không mua ở M+1 không có nghĩa là không quay lại. Báo cáo đếm riêng khách bỏ qua M+1 nhưng có mua ở M+2 trở đi. Khi so sánh cohort, dùng cùng độ dài theo dõi; dữ liệu khoảng một năm không đủ chứng minh quy luật mùa vụ.

## 7. Thực hành web scraping

`src/book_scraper.py` gửi HTTP GET với timeout, kiểm tra status, parse HTML bằng BeautifulSoup, đọc text và thuộc tính từ selector, theo liên kết next bằng URL tuyệt đối rồi xuất CSV. Notebook minh họa một thẻ `article.product_pod`, thuộc tính của `h3 a` và class chứa rating. Mặc định dùng HTML mẫu offline; bật `LIVE_DEMO` để kiểm tra HTTP thật trên một trang.

CSV sách là kết quả từ lần cào đầy đủ; demo không ghi đè file. Giá và rating của website dùng để thực hành, không phải dữ liệu để suy ra thị trường.

## 8. Kết luận và giới hạn

Xem [báo cáo insight mới nhất](../reports/insight_report.md) để lấy số liệu thuyết trình. Mỗi kết luận cần đi cùng phạm vi đo, giới hạn và đề xuất kiểm chứng. Không suy từ doanh thu sang lợi nhuận, dòng tiền, khả năng cấp tín dụng hoặc nguyên nhân hủy; dataset không chứa thông tin cần thiết cho các kết luận đó.
