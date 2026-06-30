# Production Readiness Checklist (PRR) - FastAPI API

Bảng tự đánh giá mức độ sẵn sàng vận hành của hệ thống trước khi Go-live môi trường Production.

## 1. Bảo mật & IAM (Security & Access Control)
- [x] **Least Privilege IAM SA:** Các Service Account (`github-ci-sa` và `cloudrun-runtime-sa`) được phân tách quyền rõ ràng. `github-ci-sa` chỉ có quyền deploy và push ảnh, `cloudrun-runtime-sa` chỉ có quyền ghi logs.
- [x] **Workload Identity Federation (WIF):** Hoàn thành tích hợp trong GitHub Actions (`ci.yml`), loại bỏ hoàn toàn các file JSON Key tĩnh để tránh rò rỉ thông tin xác thực.
- [x] **Private Service & Ingress:** Cloud Run Backend đã cấu hình không cho phép truy cập vô danh (`--no-allow-unauthenticated`) và chặn rào Ingress ở mức `internal` (Day 12).
- [x] **Secret Management:** Môi trường local đã được chuyển sang quản lý tập trung qua file `.env` (được chặn bởi `.gitignore`) và môi trường CI/CD sử dụng GitHub Secrets.

## 2. Khả năng quan sát (Observability)
- [x] **Structured Log:** Log ứng dụng (`src/main.py`) sử dụng thư viện `google-cloud-logging` ghi log dạng JSON thông minh, tự động bóc tách Trace ID từ header `X-Cloud-Trace-Context`.
- [x] **Alert Policies:** Khai báo hoàn toàn bằng IaC (`sst.config.ts`) bao gồm: cảnh báo lỗi nghiêm trọng (HTTP 5xx) và hiệu năng chậm (p95 Latency > 2s).
- [x] **Performance Dashboard:** Dựng tự động bằng code Dashboard hiển thị trực quan các chỉ số Traffic và Latency.
- [x] **Runbooks:** Đã thiết lập Sổ tay vận hành tại `docs/runbooks/alert_5xx.md` và đính kèm trực tiếp link hướng dẫn vào nội dung mail cảnh báo.

## 3. Vận hành & Độ tin cậy (Reliability & Operations)
- [x] **Auto-scaling:** Cloud Run mặc định tự động co giãn số lượng instances dựa trên tải lượng CPU.
- [x] **Rollback Flow:** Đã lên tài liệu chi tiết quy trình quay lui (Rollback) bằng cách điều hướng Traffic trên GCP Console hoặc Revert Commit trên Git (Day 7).
- [x] **IaC (SST):** Tài nguyên Cloud Run và hệ thống giám sát đã được code hóa thành công trong `sst.config.ts`.

## 4. Hiệu năng & Kiểm thử (Performance & Testing)
- [x] **Unit Tests:** Hệ thống kiểm thử tự động với `pytest` đã được cấu hình chạy trong job `test-python-code` của GitHub Actions.
- [ ] **Failure Testing:** **CHƯA ĐẠT (TODO)**. Hệ thống chưa được kiểm thử trong điều kiện thực tế bị phá hủy (như giả lập crash app, giả lập lỗi cấu hình, mất quyền IAM) để kiểm chứng xem Alert và Runbook hoạt động có chính xác không. Đây là nhiệm vụ trọng tâm của Day 18.