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

## 7.9. Chuẩn hóa dữ liệu & Tách mã nghiệp vụ

Trước khi xuất dữ liệu sạch, pipeline thực hiện thêm 2 bước chuẩn hóa quan trọng:

1. **Chuẩn hóa chuỗi và định dạng mã:**
   - `InvoiceNo` và `StockCode` được ép kiểu chuỗi, cắt khoảng trắng thừa (`str.strip()`).
   - `StockCode` được chuyển toàn bộ sang chữ in hoa (`str.upper()`), giúp gom 110 mã bị trùng lặp do khác biệt chữ hoa/thường (ví dụ `85123a` và `85123A`), đưa số mã sản phẩm duy nhất từ 3,938 về **3,828 mã**.
   - `Description` được cắt tỉa khoảng trắng đầu/cuối.

2. **Gắn cờ mã phi sản phẩm (`IsNonProduct`):**
   - Đánh dấu 10 mã dịch vụ/chi phí hệ thống: `DOT` (DOTCOM POSTAGE), `POST` (POSTAGE), `M` (Manual), `AMAZONFEE`, `B` (Adjust bad debt), `C2` (Carriage), `BANK CHARGES`, `S` (Samples), `D` (Discount), `CRUK` (CRUK Commission).
   - Nhóm này chiếm ~3.70% doanh thu bán hàng. Việc tạo cờ boolean `IsNonProduct` giúp các phân tích sản phẩm bán lẻ dễ dàng lọc bỏ các mã này mà không làm mất thông tin tài chính chung.

---

## 7.10. Kết quả sau cleaning & Cleaning Log

Quá trình làm sạch dữ liệu ghi nhận chi tiết qua từng bước:

| Bước làm sạch | Số dòng ban đầu | Số dòng bị loại | Số dòng còn lại | Ghi chú lý do |
|---|---|---|---|---|
| **1. Dữ liệu gốc** | — | — | **541,909** | Kích thước ban đầu |
| **2. Deduplication** | 541,909 | 5,268 | 536,641 | Loại bỏ các dòng trùng lặp toàn bộ |
| **3. Lọc UnitPrice > 0** | 536,641 | 2,512 | 534,129 | Loại bỏ đơn giá bằng 0 hoặc âm |
| **4. Lọc Quantity âm phi hủy** | 534,129 | 0 | 534,129 | Toàn bộ dòng Qty âm còn lại đều là đơn hủy hợp lệ (Invoice bắt đầu bằng C) |
| **Tổng kết** | **541,909** | **7,780** | **534,129** | Giảm 1.44% tổng số dòng |

Dataset sau cleaning có thêm các thuộc tính mới:

- `IsCancelled` (boolean): đánh dấu đơn hủy.
- `IsNonProduct` (boolean): đánh dấu mã dịch vụ/phí vận chuyển.
- `OrderMonth` (chuỗi `YYYY-MM`): phục vụ phân tích xu hướng thời gian.
- `Revenue` (float): `Quantity * UnitPrice` (âm với đơn hủy, dương với đơn bán).

Kết quả được xuất thành:

`data/processed/cleaned_retail.csv`

File này là nguồn dữ liệu chuẩn mực cho tất cả các bước phân tích downstream.

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

### Xử lý khách hàng có Monetary âm (`HasNegativeMonetary`)

Trong quá trình phân tích, nhóm phát hiện **8 khách hàng** có giá trị hoàn trả vượt quá tổng giá trị mua hàng trong giai đoạn theo dõi (ví dụ đơn mua diễn ra trước thời điểm ghi nhận dữ liệu hoặc đơn đổi trả phát sinh chênh lệch).

Để đảm bảo tính hợp lệ của phân vị và xếp hạng công bằng:
- Thuật toán gắn cờ `HasNegativeMonetary = True`.
- Kẹp giá trị `Monetary` về mức tối thiểu bằng 0 (`Monetary.clip(lower=0)`), tránh làm lệch ngưỡng tính `M_Score`.

---

## 10.4. Phân tích tương quan RFM & Biểu đồ phân tán (Scatter Plot)

Để kiểm chứng tính độc lập và ý nghĩa tương tác giữa 3 chỉ số R, F, M, nhóm xây dựng **RFM Correlation Heatmap** và **Scatter Plot** phân bố khách hàng.

### Tương quan Pearson giữa Recency, Frequency và Monetary

Ma trận tương quan ghi nhận:
- **Frequency và Monetary:** tương quan dương mạnh (**r ≈ 0.43**). Khách hàng mua sắm càng thường xuyên thì tích lũy chi tiêu ròng càng lớn.
- **Recency và Frequency:** tương quan âm (**r ≈ -0.21**). Khách hàng mới quay lại mua hàng gần đây có tần suất mua cao hơn rõ rệt.
- **Recency và Monetary:** tương quan âm nhẹ (**r ≈ -0.12**).

Biểu đồ heatmap tương quan được lưu tại `reports/figures/rfm_correlation_heatmap.png`.

### Biểu đồ phân tán Frequency vs Monetary (log scale) theo phân khúc

Biểu đồ phân tán trên thang đo `log1p` (lưu tại `reports/figures/rfm_scatter_freq_monetary.png`) thể hiện cấu trúc phân cụm rất mạch lạc:
- **Champions:** gom cụm chặt chẽ ở góc trên cùng bên phải (tần suất mua cao, chi tiêu lớn).
- **Lost:** dồn về góc dưới bên trái (mua 1–2 lần với giá trị nhỏ).
- **At Risk & Regular Customers:** phân bố trải rộng ở dải chuyển tiếp trung tâm — đây là vùng hành động chiến lược để kích hoạt chuyển đổi khách hàng tiềm năng lên nhóm Champions.

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

# 13. Tổng hợp các bước đã hoàn thành

Project đã hoàn thành toàn bộ pipeline từ đầu đến cuối:

1. Xác định vấn đề và câu hỏi nghiên cứu.
2. Khảo sát cấu trúc dataset.
3. Data Profiling.
4. Xây dựng quy tắc Data Cleaning.
5. Xây dựng pipeline làm sạch dữ liệu.
6. Tạo `cleaned_retail.csv`.
7. Xây dựng các function Python cơ bản (`utils.py`).
8. Sử dụng List, Dictionary, Set và Tuple.
9. Xây dựng class `RetailDataProcessor`.
10. Xây dựng RFM Customer Segmentation.
11. Tạo `customer_segments.csv`.
12. Sử dụng NumPy để tính thống kê mô tả.
13. Phát hiện outlier bằng phương pháp IQR.
14. Tạo `outlier_summary.csv` và `outliers_detected.csv`.
15. Kiểm định chất lượng dữ liệu — 15 phép kiểm tra tự động (cả 15 đạt 0 lỗi).
16. EDA — trả lời 8 câu hỏi nghiên cứu, sinh 9 bảng kết quả và 8 biểu đồ.
17. Tạo Jupyter Notebook `eda_retail_analysis.ipynb` với code, output và nhận xét.

---

# 14. EDA — Kết quả 8 câu hỏi nghiên cứu

Tất cả số liệu dưới đây được tính từ `cleaned_retail.csv` và `customer_segments.csv`.
Doanh thu theo tháng, quốc gia và sản phẩm chỉ dùng normal sales; cancellation được phân tích riêng.

---

## 14.1. Doanh thu biến động theo thời gian như thế nào?

Gross revenue theo tháng (đơn vị GBP):

| Tháng | Doanh thu | Tháng | Doanh thu |
|---|---|---|---|
| 2010-12 | 821,453 | 2011-07 | 718,076 |
| 2011-01 | 689,812 | 2011-08 | 757,841 |
| 2011-02 | 522,546 | 2011-09 | 1,056,435 |
| 2011-03 | 716,215 | 2011-10 | 1,151,264 |
| 2011-04 | 536,968 | **2011-11** | **1,503,867** |
| 2011-05 | 769,297 | 2011-12 | 637,790 |
| 2011-06 | 760,547 | | |

Nhận xét:

- Doanh thu cao nhất vào **tháng 11/2011** với 1,503,867 GBP.
- Ba tháng 9, 10, 11 chiếm khoảng **34.9%** tổng gross revenue cả giai đoạn, phù hợp mùa mua sắm cuối năm trước Giáng sinh. (Lưu ý: Q4 theo lịch dương là tháng 10–12, chiếm ~30.9%; tháng 12 trong dataset chưa đầy đủ.)
- Tháng 12/2011 thấp vì dữ liệu chỉ kéo dài đến ngày 09/12 — không phản ánh xu hướng thực.

### Phân tích chuyên sâu: Doanh thu thị trường UK vs Non-UK theo tháng

Để hiểu rõ cấu trúc doanh thu theo địa lý, nhóm tổng hợp bảng so sánh doanh thu nội địa (United Kingdom) và quốc tế (Non-UK) theo từng tháng (`reports/tables/uk_vs_nonuk_monthly.csv`):

| Tháng | UK (GBP) | Non-UK (GBP) | Tổng cộng (GBP) | Tỷ trọng UK (%) |
|---|---|---|---|---|
| 2010-12 | 746,082 | 75,371 | 821,453 | 90.8% |
| 2011-01 | 559,976 | 129,836 | 689,812 | 81.2% |
| 2011-02 | 428,987 | 93,559 | 522,546 | 82.1% |
| 2011-03 | 584,811 | 131,404 | 716,215 | 81.7% |
| 2011-04 | 475,678 | 61,291 | 536,968 | 88.6% |
| 2011-05 | 638,105 | 131,192 | 769,297 | 82.9% |
| 2011-06 | 618,346 | 142,201 | 760,547 | 81.3% |
| 2011-07 | 600,919 | 117,157 | 718,076 | 83.7% |
| 2011-08 | 606,785 | 151,056 | 757,841 | 80.1% |
| 2011-09 | 895,099 | 161,337 | 1,056,435 | 84.7% |
| 2011-10 | 935,404 | 215,860 | 1,151,264 | 81.3% |
| 2011-11 | 1,319,934 | 183,933 | 1,503,867 | 87.8% |
| 2011-12 | 591,620 | 46,171 | 637,790 | 92.8% |

**Nhận xét thị trường:**
- **Thị trường Anh là động lực tăng trưởng:** Doanh thu UK chiếm bình quân 84.6% tổng doanh số và tạo nên toàn bộ sự bùng nổ cuối năm (tháng 9: 0.90M → tháng 11: 1.32M GBP).
- **Thị trường quốc tế có tính ổn định cao:** Doanh thu ngoài UK dao động đều đặn trong dải 90k – 215k GBP/tháng, thể hiện nguồn cầu bền vững từ các đối tác bán buôn châu Âu (Hà Lan, Đức, Pháp, Ireland).
- Biểu đồ đường so sánh được lưu tại `reports/figures/uk_vs_nonuk_monthly.png`.

---

## 14.2. Sản phẩm nào được bán với số lượng nhiều nhất?

| Hạng | Sản phẩm | Số lượng |
|---|---|---|
| 1 | PAPER CRAFT , LITTLE BIRDIE | 80,995 |
| 2 | MEDIUM CERAMIC TOP STORAGE JAR | 78,033 |
| 3 | WORLD WAR 2 GLIDERS ASSTD DESIGNS | 54,951 |
| 4 | JUMBO BAG RED RETROSPOT | 48,371 |
| 5 | WHITE HANGING HEART T-LIGHT HOLDER | 37,872 |
| 6 | POPCORN HOLDER | 36,749 |

Nhận xét:

Đơn hàng 80,995 sản phẩm PAPER CRAFT, LITTLE BIRDIE (khách 16446, ngày 09/12/2011) bị hủy sau 12 phút. Tương tự, đơn 74,215 sản phẩm MEDIUM CERAMIC TOP STORAGE JAR (khách 12346) cũng bị hủy ngay sau đó. Vì phân tích này dùng gross sales nên hai đơn trên vẫn được tính vào thứ hạng.

---

## 14.3. Sản phẩm nào tạo ra doanh thu cao nhất?

| Hạng | Sản phẩm | Doanh thu |
|---|---|---|
| 1 | DOTCOM POSTAGE (mã phí) | 206,249 |
| 2 | REGENCY CAKESTAND 3 TIER | 174,157 |
| 3 | PAPER CRAFT , LITTLE BIRDIE | 168,470 |
| 4 | WHITE HANGING HEART T-LIGHT HOLDER | 104,284 |
| 5 | PARTY BUNTING | 99,445 |
| 6 | JUMBO BAG RED RETROSPOT | 94,160 |

Nhận xét:

Kết quả giữ nguyên các mã phí và dịch vụ như `DOTCOM POSTAGE`, `POSTAGE`, `Manual`. Nếu chỉ tính sản phẩm bán lẻ thực sự thì **REGENCY CAKESTAND 3 TIER** đứng đầu với doanh thu 174,157.

---

## 14.4. Phân khúc giá nào có lượng mua cao nhất?

Phân khúc giá được chia theo tứ phân vị UnitPrice: Q1 = 1.25, Median = 2.08, Q3 = 4.13.

| Phân khúc | Khoảng giá | Số lượng bán | Doanh thu |
|---|---|---|---|
| Low | ≤ 1.25 | **2,887,471** | 2,016,182 |
| Medium | 1.25 – 2.08 | 1,286,199 | 2,231,864 |
| High | 2.08 – 4.13 | 897,419 | 2,585,402 |
| Premium | > 4.13 | 501,331 | **3,808,663** |

Nhận xét:

Phân khúc **Low** có lượng mua nhiều nhất (2.9 triệu sản phẩm). Ngược lại, phân khúc **Premium** bán ít nhất nhưng đóng góp doanh thu cao nhất (3.8 triệu). Doanh thu không tỉ lệ thuận với số lượng.

---

## 14.5. Khách hàng nào vừa chi tiêu nhiều vừa mua thường xuyên?

Top khách trong nhóm Champions (sắp xếp theo Monetary ròng):

| CustomerID | Recency (ngày) | Số hóa đơn | Monetary ròng |
|---|---|---|---|
| 14646 | 2 | 73 | 279,489 |
| 18102 | 1 | 60 | 256,438 |
| 17450 | 8 | 46 | 187,322 |
| 14911 | 1 | 201 | 132,459 |
| 12415 | 24 | 21 | 123,725 |
| 14156 | 10 | 55 | 113,215 |

Nhận xét:

Khách `14911` có **201 hóa đơn** — nổi bật trong bảng 10 khách Monetary cao nhất, nhưng không phải tần suất mua cao nhất cả nhóm Champions (khách `12748` có 209 hóa đơn, cũng thuộc Champions). Khách `14646` dẫn đầu về Monetary và có Recency chỉ 2 ngày.

---

## 14.6. Quốc gia nào đóng góp doanh thu nhiều nhất?

| Hạng | Quốc gia | Gross Revenue |
|---|---|---|
| 1 | United Kingdom | 9,001,744 |
| 2 | Netherlands | 285,446 |
| 3 | EIRE | 283,141 |
| 4 | Germany | 228,678 |
| 5 | France | 209,625 |
| 6 | Australia | 138,454 |
| 7 | Spain | 61,559 |
| 8 | Switzerland | 57,068 |
| 9 | Belgium | 41,196 |
| 10 | Sweden | 38,368 |

Nhận xét:

United Kingdom chiếm khoảng **84.6%** gross revenue. Khoảng cách giữa UK và các nước còn lại rất lớn nên biểu đồ dùng thang logarit để thể hiện rõ sự khác biệt.

---

## 14.7. Khách hàng nào đã lâu không quay lại mua hàng?

Nhóm Lost và At Risk gồm **1,692 khách**.

Những khách có Recency lớn nhất (lên tới 374 ngày) hầu hết chỉ mua 1 lần với giá trị nhỏ:

| CustomerID | Segment | Recency (ngày) | Frequency | Monetary |
|---|---|---|---|---|
| 18074 | Lost | 374 | 1 | 489.60 |
| 14729 | Lost | 374 | 1 | 313.49 |
| 17968 | Lost | 374 | 1 | 265.10 |

---

## 14.8. Sản phẩm nào thường xuyên xuất hiện trong các đơn bị hủy?

Để phân tích khách quan cả về mặt tần suất hủy lẫn tác động tài chính thực tế, nhóm xây dựng 2 bảng xếp hạng độc lập (dữ liệu từ `reports/tables/cancelled_products.csv` và `reports/tables/cancelled_products_by_value.csv`):

**Top 10 theo số lượng hóa đơn hủy (Tần suất hủy cao nhất):**

| Hạng | Sản phẩm (Mã) | Số hóa đơn hủy | Giá trị hủy (GBP) |
|---|---|---|---|
| 1 | Manual (`M`) | 223 | 146,784.46 |
| 2 | REGENCY CAKESTAND 3 TIER (`22423`) | 180 | 9,697.05 |
| 3 | POSTAGE (`POST`) | 124 | 11,871.24 |
| 4 | JAM MAKING SET WITH JARS (`22960`) | 87 | 1,012.79 |
| 5 | SET OF 3 CAKE TINS PANTRY DESIGN (`22720`) | 73 | 730.10 |
| 6 | Discount (`D`) | 65 | 5,696.22 |
| 7 | STRAWBERRY CERAMIC TRINKET BOX (`21232`) | 57 | 442.00 |
| 8 | ROSES REGENCY TEACUP AND SAUCER (`22699`) | 54 | 1,150.35 |
| 9 | POPCORN HOLDER (`22197`) | 50 | 366.55 |
| 10 | RECIPE BOX PANTRY YELLOW DESIGN (`22666`) | 47 | 421.05 |

**Top 10 theo giá trị tiền hoàn trả (Tác động tài chính lớn nhất):**

| Hạng | Sản phẩm (Mã) | Số hóa đơn hủy | Giá trị hủy (GBP) |
|---|---|---|---|
| 1 | AMAZON FEE (`AMAZONFEE`) | 32 | 235,281.59 |
| 2 | PAPER CRAFT , LITTLE BIRDIE (`23843`) | 1 | 168,469.60 |
| 3 | Manual (`M`) | 223 | 146,784.46 |
| 4 | MEDIUM CERAMIC TOP STORAGE JAR (`23166`) | 10 | 77,479.64 |
| 5 | POSTAGE (`POST`) | 124 | 11,871.24 |
| 6 | REGENCY CAKESTAND 3 TIER (`22423`) | 180 | 9,697.05 |
| 7 | CRUK Commission (`CRUK`) | 16 | 7,933.43 |
| 8 | Bank Charges (`BANK CHARGES`) | 25 | 7,340.64 |
| 9 | WHITE HANGING HEART T-LIGHT HOLDER (`85123A`) | 42 | 6,624.30 |
| 10 | FAIRY CAKE FLANNEL ASSORTED COLOUR (`21108`) | 3 | 6,591.42 |

Nhận xét:

- **Hai góc nhìn bổ trợ cho nhau:** Bảng tần suất phản ánh những mặt hàng hay gặp trục trặc khi đặt mua (sản phẩm thật bị hủy nhiều nhất là *REGENCY CAKESTAND 3 TIER* với 180 hóa đơn), trong khi bảng giá trị hoàn trả phản ánh các giao dịch cá biệt làm biến động dòng tiền (chủ yếu là chi phí sàn Amazon Fee, đơn hàng số lượng khủng của khách bán sỉ hoặc điều chỉnh Manual).
- Biểu đồ đối chiếu trực quan được lưu tại `reports/figures/cancelled_products.png`.

---

## 14.9. Phân phối giá trị đơn hàng

| Chỉ số | Giá trị |
|---|---|
| Min | 0.38 |
| Q1 | 151.70 |
| Median | 303.30 |
| Mean | 533.17 |
| Q3 | 493.46 |
| Max | 168,469.60 |

Nhận xét:

Mean (533.17) lớn hơn đáng kể so với Median (303.30), phản ánh phân phối lệch phải: phần lớn đơn hàng có giá trị vừa phải nhưng tồn tại một số đơn rất lớn kéo trung bình lên. Đây là bằng chứng trực quan bổ sung cho kết quả phát hiện outlier ở phần 11.

---

## 14.10. Phân tích giữ chân khách hàng (Cohort Retention Analysis)

Để trả lời câu hỏi cốt lõi về **tính bền vững của doanh nghiệp**: *"Khách hàng sau khi mua lần đầu có tiếp tục quay lại trong các tháng tiếp theo hay không?"*, nhóm thực hiện phân tích Cohort Retention trên toàn bộ các khách hàng định danh.

Nhóm khách hàng (Cohort) được xác định bằng **tháng mua hàng đầu tiên** (`CohortMonth`). Tỷ lệ giữ chân (`Retention Rate`) được tính bằng tỷ lệ phần trăm số khách hàng trong cohort đó tiếp tục có phát sinh giao dịch mua hàng ở tháng thứ $N$ ($M+N$).

Dữ liệu ma trận được lưu tại `reports/tables/cohort_retention.csv`:

| Cohort | Quy mô (M0) | M+1 | M+2 | M+3 | M+4 | M+5 | M+6 | M+7 | M+8 | M+9 | M+10 | M+11 | M+12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **2010-12** | 100% | **36.6%** | 32.3% | 38.4% | 36.3% | 39.8% | 36.3% | 34.9% | 35.4% | 39.5% | 37.4% | **50.3%** | 26.6% |
| **2011-01** | 100% | 22.1% | 26.6% | 23.0% | 32.1% | 28.8% | 24.7% | 24.2% | 30.0% | 36.5% | 11.8% | — | — |
| **2011-02** | 100% | 18.7% | 18.7% | 28.4% | 27.1% | 24.7% | 25.3% | 27.9% | 29.5% | 6.8% | — | — | — |
| **2011-03** | 100% | 15.0% | 25.2% | 19.9% | 22.3% | 16.8% | 26.8% | 23.0% | 7.7% | — | — | — | — |
| **2011-04** | 100% | 21.3% | 20.3% | 21.0% | 19.7% | 22.7% | 21.7% | 26.0% | 8.3% | — | — | — | — |
| **2011-05** | 100% | 19.0% | 17.3% | 17.3% | 20.8% | 23.2% | 26.4% | 9.5% | — | — | — | — | — |
| **2011-06** | 100% | 17.4% | 15.7% | 26.4% | 23.1% | 33.5% | 9.5% | — | — | — | — | — | — |
| **2011-07** | 100% | 18.1% | 20.7% | 22.3% | 27.1% | 11.2% | — | — | — | — | — | — | — |
| **2011-08** | 100% | 20.7% | 24.9% | 24.3% | 12.4% | — | — | — | — | — | — | — | — |
| **2011-09** | 100% | 23.4% | 30.1% | 11.4% | — | — | — | — | — | — | — | — | — |
| **2011-10** | 100% | 24.0% | 11.5% | — | — | — | — | — | — | — | — | — | — |
| **2011-11** | 100% | 11.1% | — | — | — | — | — | — | — | — | — | — | — |
| **2011-12** | 100% | — | — | — | — | — | — | — | — | — | — | — | — |

**Nhận xét sâu về hành vi giữ chân khách hàng:**
1. **Hiện tượng Drop-off sau tháng đầu tiên:** Ngay sau tháng gia nhập ($M+1$), tỷ lệ khách quay lại sụt giảm mạnh xuống còn khoảng **15% – 36.6%**. Điều này cho thấy đa số khách hàng là người mua vãng lai một lần.
2. **Khách hàng cốt lõi ổn định ($M+2$ đến $M+10$):** Sau cú rơi ban đầu, tỷ lệ retention đi ngang và duy trì rất vững ở mức **20% – 30%**. Đây chính là tập khách hàng thân thiết đóng góp phần lớn doanh thu ổn định cho nhà bán lẻ.
3. **Hiệu ứng mùa vụ tháng 11/2011:** Ở cột tháng 11/2011 (tương ứng với các mốc $M+11$ của cohort 2010-12, $M+9$ của cohort 2011-01,...), tỷ lệ quay lại vọt lên **50.3%** và **36.5%**, chứng minh sức hút mạnh mẽ của mùa mua sắm cuối năm đối với ngay cả những khách hàng cũ đã lâu không hoạt động.
4. Biểu đồ nhiệt (Heatmap) thể hiện ma trận giữ chân được lưu tại `reports/figures/cohort_retention_heatmap.png`.

---

# 15. Kết luận tổng hợp

## 15.1. Bảng kết quả tổng hợp 8 câu hỏi nghiên cứu & phân tích mở rộng

| Chỉ tiêu / Câu hỏi nghiên cứu | Kết quả thực nghiệm cốt lõi |
|---|---|
| **1. Doanh thu theo thời gian** | Đạt đỉnh vào tháng 11/2011 với 1.50M GBP; ba tháng 9–11 chiếm 34.9% gross revenue; thị trường UK là động lực chính tạo nên đợt bùng nổ cuối năm. |
| **2. Sản phẩm bán nhiều nhất** | *PAPER CRAFT, LITTLE BIRDIE* (80,995 đơn vị) và *MEDIUM CERAMIC TOP STORAGE JAR* (78,033 đơn vị) — các đơn đột biến này đều có phát sinh hoàn hủy lớn. |
| **3. Sản phẩm doanh thu cao nhất** | Khi loại mã phí vận chuyển (`DOTCOM POSTAGE` 206K), **REGENCY CAKESTAND 3 TIER** đứng đầu với **174,157 GBP**. |
| **4. Phân khúc giá chủ lực** | Phân khúc **Low** (≤ 1.25 GBP) đạt lượng bán lớn nhất (2.9M đơn vị); phân khúc **Premium** (> 4.13 GBP) đóng góp doanh thu cao nhất (3.8M GBP). |
| **5. Khách hàng VIP (Champions)** | ID `14646` đứng đầu chi tiêu ròng (279K GBP, 73 hóa đơn); ID `14911` (201 hóa đơn) và ID `12748` (209 hóa đơn) có tần suất mua sắm dày đặc nhất. |
| **6. Địa lý đóng góp doanh thu** | **United Kingdom** đóng góp 84.6% doanh thu (9.0M GBP); các nước ngoài UK duy trì ổn định đều đặn từ 100k–220k GBP/tháng. |
| **7. Khách hàng có nguy cơ rời bỏ** | 2,180 khách hàng thuộc nhóm Lost và At Risk; thời gian không quay lại (Recency) dài nhất lên tới 374 ngày. |
| **8. Sản phẩm trong đơn hủy** | Tần suất hủy cao nhất: *Manual* (223 đơn), *REGENCY CAKESTAND 3 TIER* (180 đơn); Giá trị hủy lớn nhất: *AMAZON FEE* (235K GBP), *PAPER CRAFT* (168K GBP). |
| **9. Tương quan hành vi RFM** | Tần suất (Frequency) và Chi tiêu (Monetary) tương quan thuận mạnh ($r=0.43$); biểu đồ phân tán phân cụm rất mạch lạc. |
| **10. Tỷ lệ giữ chân (Cohort Retention)** | Tỷ lệ quay lại tháng đầu ($M+1$) giảm về 18%–38%; duy trì ổn định 20%–25% ở các tháng tiếp theo; bật tăng mạnh vào tháng 11/2011. |

## 15.2. Insight kinh doanh chuyên sâu

1. **Hiệu ứng Pareto rõ nét:** Nhóm Champions chiếm ~29.8% số khách nhưng đóng góp tới **~75.2% Monetary ròng trong RFM** (~63.9% net revenue toàn bộ dataset). Doanh nghiệp phụ thuộc lớn vào nhóm khách hàng hạt nhân này.
2. **Khách hàng quốc tế là "mỏ neo" ổn định:** Khác với sự trồi sụt theo mùa vụ của thị trường nội địa UK, doanh thu Non-UK duy trì đều đặn 100k–220k GBP mỗi tháng, đóng vai trò giảm thiểu rủi ro dòng tiền trong các tháng thấp điểm đầu năm.
3. **Cú sốc tỷ lệ giữ chân tháng đầu ($M+1$):** Khoảng 65% – 80% khách hàng mới không bao giờ quay lại sau đơn hàng đầu tiên. Tuy nhiên, nhóm vượt qua được mốc $M+1$ sẽ có xu hướng gắn bó rất lâu dài (duy trì 20%–30% suốt cả năm).
4. **Mâu thuẫn giữa quy mô bán và rủi ro hủy hàng:** Những mặt hàng bán chạy nhất (như *REGENCY CAKESTAND* hay *PAPER CRAFT*) lại chính là những mặt hàng nằm trong top đầu về số lượng và giá trị hủy đơn, đặt ra dấu hỏi lớn về khâu đóng gói, vận chuyển hàng dễ vỡ và chính sách bán buôn.

## 15.3. Đề xuất hành động chiến lược

- **Chiến lược VIP Loyalty cho nhóm Champions:** Cung cấp hạn mức tín dụng ưu đãi, quản lý tài khoản riêng (Dedicated Account Manager), và dịch vụ giao hàng ưu tiên để bảo vệ 75% dòng tiền cốt lõi.
- **Chiến dịch Onboarding & Kích hoạt lần mua thứ hai ($M+1$):** Do tỷ lệ rơi rụng ở tháng đầu tiên là cao nhất, marketing cần tự động gửi email hướng dẫn, khảo sát trải nghiệm và voucher giảm giá lần 2 trong vòng 14–21 ngày kể từ lần mua đầu.
- **Kế hoạch Win-back cho nhóm At Risk:** Tiếp cận 862 khách hàng At Risk bằng các ưu đãi phục hồi trước khi thời gian vắng mặt vượt quá 120 ngày (ngưỡng chuyển dịch sang nhóm Lost).
- **Chuẩn bị chuỗi cung ứng quý 4:** Tăng công suất kho bãi, nhân sự vận hành và ngân sách quảng cáo từ tháng 8–9 để đón đầu đợt sóng mua sắm tháng 9–11 (giai đoạn đóng góp hơn 1/3 doanh thu cả năm).
- **Cải tiến quy trình đóng gói và chính sách bán buôn:** Rà soát lại quy cách vận chuyển dòng sản phẩm gốm sứ / kệ bánh *REGENCY CAKESTAND* nhằm hạ thấp tỷ lệ hủy (180 hóa đơn hủy), giảm thiểu tổn thất vận hành.

---

# 16. Giới hạn của phân tích

Các điểm sau phản ánh phạm vi và giới hạn của nghiên cứu, cần lưu ý khi áp dụng vào thực tế:

1. **Doanh thu phân tích tổng quát là Gross Revenue:** Phân tích doanh thu theo thời gian, quốc gia và sản phẩm chỉ tính các giao dịch bán hàng bình thường. Giá trị hủy (~893,980 GBP, ~8.4% gross) chỉ được cấn trừ trong Monetary của bảng RFM, chưa áp dụng khấu trừ hồi tố ở từng dòng hóa đơn.
2. **24.8% giao dịch thiếu CustomerID:** Có 132,565 dòng giao dịch không có mã khách hàng, buộc phải loại khỏi mô hình RFM và Cohort. Mô hình chỉ đại diện cho 4,338 khách hàng định danh.
3. **Dữ liệu tháng 12/2011 không trọn vẹn:** Tập dữ liệu kết thúc vào ngày 09/12/2011, do đó mức sụt giảm ở tháng 12 không phản ánh thực tế kinh doanh cả tháng.
4. **Giới hạn thời gian khảo sát (~1 năm):** Dataset chỉ bao gồm 12 tháng trọn vẹn và 1 tháng lẻ, do đó nhận định về tính mùa vụ cần được kiểm chứng thêm qua dữ liệu nhiều năm liên tiếp.
5. **Đặc thù thị trường Anh:** UK chiếm gần 85% tổng doanh thu, do đó các quy luật rút ra chủ yếu phản ánh hành vi tiêu dùng và bán buôn tại Vương quốc Anh.
6. **Mã phí và nghiệp vụ phi sản phẩm (`IsNonProduct`):** Chiếm ~3.7% doanh thu bán hàng. Pipeline đã tạo cờ đánh dấu riêng biệt; các phân tích chi tiết sản phẩm cần lưu ý loại trừ để tránh nhầm lẫn phí vận chuyển với hàng hóa thương mại.