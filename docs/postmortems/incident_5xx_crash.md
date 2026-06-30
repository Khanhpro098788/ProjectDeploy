# Incident Postmortem: Lỗi HTTP 5xx trên FastAPI Service (Môi trường Dev)

**Ngày xảy ra sự cố:** 30/06/2026  
**Chủ trì báo cáo:** Huy (DevOps Engineer)  
**Trạng thái:** Đã khắc phục  

---

## 1. Tóm tắt sự cố (Summary)
Vào lúc 03:24:27 AM UTC (10:24:27 AM giờ địa phương Việt Nam) ngày 30/06/2026, hệ thống giám sát đã kích hoạt cảnh báo lỗi HTTP 5xx trên dịch vụ Cloud Run `fastapi-service-dev`. Tổng cộng có 12 yêu cầu bị lỗi 500 liên tiếp từ phía client. Sự cố kéo dài trong khoảng 1 phút và đã tự phục hồi sau khi client ngừng gửi request lỗi. Không có ảnh hưởng nghiêm trọng tới dữ liệu người dùng.

## 2. Dòng thời gian sự cố (Timeline)
* **03:24:27 UTC:** Client bắt đầu gửi request lỗi vào endpoint `/crash` để thử nghiệm.
* **03:24:30 UTC:** 12 request lỗi liên tiếp được ghi nhận trong logs.
* **03:30:00 UTC:** Hệ thống Google Cloud Alerting quét metric và gửi Email cảnh báo (mất khoảng 5 phút trễ do chu kỳ đánh giá của GCP).
* **03:30:10 UTC:** Kỹ sư vận hành nhận được email cảnh báo, truy cập Logs Explorer qua liên kết Runbook để chẩn đoán.
* **03:31:00 UTC:** Xác nhận lỗi do client cố tình gọi endpoint `/crash` phục vụ mục đích kiểm thử. Sự cố kết thúc.

## 3. Phân tích nguyên nhân gốc rễ (Root Cause Analysis - 5 Whys)
1. *Tại sao người dùng nhận lỗi 500?* -> Vì ứng dụng FastAPI trả về lỗi "Internal Server Error".
2. *Tại sao FastAPI trả về lỗi Internal Server Error?* -> Vì code tại endpoint `/crash` thực hiện phép toán chia cho 0 (`1 / 0`).
3. *Tại sao phép toán chia cho 0 lại được thực thi?* -> Vì lập trình viên đã cố tình viết endpoint `/crash` để phục vụ việc test Alerting.
4. *Tại sao endpoint thử nghiệm nguy hiểm này lại có thể truy cập được từ môi trường dev?* -> Vì chưa có cơ chế ẩn hoặc tắt các endpoint thử nghiệm khi deploy ứng dụng lên môi trường cloud.

## 4. Hành động khắc phục & Ngăn ngừa (Action Items)
- [ ] **Action Item 1 (Ngắn hạn):** Khóa endpoint `/crash` hoặc thêm middleware bắt ngoại lệ (Exception Handling) toàn cục để trả về thông báo thân thiện hơn thay vì crash cả request.
- [ ] **Action Item 2 (Dài hạn):** Cấu hình để các endpoint thử nghiệm (như `/crash`) chỉ hoạt động trong môi trường LOCAL và tự động bị vô hiệu hóa khi deploy lên Cloud Run.
