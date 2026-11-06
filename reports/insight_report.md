# Báo cáo Insight — Phân tích khách hàng và sản phẩm trong bán lẻ online

**Môn học:** PSD301M | **Nhóm:** Trí Dũng, Tuấn Triển  
**Dữ liệu:** UCI Online Retail (541,909 dòng, 12/2010–12/2011)

---

## 1. Mục tiêu và câu hỏi nghiên cứu

Phân tích giao dịch bán lẻ online nhằm trả lời: *Nhóm khách hàng và sản phẩm nào tạo doanh thu cao, và các đơn hàng có xuất hiện dấu hiệu bất thường hoặc hủy giao dịch hay không?*

Tám câu hỏi phụ: doanh thu theo thời gian, sản phẩm bán nhiều nhất, sản phẩm doanh thu cao nhất, phân khúc giá, khách chi tiêu cao & mua thường xuyên, quốc gia đóng góp nhiều nhất, khách lâu không quay lại, sản phẩm hay bị hủy.

---

## 2. Nguồn dữ liệu

**UCI Online Retail** — dữ liệu giao dịch thật của một doanh nghiệp bán lẻ online UK, 541,909 dòng × 8 thuộc tính. Đủ dữ liệu để thực hiện phân tích RFM, doanh thu và phát hiện hủy đơn.

**Books to Scrape** — 1,000 sách thu thập bằng `requests` + `BeautifulSoup` (thực hành kỹ thuật web scraping theo Option B của rubric). Dữ liệu này không dùng trong phân tích chính.

---

## 3. Quy trình phân tích

- **Data Profiling:** 1,454 dòng thiếu Description; 135,080 (24.9%) thiếu CustomerID; 5,268 dòng trùng lặp; 10,624 Quantity âm.
- **Data Cleaning:** loại trùng lặp (−5,268), loại UnitPrice ≤ 0 (−2,512), giữ đơn hủy để phân tích riêng → **534,129 dòng** sau cleaning. Thêm cột `IsCancelled`, `OrderMonth`, `Revenue`, `IsNonProduct`.
- **Cấu trúc dữ liệu Python:** List (invoice_records), Dict (country_summary), Set (product_codes), Tuple (date_range).
- **Lớp OOP:** `RetailDataProcessor` đóng gói toàn bộ pipeline load → clean → RFM.
- **NumPy / IQR:** thống kê mô tả và phát hiện outlier trên Revenue, Quantity, UnitPrice.
- **RFM Customer Segmentation:** Recency, Frequency, Monetary (đã trừ giá trị hủy). Điểm 1–4 theo percentile, gán 5 phân khúc.
- **EDA:** 8 câu hỏi nghiên cứu, 9+ bảng kết quả, 10+ biểu đồ.
- **Validation:** 15 phép kiểm tra tự động — tất cả 0 lỗi.

---

## 4. Kết quả chính

| Câu hỏi | Insight | Con số |
|---|---|---|
| Doanh thu theo thời gian | Đỉnh tháng 11/2011; mùa cuối năm (tháng 9–11) chiếm ~34.9% gross revenue | 1,503,867 GBP |
| Sản phẩm bán nhiều nhất | REGENCY CAKESTAND 3 TIER dẫn đầu khi gộp đúng theo StockCode; hai đơn hủy bất thường (80,995 và 74,215 chiếc) làm sai lệch xếp hạng thô | — |
| Sản phẩm doanh thu cao nhất | REGENCY CAKESTAND 3 TIER (174,157 GBP) sau khi loại mã phí | 174,157 GBP |
| Phân khúc giá | Low (≤ 1.25 GBP) có lượng mua nhiều nhất; Premium (> 4.13 GBP) đóng góp doanh thu cao nhất | 3.8M GBP |
| Khách hàng giá trị cao | Champions (29.8% khách) tạo ~75.2% tổng Monetary RFM | 1,291 khách |
| Quốc gia dẫn đầu | United Kingdom chiếm 84.6% gross revenue | 9,001,744 GBP |
| Khách lâu không quay lại | 1,692 khách Lost + At Risk; Recency lớn nhất 374 ngày | 862 At Risk |
| Sản phẩm hay bị hủy | REGENCY CAKESTAND 3 TIER: 180 hóa đơn hủy; AMAZON FEE: giá trị hủy lớn nhất (235,281 GBP) | — |

---

## 5. Đề xuất hành động

- **Champions:** duy trì loyalty program và ưu đãi cá nhân hóa — nhóm này tạo ~75% Monetary RFM.
- **At Risk (862 khách):** triển khai win-back campaign (email/voucher) trước khi Recency vượt 120 ngày.
- **Mùa vụ:** chuẩn bị tồn kho và marketing từ tháng 8–9 cho giai đoạn cao điểm tháng 9–11.
- **REGENCY CAKESTAND 3 TIER:** điều tra nguyên nhân 180 hóa đơn hủy dù thuộc top doanh thu.

---

## 6. Giới hạn của phân tích

1. **Doanh thu gross** — phân tích sản phẩm/tháng/quốc gia chưa trừ giá trị hủy (~8.4%).
2. **~25% dòng thiếu CustomerID** — RFM chỉ bao phủ 4,338 khách xác định được.
3. **Dữ liệu 1 năm** — chưa đủ để kết luận chắc chắn về tính mùa vụ.
4. **Tháng 12/2011 chưa đầy đủ** (đến ngày 09/12) — không so sánh thẳng với các tháng khác.
5. **Mã phí lẫn trong dữ liệu sản phẩm** — đã gắn cờ `IsNonProduct`, loại khỏi các phân tích sản phẩm.
6. **UK chiếm 84.6%** — kết luận chủ yếu phản ánh thị trường Anh.
