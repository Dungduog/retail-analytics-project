# EDA Results

Các kết quả dưới đây được tính từ `cleaned_retail.csv` và `customer_segments.csv`. Doanh thu sản phẩm, tháng và quốc gia chỉ dùng normal sales; cancellation được phân tích riêng.

## 1. Doanh thu theo thời gian

Tháng có gross revenue cao nhất là `2011-11` với 1,503,866.78.

## 2. Sản phẩm bán nhiều nhất

`PAPER CRAFT , LITTLE BIRDIE` (`23843`) có tổng Quantity cao nhất: 80,995.

## 3. Sản phẩm tạo doanh thu cao nhất

`DOTCOM POSTAGE` (`DOT`) đứng đầu theo Revenue: 206,248.77. Kết quả giữ nguyên các mã phí/dịch vụ có trong dataset; chưa tự động loại chúng.

## 4. Phân khúc giá có lượng mua cao nhất

Phân khúc `Low` có Quantity cao nhất: 2,887,471. Các phân khúc được xác định bằng tứ phân vị UnitPrice: Q1=1.25, Median=2.08, Q3=4.13.

## 5. Khách hàng chi tiêu nhiều và mua thường xuyên

Trong nhóm Champions, CustomerID `14646` có Monetary cao nhất: 279,489.02, Frequency=73.

## 6. Quốc gia đóng góp doanh thu nhiều nhất

`United Kingdom` có gross revenue cao nhất: 9,001,744.09.

## 7. Khách hàng lâu không quay lại

CustomerID `18074` có Recency lớn nhất trong nhóm Lost/At Risk: 374 ngày.

## 8. Sản phẩm thường xuất hiện trong đơn bị hủy

`Manual` (`M`) xuất hiện trong 223 cancellation invoices, cao nhất theo tiêu chí này.

## Phạm vi

EDA này không thêm dữ liệu ngoài dataset và không tự động xóa outlier, mã phí hoặc nghiệp vụ nội bộ. Các file chi tiết nằm trong `reports/tables/`; biểu đồ nằm trong `reports/figures/`.
