# Báo cáo insight — Phân tích bán lẻ online

**Môn học:** PSD301M · **Nhóm:** Trí Dũng, Tuấn Triển

**Mục tiêu:** Xác định khách hàng và sản phẩm tạo doanh thu cao, phân tích giao dịch bất thường và hoàn hủy trên UCI Online Retail.

Books to Scrape là bài thực hành requests/BeautifulSoup riêng, không dùng để kết luận về giao dịch UCI.

Các kết quả dưới đây được tính từ `cleaned_retail.csv` và `customer_segments.csv`. Doanh thu sản phẩm, tháng và quốc gia chỉ dùng dòng bán (gross). Xếp hạng mã hàng giữ phí và dịch vụ; xếp hạng hàng hóa loại các mã có cờ IsNonProduct.

## 1. Doanh thu theo thời gian

Tháng có gross revenue cao nhất là `2011-11` với £1,503,866.78. Tháng 2011-12 chỉ có dữ liệu đến 09/12/2011; không so trực tiếp với tháng trọn vẹn.
Tổng gross £10,642,110.80, hoàn hủy £893,979.73, net £9,748,131.07. Dashboard ghi hoàn hủy vào tháng phát sinh hóa đơn hủy.

## 2. Sản phẩm bán nhiều nhất

`PAPER CRAFT , LITTLE BIRDIE` (`23843`) có tổng lượng bán gross cao nhất trong hàng hóa: 80,995 đơn vị. Lượng bán ban đầu vẫn được tính vào gross dù có hoàn hủy về sau.

## 3. Sản phẩm tạo doanh thu cao nhất

`REGENCY CAKESTAND 3 TIER` (`22423`) đứng đầu trong hàng hóa theo gross revenue: £174,156.54. Nếu xét toàn bộ mã hàng, mã đứng đầu là `DOTCOM POSTAGE` với £206,248.77.

## 4. Phân khúc giá có lượng mua cao nhất

Phân khúc `Low` có Quantity cao nhất: 2,887,471. Các phân khúc được xác định bằng tứ phân vị UnitPrice: Q1=1.25, Median=2.08, Q3=4.13.
Bảng này mô tả đơn giá của các dòng bán, bao gồm mã phí nếu có.

## 5. Khách hàng chi tiêu nhiều và mua thường xuyên

Trong nhóm Champions, CustomerID `14646` có Monetary cao nhất: 279,489.02, Frequency=73 hóa đơn bán. Champions chiếm 75.2% tổng Monetary của khách trong RFM.

## 6. Quốc gia đóng góp doanh thu nhiều nhất

`United Kingdom` có gross revenue cao nhất: £9,001,744.09 (84.6% gross).

## 7. Khách hàng lâu không quay lại

Lost và At Risk có 2,180 khách. CustomerID `18074` có Recency lớn nhất trong hai nhóm: 374 ngày. Đây là phân nhóm theo quy tắc RFM, không phải dự báo rời bỏ.

## 8. Sản phẩm thường xuất hiện trong đơn bị hủy

`Manual` (`M`) xuất hiện trong 223 hóa đơn hủy, cao nhất trong tất cả mã. Trong hàng hóa, `REGENCY CAKESTAND 3 TIER` xuất hiện trong 180 hóa đơn hủy. `AMAZON FEE` dẫn đầu theo giá trị hủy: £235,281.59. Các số đếm trên không phải tỷ lệ đơn bán bị hủy.

## Tương quan RFM và cohort

- Pearson Frequency–Monetary trên R/F/M gốc: 0.576. Tương quan không xác định nhân quả. Scatter log1p không vẽ 8 khách Monetary âm; họ vẫn nằm trong bảng và ma trận tương quan.
- Có 1,728 khách không mua ở M+1 nhưng mua từ M+2 trở đi trong kỳ quan sát. Vì vậy, vắng mặt ở M+1 không đồng nghĩa không bao giờ quay lại.
- Cohort dựa trên tháng mua đầu quan sát được. CSV lưu tỷ lệ 0–1; 0 là kỳ đã quan sát nhưng không có lượt mua lại, ô trống là ngoài kỳ quan sát. Tháng 2011-12 chỉ có dữ liệu đến 09/12/2011; không so trực tiếp với tháng trọn vẹn.

## Phạm vi

Dòng thiếu CustomerID vẫn được tính vào tổng doanh thu, nhưng không dùng cho RFM và cohort. Monetary giữ giá trị thực sau hoàn hủy, kể cả âm. Dữ liệu chỉ bao phủ khoảng một năm và không có chi phí, dòng tiền hay lý do hoàn trả. Outlier được gắn cờ để xem xét, không tự động loại.

## Đề xuất cần kiểm chứng

- **Chăm sóc Champions:** Tỷ trọng Monetary cao trong RFM gợi ý một nhóm ưu tiên thử chương trình chăm sóc. Đo mua lại và giá trị sau hoàn hủy, không suy ra lợi nhuận hay khả năng cấp tín dụng.
- **Khách chưa mua lại:** Có thể thử nhắc mua lần hai hoặc win-back. Mốc 120 ngày là đề xuất thử nghiệm, không phải ngưỡng chuyển sang Lost.
- **Hoàn hủy hàng hóa:** `REGENCY CAKESTAND 3 TIER` có nhiều hóa đơn hủy; chưa có mẫu số và lý do hủy để kết luận rủi ro hay nguyên nhân. Cần bổ sung dữ liệu liên kết giao dịch và lý do hoàn trả trước khi đề xuất thay đổi vận hành.

Nguồn đối chiếu: các bảng trong `reports/tables/`, dữ liệu RFM và notebook chạy chung pipeline. Báo cáo này được tạo lại bằng `python main.py`.
