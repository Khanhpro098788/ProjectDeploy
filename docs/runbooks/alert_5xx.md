# Runbook: Xử lý sự cố lỗi HTTP 5xx liên tục

## 1. Mô tả sự cố
Hệ thống API phát sinh lỗi HTTP 5xx (Internal Server Error) vượt quá ngưỡng cho phép liên tục trong 1 phút. Cảnh báo này cho thấy hệ thống đang gặp lỗi nghiêm trọng từ phía máy chủ (Backend API) khiến người dùng không thể thực hiện các thao tác mong muốn.

## 2. Các bước chẩn đoán nhanh (Triage Steps)
1. **Truy cập Logs Explorer:**
   * Mở giao diện **Google Cloud Console** -> **Logging** -> **Logs Explorer**.
2. **Lọc thông tin Logs:**
   * Nhập câu lệnh truy vấn dưới đây vào khung tìm kiếm và nhấn **Run query**:
     ```text
     resource.type="cloud_run_revision"
     resource.labels.service_name="fastapi-service-dev"
     severity>=ERROR
     ```
3. **Phân tích lỗi:**
   * Kiểm tra các dòng log có mã trạng thái `status_code >= 500`.
   * Trích xuất giá trị `trace` ID (Trace context) để lọc toàn bộ vòng đời của request bị lỗi nhằm tìm ra chính xác dòng code hoặc hàm gây lỗi.

## 3. Các bước khắc phục tạm thời (Mitigation Steps)
1. **Trường hợp lỗi do Code mới deploy (nhân bản mới):**
   * Nếu sự cố bắt đầu xuất hiện ngay sau khi có đợt cập nhật code mới, thực hiện quay lui (Rollback) về phiên bản (Revision) hoạt động tốt trước đó:
     * Vào **Cloud Run** -> Chọn dịch vụ -> **Revisions** -> Chọn bản cũ ổn định -> **Manage Traffic** -> Chuyển 100% traffic về bản cũ.
     * Hoặc thực hiện `git revert` commit bị lỗi trên GitHub để CI/CD tự động deploy lại bản ổn định.
2. **Trường hợp lỗi do cạn kiệt tài nguyên:**
   * Nếu logs chỉ ra lỗi liên quan đến kết nối cơ sở dữ liệu (`Connection Timeout`) hoặc cạn kiệt CPU/RAM:
     * Kiểm tra biểu đồ giám sát tài nguyên của Cloud Run.
     * Tạm thời nâng cấu hình tài nguyên (vCPU/RAM) hoặc tăng giới hạn số lượng container instances (`max-instances`) để gánh tải.
