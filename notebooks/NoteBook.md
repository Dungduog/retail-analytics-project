# Phân tích khách hàng và sản phẩm trong bán lẻ online

## 1. Đặt vấn đề

Trong hoạt động bán lẻ online, mỗi giao dịch đều tạo ra nhiều thông tin liên quan đến sản phẩm, số lượng mua, giá bán, thời gian giao dịch, khách hàng và quốc gia.

Nếu chỉ lưu trữ dữ liệu mà không phân tích, doanh nghiệp sẽ khó nhận biết được sản phẩm nào đang bán tốt, khách hàng nào mang lại giá trị cao, doanh thu thay đổi theo thời gian như thế nào và các đơn hàng bị hủy có ảnh hưởng ra sao đến hoạt động kinh doanh.

Dự án này sử dụng bộ dữ liệu **UCI Online Retail** để phân tích dữ liệu giao dịch trong môi trường bán lẻ online.

Nhóm tập trung vào các hoạt động chính:

- Làm sạch dữ liệu giao dịch.
- Xây dựng các thuộc tính cần thiết cho phân tích.
- Phân tích sản phẩm và doanh thu.
- Phân tích hành vi khách hàng.
- Xây dựng RFM để đánh giá khách hàng.
- Phân tích các giao dịch bị hủy.
- Phát hiện các giá trị bất thường trong dữ liệu.

Mục tiêu của dự án là biến dữ liệu giao dịch thô thành dữ liệu có cấu trúc và có thể sử dụng cho các bước phân tích tiếp theo.

---

## 2. Câu hỏi nghiên cứu chính

**Nhóm khách hàng và sản phẩm nào tạo ra doanh thu cao, và các đơn hàng có xuất hiện dấu hiệu bất thường hoặc hủy giao dịch hay không?**

---

## 3. Các câu hỏi nghiên cứu phụ

Dự án tập trung trả lời các câu hỏi sau:

1. Doanh thu biến động theo thời gian như thế nào?
2. Sản phẩm nào được bán với số lượng nhiều nhất?
3. Sản phẩm nào tạo ra doanh thu cao nhất?
4. Phân khúc giá nào có lượng mua cao nhất?
5. Khách hàng nào vừa chi tiêu nhiều vừa mua hàng thường xuyên?
6. Quốc gia nào đóng góp doanh thu nhiều nhất?
7. Khách hàng nào đã lâu không quay lại mua hàng?
8. Những sản phẩm nào thường xuyên xuất hiện trong các đơn hàng bị hủy?

---

## 4. Mục tiêu phân tích

Thông qua các câu hỏi nghiên cứu trên, nhóm hướng tới các mục tiêu:

- Hiểu xu hướng doanh thu theo thời gian.
- Xác định các sản phẩm có hiệu suất bán hàng cao.
- Đánh giá mức độ đóng góp doanh thu của từng quốc gia.
- Phân tích hành vi mua hàng của khách hàng.
- Nhận diện những khách hàng có giá trị cao.
- Nhận diện những khách hàng đã lâu không quay lại.
- Phân tích các giao dịch bị hủy.
- Phát hiện các giá trị bất thường trong dữ liệu.
- Chuẩn bị dữ liệu sạch để phục vụ cho các bước EDA và visualization tiếp theo.

---

# 5. Dataset

## 5.1. Nguồn dữ liệu

Dataset chính được sử dụng là **UCI Online Retail**.

Dataset chứa dữ liệu giao dịch của một doanh nghiệp bán lẻ online với khoảng hơn 500,000 dòng dữ liệu.

Các thuộc tính chính bao gồm:

| Thuộc tính | Ý nghĩa |
|---|---|
| `InvoiceNo` | Mã hóa đơn |
| `StockCode` | Mã sản phẩm |
| `Description` | Tên sản phẩm |
| `Quantity` | Số lượng sản phẩm |
| `InvoiceDate` | Thời gian giao dịch |
| `UnitPrice` | Giá của một đơn vị sản phẩm |
| `CustomerID` | Mã khách hàng |
| `Country` | Quốc gia của khách hàng |

---

## 5.2. Kích thước dữ liệu ban đầu

Dataset ban đầu có:

- **541,909 dòng**
- **8 thuộc tính**

Khoảng thời gian dữ liệu:

- Bắt đầu: `2010-12-01`
- Kết thúc: `2011-12-09`

---

# 6. Data Profiling

Trước khi làm sạch dữ liệu, nhóm thực hiện bước Data Profiling để hiểu cấu trúc và chất lượng dữ liệu.

Các nội dung được kiểm tra bao gồm:

- Kiểu dữ liệu của từng cột.
- Số lượng missing values.
- Tỷ lệ missing values.
- Thống kê mô tả.
- Duplicate records.
- Quantity âm.
- UnitPrice bằng hoặc nhỏ hơn 0.
- Cancellation invoices.

---

## 6.1. Kiểu dữ liệu

Các kiểu dữ liệu ban đầu bao gồm:

- `InvoiceNo`: object
- `StockCode`: object
- `Description`: object
- `Quantity`: integer
- `InvoiceDate`: datetime
- `UnitPrice`: float
- `CustomerID`: float
- `Country`: string

---

## 6.2. Missing values

Hai thuộc tính có missing values đáng chú ý là:

- `Description`: 1,454 dòng thiếu.
- `CustomerID`: 135,080 dòng thiếu.

`CustomerID` có tỷ lệ missing lớn, khoảng 25% dataset.

Đây là vấn đề cần được xử lý cẩn thận vì `CustomerID` cần thiết cho các phân tích hành vi khách hàng nhưng không nhất thiết phải có đối với các phân tích doanh thu, sản phẩm hoặc quốc gia.

---

## 6.3. Duplicate records

Dataset có:

**5,268 dòng bị trùng lặp hoàn toàn.**

Một dòng được xem là duplicate khi toàn bộ các thuộc tính của nó giống hoàn toàn với một dòng khác.

Duplicate có thể làm tăng sai số khi tính tổng doanh thu hoặc số lượng bán nên cần được loại bỏ.

---

## 6.4. Quantity bất thường

Có:

**10,624 dòng có `Quantity < 0`.**

Tuy nhiên, Quantity âm không thể được xử lý bằng cách xóa toàn bộ vì một phần trong số đó là các giao dịch cancellation hoặc hoàn trả.

Do đó cần kết hợp `Quantity` với `InvoiceNo` để xác định ý nghĩa của từng trường hợp.

---

## 6.5. UnitPrice bất thường

Dataset có:

- Một số bản ghi `UnitPrice < 0`.
- Một số bản ghi `UnitPrice = 0`.

Những bản ghi này không phản ánh giao dịch bán hàng thông thường nên sẽ được loại khỏi tập dữ liệu phân tích chính.

---

## 6.6. Cancellation invoices

Các hóa đơn có `InvoiceNo` bắt đầu bằng ký tự:

`C`

được xem là các giao dịch cancellation hoặc hoàn trả.

Dataset có khoảng:

**9,288 dòng cancellation.**

Các dòng này không được xóa vì chúng cần thiết cho việc phân tích đơn hàng bị hủy.

---

# 7. Data Cleaning

Sau Data Profiling, nhóm xây dựng pipeline làm sạch dữ liệu để chuyển dữ liệu thô thành dữ liệu có thể sử dụng cho phân tích.

---

## 7.1. Loại bỏ duplicate

Các dòng trùng lặp hoàn toàn được loại bỏ bằng:

`drop_duplicates()`

Việc này giúp tránh tính cùng một giao dịch nhiều lần khi tính doanh thu hoặc số lượng bán.

---

## 7.2. Xử lý UnitPrice

Các giao dịch có:

`UnitPrice <= 0`

được loại khỏi dataset chính.

Lý do là giá bằng 0 hoặc âm không phản ánh một giao dịch bán hàng thông thường và có thể làm sai lệch việc tính doanh thu.

---

## 7.3. Xác định cancellation

Các hóa đơn có `InvoiceNo` bắt đầu bằng ký tự `C` được xác định là cancellation.

Một thuộc tính mới được tạo:

`IsCancelled`

Trong đó:

- `False`: giao dịch bán hàng bình thường.
- `True`: giao dịch cancellation.

Việc giữ lại cancellation giúp phục vụ các phân tích liên quan đến hoàn trả và hủy giao dịch.

---

## 7.4. Xử lý Quantity âm

Quantity được xử lý theo ba trường hợp:

- `Quantity > 0`: giao dịch bán hàng bình thường.
- `Quantity < 0` và `InvoiceNo` bắt đầu bằng `C`: cancellation, được giữ lại.
- `Quantity < 0` nhưng `InvoiceNo` không bắt đầu bằng `C`: loại khỏi tập dữ liệu phân tích chính.

Các trường hợp Quantity âm nhưng không phải cancellation có thể liên quan đến điều chỉnh kho hoặc các nghiệp vụ nội bộ và không phản ánh giao dịch mua hàng thông thường.

---

## 7.5. Xử lý missing CustomerID

Nhóm không xóa toàn bộ các giao dịch bị thiếu `CustomerID`.

Các giao dịch này vẫn chứa thông tin có giá trị như:

- sản phẩm,
- số lượng,
- doanh thu,
- thời gian,
- quốc gia.

Do đó chúng vẫn được giữ trong `cleaned_retail.csv`.

Tuy nhiên, những dòng thiếu `CustomerID` sẽ không được sử dụng trong các phân tích ở cấp độ khách hàng như RFM vì không thể xác định chúng thuộc về khách hàng nào.

---

## 7.6. Chuẩn hóa InvoiceDate

`InvoiceDate` được chuyển sang kiểu:

`datetime`

Việc này giúp thực hiện các thao tác phân tích theo thời gian.

---

## 7.7. Tạo OrderMonth

Từ `InvoiceDate`, nhóm tạo thêm thuộc tính:

`OrderMonth`

có dạng:

`YYYY-MM`

Ví dụ:

`2011-09`

Thuộc tính này sẽ được sử dụng để phân tích doanh thu theo tháng.

---

## 7.8. Tạo Revenue

Doanh thu của từng dòng giao dịch được tính theo công thức:

`Revenue = Quantity × UnitPrice`

Đối với giao dịch bán hàng bình thường:

`Revenue > 0`

Đối với cancellation:

`Revenue < 0`

Giá trị âm giúp thể hiện phần doanh thu bị hoàn trả hoặc hủy.

---

## 7.9. Kết quả sau cleaning

Dữ liệu ban đầu:

**541,909 dòng**

Sau quá trình cleaning:

**534,129 dòng**

Dataset sau cleaning có thêm các thuộc tính:

- `IsCancelled`
- `OrderMonth`
- `Revenue`

Kết quả được xuất thành:

`cleaned_retail.csv`

File này được sử dụng làm nguồn dữ liệu chính cho các bước phân tích tiếp theo.

---

# 8. Sử dụng Python Functions và Data Structures

Trong quá trình xây dựng pipeline, nhóm xây dựng bốn hàm cơ bản:

### 8.1. Tính Revenue

Hàm tính:

`Revenue = Quantity × UnitPrice`

### 8.2. Kiểm tra cancellation

Hàm kiểm tra xem `InvoiceNo` có bắt đầu bằng ký tự `C` hay không.

### 8.3. Tách tháng giao dịch

Hàm chuyển `InvoiceDate` thành:

`YYYY-MM`

### 8.4. Gán nhãn RFM

Hàm sử dụng điểm:

- `R_Score`
- `F_Score`
- `M_Score`

để xác định nhóm khách hàng.

---

## 8.5. Sử dụng List, Dict, Set và Tuple

Project sử dụng các cấu trúc dữ liệu Python cơ bản.

### List

`invoice_records`

được sử dụng để lưu danh sách các giao dịch.

### Dictionary

`country_summary`

được sử dụng để ánh xạ:

`Country → Revenue`

### Set

`product_codes`

được sử dụng để lưu tập hợp các mã sản phẩm duy nhất.

### Tuple

`date_range`

được sử dụng để lưu:

`(ngày bắt đầu, ngày kết thúc)`

---

# 9. Xây dựng RetailDataProcessor

Để tổ chức pipeline rõ ràng hơn, nhóm xây dựng class:

`RetailDataProcessor`

Class này chịu trách nhiệm xử lý các bước chính:

- Load dữ liệu.
- Clean dữ liệu.
- Tạo các cấu trúc dữ liệu cơ bản.
- Phân tích doanh thu.
- Tạo customer segmentation.
- Export kết quả.

Việc sử dụng class giúp pipeline có cấu trúc rõ ràng và có thể chạy lại trên dữ liệu mới.

---

# 10. Customer Segmentation bằng RFM

RFM được sử dụng để đánh giá hành vi của từng khách hàng dựa trên ba yếu tố:

### Recency

Số ngày kể từ lần mua hàng gần nhất.

Recency càng thấp thì khách hàng càng mới quay lại mua hàng.

### Frequency

Số hóa đơn mua hàng khác nhau của khách hàng.

Frequency càng cao thì khách hàng mua hàng càng thường xuyên.

### Monetary

Tổng giá trị ròng mà khách hàng mang lại.

Monetary được tính bằng:

`GrossMonetary - CancelledValue`

Trong đó:

- `GrossMonetary`: tổng giá trị mua hàng.
- `CancelledValue`: tổng giá trị các giao dịch bị cancellation.
- `Monetary`: giá trị ròng của khách hàng.

---

## 10.1. RFM Score

Mỗi khách hàng được gán:

- `R_Score`: từ 1 đến 4.
- `F_Score`: từ 1 đến 4.
- `M_Score`: từ 1 đến 4.

Ý nghĩa:

- Score 1: thấp.
- Score 4: cao.

Riêng Recency có logic ngược:

Recency càng thấp thì `R_Score` càng cao.

---

## 10.2. Customer Segment

Các segment hiện tại bao gồm:

### Champions

Khách hàng:

- mua gần đây,
- mua thường xuyên,
- chi tiêu cao.

Điều kiện:

`R >= 3, F >= 3, M >= 3`

### At Risk

Khách từng có giá trị hoặc mua thường xuyên nhưng đã lâu không quay lại.

Điều kiện:

`R <= 2` và (`F >= 3` hoặc `M >= 3`)

### Loyal Customers

Khách hàng mua thường xuyên và vẫn còn tương đối active.

### Lost

Khách đã lâu không quay lại, có Frequency thấp và Monetary thấp.

### Regular Customers

Các khách hàng không thuộc các nhóm trên.

---

## 10.3. Kết quả RFM

Sau khi xử lý, dữ liệu RFM được xuất thành:

`customer_segments.csv`

Các thuộc tính chính gồm:

- `CustomerID`
- `Recency`
- `Frequency`
- `GrossMonetary`
- `CancelledValue`
- `Monetary`
- `R_Score`
- `F_Score`
- `M_Score`
- `Segment`

Ví dụ, khách hàng `12346` có:

- GrossMonetary ≈ 77,183.60
- CancelledValue ≈ 77,183.60
- Monetary = 0
- Segment = Lost

Trường hợp này cho thấy việc trừ cancellation khỏi Monetary là cần thiết để đánh giá đúng giá trị thực tế của khách hàng.

---

# 11. Phân tích thống kê bằng NumPy

Sau khi hoàn thành cleaning, nhóm sử dụng NumPy để thực hiện thống kê mô tả trên ba thuộc tính:

- `Revenue`
- `Quantity`
- `UnitPrice`

Các phép thống kê được sử dụng gồm:

- Mean
- Median
- Standard deviation
- Percentile 25%
- Percentile 75%

Mục tiêu của bước này là hiểu phân bố dữ liệu và phát hiện các giá trị bất thường.

---

## 11.1. Mean

Mean thể hiện giá trị trung bình của dữ liệu.

Ví dụ:

`np.mean(data)`

---

## 11.2. Median

Median là giá trị nằm giữa dữ liệu sau khi sắp xếp.

Median ít bị ảnh hưởng bởi các giá trị cực lớn hoặc cực nhỏ hơn mean.

---

## 11.3. Standard Deviation

Standard deviation thể hiện mức độ phân tán của dữ liệu quanh giá trị trung bình.

Standard deviation càng lớn thì dữ liệu càng phân tán mạnh.

---

## 11.4. Percentile

Nhóm sử dụng:

- Q1 = percentile 25%.
- Q3 = percentile 75%.

Từ đó tính:

`IQR = Q3 - Q1`

---

# 12. Outlier Detection

Để phát hiện outlier, nhóm sử dụng phương pháp IQR.

Giới hạn được xác định bằng:

`Lower Bound = Q1 - 1.5 × IQR`

`Upper Bound = Q3 + 1.5 × IQR`

Một giá trị được đánh dấu là outlier nếu:

- nhỏ hơn Lower Bound, hoặc
- lớn hơn Upper Bound.

Outlier không đồng nghĩa với dữ liệu sai.

Một outlier có thể là:

- lỗi dữ liệu,
- giao dịch đặc biệt,
- giao dịch mua số lượng rất lớn,
- hoặc nghiệp vụ không phải bán sản phẩm thông thường.

---

## 12.1. Outlier của Revenue

Kết quả:

- Mean ≈ 20.28
- Median = 9.92
- Q1 = 3.90
- Q3 = 17.70
- Upper Bound = 38.40
- Số outlier = 42,624

Một số Revenue rất lớn được phát hiện như:

- 168,469.60
- 77,183.60
- 38,970.00

Mean lớn hơn đáng kể so với median cho thấy một số giao dịch lớn đang kéo giá trị trung bình lên.

---

## 12.2. Outlier của Quantity

Kết quả:

- Mean ≈ 10.62
- Median = 4
- Q1 = 1
- Q3 = 11
- Upper Bound = 26
- Số outlier = 27,111

Một số giao dịch có Quantity rất lớn như:

- 80,995
- 74,215
- 4,800
- 4,300

Những giá trị này cần được xem xét riêng thay vì tự động xóa khỏi dataset.

---

## 12.3. Outlier của UnitPrice

Kết quả:

- Mean ≈ 3.92
- Median = 2.08
- Q1 = 1.25
- Q3 = 4.13
- Upper Bound = 8.45
- Số outlier = 37,827

Một số giá trị UnitPrice cực lớn thuộc về các bản ghi như:

- `AMAZON FEE`
- `Adjust bad debt`
- `POSTAGE`
- `DOTCOM POSTAGE`
- `Manual`

Các bản ghi này có thể là phí hoặc nghiệp vụ nội bộ thay vì sản phẩm bán lẻ thông thường.

Do đó, chúng cần được cân nhắc khi thực hiện các phân tích sản phẩm ở bước EDA.

---

## 12.4. Lưu kết quả outlier

Kết quả phân tích outlier được xuất thành hai file:

### `outlier_summary.csv`

Lưu các thống kê:

- Mean
- Median
- Standard deviation
- Q1
- Q3
- IQR
- Lower Bound
- Upper Bound
- Outlier Count
- Outlier Percentage

### `outliers_detected.csv`

Lưu chi tiết các giao dịch bị phát hiện là outlier.

Một giao dịch có thể xuất hiện nhiều lần trong file này nếu đồng thời là outlier của nhiều thuộc tính, ví dụ vừa là outlier của `Quantity` vừa là outlier của `Revenue`.

---

# 13. Kết quả đạt được đến thời điểm hiện tại

Đến thời điểm hiện tại, project đã hoàn thành các bước:

1. Xác định vấn đề và câu hỏi nghiên cứu.
2. Khảo sát cấu trúc dataset.
3. Data Profiling.
4. Xây dựng quy tắc Data Cleaning.
5. Xây dựng pipeline làm sạch dữ liệu.
6. Tạo `cleaned_retail.csv`.
7. Xây dựng các function Python cơ bản.
8. Sử dụng List, Dictionary, Set và Tuple.
9. Xây dựng class `RetailDataProcessor`.
10. Xây dựng RFM Customer Segmentation.
11. Tạo `customer_segments.csv`.
12. Sử dụng NumPy để tính thống kê mô tả.
13. Phát hiện outlier bằng phương pháp IQR.
14. Tạo `outlier_summary.csv`.
15. Tạo `outliers_detected.csv`.

Các bước EDA, visualization và trả lời chi tiết các câu hỏi nghiên cứu sẽ được thực hiện ở các phần tiếp theo.