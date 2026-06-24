# FastAPI Demo API

**Mô tả ngắn:** Dự án triển khai FastAPI lên Google Cloud Run bằng Docker, GitHub Actions và SST.
**Phiên bản:** 1.0.0
**Trạng thái:** Hoàn thành Tuần 1 và Tuần 2
**Môi trường:** Development / Production
**Maintainer:** Khanh
**Repository:** ProjectDeploy
**Ngày cập nhật:** 24/06/2026

## 1. Giới thiệu tổng quan
Dự án cung cấp một RESTful API quản lý sản phẩm mẫu.
Mục tiêu chính là thực hành quy trình DevOps: đóng gói ứng dụng (Docker), tự động hóa CI/CD (GitHub Actions) và triển khai hạ tầng dưới dạng mã (IaC - SST) lên nền tảng Google Cloud.

## 2. Phạm vi và giới hạn
- **Nội dung thuộc phạm vi:** Đóng gói Docker, GitHub Actions CI/CD, cấu hình SST deploy lên Cloud Run, tạo mạng VPC cơ bản.
- **Nội dung ngoài phạm vi:** Cấu hình DNS domain tùy chỉnh, load balancer nâng cao.
- **Chức năng chưa hoàn thành:** [CẦN BỔ SUNG: chức năng còn thiếu]
- **Nội dung chưa được kiểm thử:** Tải trọng cao (Load testing).
- **Giới hạn development:** Dữ liệu lưu trong bộ nhớ (In-memory), sẽ mất khi container khởi động lại.
- **Giới hạn production:** Chưa kết nối cơ sở dữ liệu thực (PostgreSQL/MySQL).

## 3. Kiến trúc hệ thống và luồng hoạt động

```mermaid
flowchart LR
    Dev["Developer"] -->|git push| Git["GitHub Repository"]
    Git --> CI["GitHub Actions"]
    CI -->|Test| Pytest["Pytest"]
    CI -->|Build| Docker["Docker Image"]
    CI -->|Push| AR["Artifact Registry"]
    CI -->|Deploy| SST["SST IaC"]
    SST --> CR["Cloud Run"]
    Client["User"] -->|HTTPS| CR
```
**Luồng xử lý chính:**
1. Developer đẩy mã nguồn lên GitHub nhánh `main`.
2. GitHub Actions kích hoạt workflow CI/CD.
3. Chạy kiểm thử tự động với Pytest.
4. Đóng gói mã nguồn thành Docker image.
5. Đẩy image lên Artifact Registry.
6. SST đọc cấu hình hạ tầng và gọi API GCP để cập nhật dịch vụ Cloud Run.

| Thành phần | Trách nhiệm | Đầu vào | Đầu ra |
|---|---|---|---|
| GitHub Actions | Tự động hóa quá trình test, build và deploy. | Mã nguồn, Commit trigger | Docker Image, Lệnh Deploy |
| Artifact Registry | Lưu trữ các phiên bản Docker image. | Docker Image | Image URL cho Cloud Run |
| Cloud Run | Chạy ứng dụng web serverless. | Docker Image, Biến môi trường | HTTPS Endpoint |
| SST | Quản lý vòng đời tài nguyên GCP. | sst.config.ts | Dịch vụ trên GCP |

## 4. Lý thuyết cốt lõi và thuật ngữ

| Thuật ngữ | Giải thích ngắn gọn | Vai trò trong dự án |
|---|---|---|
| CI/CD | Tích hợp và triển khai liên tục. | Tự động hóa kiểm thử và đẩy code lên server. |
| Docker Image | Gói phần mềm chứa mã nguồn và môi trường. | Đảm bảo code chạy đồng nhất ở mọi nơi. |
| Cloud Run | Máy chủ phi máy chủ (Serverless) của Google. | Chạy container web tự động mở rộng. |
| IaC | Cơ sở hạ tầng dưới dạng mã. | Khai báo máy chủ bằng file code thay vì click tay. |

**Docker Container**
- **Nó là gì:** Một phiên bản thực thi độc lập và cô lập của Docker Image.
- **Vai trò trong dự án:** Chạy ứng dụng FastAPI một cách an toàn mà không phụ thuộc vào hệ điều hành máy chủ.
- **Ví dụ thực tế:** `docker run -d -p 8080:8080 fastapi-demo-project:v1.0.0`
- **Điểm cần lưu ý:** Container mất dữ liệu khi bị xóa. Port bên trong phải khớp với lệnh `EXPOSE`.

**Infrastructure as Code (IaC)**
- **Nó là gì:** Quản lý hạ tầng (máy chủ, mạng) thông qua các tệp mã nguồn.
- **Vai trò trong dự án:** Dùng SST để định nghĩa Cloud Run bằng code TypeScript, giúp dễ dàng tái tạo môi trường.
- **Ví dụ thực tế:** File `sst.config.ts`.
- **Điểm cần lưu ý:** Khai báo cấu hình sai có thể dẫn đến xóa nhầm tài nguyên.

## 5. Technology Stack

| Công nghệ/Thư viện | Phiên bản | Vai trò | Nguồn xác định |
|---|---|---|---|
| Python | 3.11 / 3.12 | Ngôn ngữ backend | Dockerfile / ci.yml |
| FastAPI | >=0.115.0 | Web Framework | requirements.txt |
| Uvicorn | >=0.30.0 | ASGI Server | requirements.txt |
| Pytest | >=8.0.0 | Công cụ kiểm thử | requirements.txt |
| Docker | Latest | Đóng gói ứng dụng | Dockerfile |
| SST | Latest | Quản lý hạ tầng | package.json |

## 6. Cấu trúc thư mục
```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── products/
│   │   ├── router.py
│   │   └── service.py
│   └── main.py
├── tests/
│   └── test_products.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── package.json
├── pyproject.toml
├── requirements.txt
└── sst.config.ts
```

| File/Thư mục | Chức năng |
|---|---|
| `.github/workflows/ci.yml` | Khai báo pipeline CI/CD tự động của GitHub Actions. |
| `src/main.py` | Entry point của ứng dụng FastAPI. |
| `tests/` | Chứa các kịch bản kiểm thử tự động. |
| `Dockerfile` | Chứa luồng lệnh để đóng gói Image. |
| `sst.config.ts` | File cấu hình hạ tầng IaC của SST. |

## 7. Yêu cầu hệ thống

| Công cụ | Phiên bản | Bắt buộc | Cách kiểm tra |
|---|---|---|---|
| Python | >=3.11 | Có | `python --version` |
| Docker | Mới nhất | Có | `docker --version` |
| Git | Mới nhất | Có | `git --version` |
| Node.js | >=18 | Có | `node --version` |
| Google Cloud CLI | Mới nhất | Có | `gcloud --version` |

## 8. Biến môi trường và cấu hình

| Biến | Bắt buộc | Mô tả | Giá trị mẫu an toàn |
|---|---|---|---|
| PORT | Không | Cổng mạng ứng dụng lắng nghe. Cloud Run tự cấp. | 8080 |
| GCP_CREDENTIALS | Có (trong CI) | JSON Key của Service Account. | `<YOUR_SERVICE_ACCOUNT_JSON>` |

**Nhắc rõ:**
- Không commit `.env`.
- Không hard-code secret.
- Kiểm tra `.gitignore`.
- Không ghi secret vào log.
- Không chia sẻ file credential công khai.

## 9. QUY TRÌNH THỰC HIỆN (WEEK 1 & WEEK 2)

### WEEK 1: Docker & GCP Foundations

**Bước 1: Khởi tạo Project và Cấp quyền IAM**
**Mục đích:** Khởi tạo vùng không gian trên Google Cloud và cấp quyền cho GitHub Actions Bot.
**Điều kiện trước khi thực hiện:**
- Cài đặt Google Cloud CLI.
- Đã đăng nhập `gcloud auth login`.
**Thực hiện tại:** Terminal nội bộ.
**Câu lệnh:**
```bash
gcloud projects create <PROJECT_ID> --name="Khanh FastAPI Deploy"
gcloud config set project <PROJECT_ID>
gcloud services enable run.googleapis.com artifactregistry.googleapis.com iam.googleapis.com
gcloud iam service-accounts create github-actions-bot
```
**Giải thích:** Tạo project, bật các API cần thiết để chạy dịch vụ và tạo tài khoản robot. Thay `<PROJECT_ID>` bằng mã định danh (vd: `khanh-fastapi-deploy-937`).
**Kết quả mong đợi:** Project được kích hoạt, Service account được tạo.
**Cách xác nhận:** `gcloud projects list`
**Khả năng chạy lại:** Không lũy đẳng (Tạo project trùng tên sẽ lỗi).
**Lỗi có thể xảy ra:**
- Biểu hiện: Lỗi Permission Denied hoặc Project ID already exists.
- Nguyên nhân: Chưa có quyền thanh toán hoặc tên trùng.

**Bước 2: Đóng gói Docker Image cục bộ**
**Mục đích:** Xây dựng Image từ mã nguồn để chạy thử nghiệm trên máy.
**Điều kiện trước khi thực hiện:** Có `Dockerfile` hợp lệ.
**Thực hiện tại:** Terminal nội bộ, tại thư mục gốc của dự án.
**Câu lệnh:**
```bash
docker build -t fastapi-demo-project:v1.0.0 .
docker run -d -p 8080:8080 --name fastapi-test fastapi-demo-project:v1.0.0
```
**Giải thích:** `-t` đặt tên cho image. `-d` chạy ngầm. `-p` liên kết cổng máy thực với container.
**Kết quả mong đợi:** Container khởi động thành công không crash.
**Cách xác nhận:** `docker ps`
**Khả năng chạy lại:** Không lũy đẳng với lệnh `run` (trùng tên container sẽ lỗi). Cách tránh: `docker rm -f fastapi-test` trước khi chạy lại.

**Bước 3: Lưu trữ trên Artifact Registry**
**Mục đích:** Lưu Docker Image lên đám mây bảo mật của Google.
**Thực hiện tại:** Terminal nội bộ.
**Câu lệnh:**
```bash
gcloud artifacts repositories create fastapi-repo --repository-format=docker --location=asia-southeast1
gcloud auth configure-docker asia-southeast1-docker.pkg.dev
docker tag fastapi-demo-project:v1.0.0 asia-southeast1-docker.pkg.dev/<PROJECT_ID>/fastapi-repo/fastapi-demo-project:v1.0.0
docker push asia-southeast1-docker.pkg.dev/<PROJECT_ID>/fastapi-repo/fastapi-demo-project:v1.0.0
```
**Giải thích:** Tạo repository docker trên đám mây. Gắn tag theo chuẩn đường dẫn của Google Cloud và đẩy dữ liệu lên.

**Bước 4: Triển khai thủ công lên Cloud Run (Day 4)**
**Mục đích:** Đưa ứng dụng ra Internet bằng dịch vụ Serverless.
**Thực hiện tại:** Terminal nội bộ.
**Câu lệnh:**
```bash
gcloud run deploy fastapi-demo-project \
  --image asia-southeast1-docker.pkg.dev/<PROJECT_ID>/fastapi-repo/fastapi-demo-project:v1.0.0 \
  --region asia-southeast1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080
```
**Giải thích:** Lệnh triển khai image lên Cloud Run. `--allow-unauthenticated` cho phép mọi người truy cập không cần token.
**Kết quả mong đợi:** Trả về một URL HTTPS hoạt động.

### WEEK 2: GitHub Actions CI/CD & SST IaC

**Bước 5: Cấu hình GitHub Actions CI/CD (Day 6-7)**
**Mục đích:** Tự động hóa hoàn toàn quá trình Test, Build và Deploy khi đẩy mã nguồn.
**Điều kiện trước khi thực hiện:** Khai báo biến môi trường `GCP_CREDENTIALS` trong Settings của GitHub Repository.
**Thực hiện tại:** File `.github/workflows/ci.yml`.
**Câu lệnh:** Đẩy code bằng git `git push origin main`.
**Giải thích:** GitHub Runner sẽ đọc file `ci.yml`, cấp quyền thông qua secret, chạy Pytest, build Docker và dùng gcloud CLI để deploy tự động.
**Cách xác nhận:** Kiểm tra tab "Actions" trên GitHub báo tích xanh (Passed).

**Bước 6: Khởi tạo và Deploy qua SST (Day 8-9)**
**Mục đích:** Thay thế lệnh gcloud thủ công bằng mã cấu hình hạ tầng TypeScript.
**Thực hiện tại:** Thư mục gốc, file `sst.config.ts`.
**Câu lệnh:**
```bash
npx sst install
npx sst deploy --stage dev
```
**Giải thích:** Lệnh `install` thiết lập các thư viện Pulumi. Lệnh `deploy` đọc file cấu hình và tự động khởi tạo Cloud Run service trên Google Cloud. `--stage` cho phép phân chia môi trường riêng biệt.
**Kết quả mong đợi:** Trả về URL HTTPS của ứng dụng và dòng chữ "Đang triển khai môi trường (stage): dev".
**Khả năng chạy lại:** Có (Lũy đẳng - Idempotent). SST quản lý state, nếu hạ tầng chưa thay đổi, nó sẽ không tạo mới.

## 10. CI/CD Pipeline
- **Trigger:** Khởi chạy khi có sự kiện `push` hoặc `pull_request` vào nhánh `main`.
- **Job 1 (test-python-code):** Chạy `pytest -v`.
- **Job 2 (build-and-deploy):**
  - **Authentication:** `google-github-actions/auth@v2`.
  - **Build:** `docker/build-push-action@v5`.
  - **Push Image:** Gắn tag bằng `github.sha`.
  - **Deployment:** Lệnh `gcloud run deploy`.
- **Secret yêu cầu:** `GCP_CREDENTIALS`.

## 11. API và Dữ liệu Đầu vào/Đầu ra

| Method | Endpoint | Chức năng | Authentication |
|---|---|---|---|
| GET | `/` | Kiểm tra API đang chạy | Không yêu cầu |
| GET | `/health` | Lấy trạng thái hệ thống | Không yêu cầu |
| GET | `/api/products` | Lấy danh sách sản phẩm | Không yêu cầu |
| GET | `/api/products/{id}` | Lấy chi tiết một sản phẩm | Không yêu cầu |

## 12. Troubleshooting (Xử lý sự cố)

**Lỗi: Khởi động container thất bại trên Cloud Run (Startup Failed)**
- **Biểu hiện:** Cloud Run báo lỗi không thể khởi động container, HTTP 503.
- **Nguyên nhân có thể:** Ứng dụng không lắng nghe cổng `PORT` do Cloud Run tiêm vào (mặc định FastAPI nghe cổng 8000, Cloud Run yêu cầu 8080).
- **Cách kiểm tra:**
  `gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=fastapi-demo-project"`
- **Cách khắc phục:**
  Sửa trong file khởi động hoặc Dockerfile để uvicorn lắng nghe đúng cổng biến môi trường:
  `CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]`
- **Cách xác nhận:**
  Deploy lại và truy cập URL thành công.

**Lỗi: GitHub Actions Unauthorized**
- **Biểu hiện:** Job `auth` báo lỗi không có quyền hoặc token hết hạn.
- **Nguyên nhân có thể:** Key JSON của Service Account bị điền sai hoặc đã bị thu hồi trên Google Cloud.
- **Cách khắc phục:** Lấy file JSON mới, vào GitHub Settings > Secrets, xóa khóa cũ và điền mã mới vào `GCP_CREDENTIALS`.

## 13. Rollback và Cleanup An Toàn

**Rollback Cloud Run:**
- **Lệnh rollback đã sử dụng:** Chuyển 100% traffic về bản ổn định cũ.
  ```bash
  gcloud run services update-traffic fastapi-demo-project --to-revisions=<REVISION_NAME>=100
  ```
- **Rủi ro:** Mã nguồn cũ có thể không tương thích với database hiện tại (Dự án này chưa dùng DB nên rủi ro = 0).

**Cleanup (Xóa tài nguyên):**
> [!WARNING]
> Lệnh sau có thể xóa dữ liệu hoặc tài nguyên và có thể không hoàn tác được.
```bash
gcloud run services delete fastapi-demo-project --region=asia-southeast1
gcloud artifacts repositories delete fastapi-repo --location=asia-southeast1
```
- **Cách xác nhận:** Vào Google Cloud Console kiểm tra lại không còn tài nguyên phát sinh chi phí.

## 14. Bảo mật
- **Secret management:** Sử dụng GitHub Secrets.
- **Least Privilege:** Service account chỉ được cấp quyền `run.admin` và `artifactregistry.writer`.
- **Container security:** Chạy Docker với `USER appuser` (non-root) để ngăn leo thang đặc quyền.
- **Không commit credential:** `.gitignore` chứa các đuôi `.env`, `.key`, `.pem`.
