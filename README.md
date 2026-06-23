# 🚀 FastAPI Demo Project

> Dự án REST API nhỏ xây dựng bằng **FastAPI** + **Python 3.11**,  
> dùng để học **Docker**, **CI/CD** và **deploy lên Google Cloud Run**.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green?logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)
![Cloud Run](https://img.shields.io/badge/Google_Cloud_Run-deploy-orange?logo=googlecloud)

---

## ✨ Đặc điểm

| | |
|---|---|
| ✅ | REST API backend thuần túy (không có frontend) |
| ✅ | Dữ liệu mẫu lưu trong list Python (không cần database) |
| ✅ | Sẵn sàng chạy với Docker |
| ✅ | Tương thích với Google Cloud Run |
| ❌ | Không có Authentication |
| ❌ | Không có Database thật |

---

## 📁 Cấu trúc dự án

```
fastapi-demo-project/
├── src/
│   ├── __init__.py
│   ├── products/
│   │   ├── __init__.py
│   │   ├── router.py       # Định nghĩa các endpoint
│   │   ├── schemas.py      # Pydantic models (validate dữ liệu)
│   │   └── service.py      # Business logic (CRUD trên list Python)
│   └── main.py             # Khởi tạo FastAPI app
├── tests/
│   ├── __init__.py
│   └── test_products.py    # pytest tests (13 test cases)
├── conftest.py             # Cấu hình pytest root
├── pyproject.toml          # Cấu hình pytest & Pyrefly
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Mô tả | Status Code |
|:------:|----------|-------|:-----------:|
| `GET` | `/` | Kiểm tra API đang chạy | 200 |
| `GET` | `/health` | Kiểm tra trạng thái service | 200 |
| `GET` | `/api/products/` | Lấy danh sách sản phẩm | 200 |
| `GET` | `/api/products/{id}` | Lấy sản phẩm theo ID | 200 / 404 |
| `POST` | `/api/products/` | Tạo sản phẩm mới | 201 |
| `PUT` | `/api/products/{id}` | Cập nhật sản phẩm | 200 / 404 |
| `DELETE` | `/api/products/{id}` | Xóa sản phẩm | 204 / 404 |

---

## ⚡ Bắt đầu nhanh (Local)

### Bước 1 — Clone và vào thư mục dự án

```bash
git clone https://github.com/Khanhpro098788/ProjectDeploy.git
cd ProjectDeploy/fastapi-demo-project
```

### Bước 2 — Tạo môi trường ảo

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Bước 3 — Cài thư viện

```bash
pip install -r requirements.txt
```

### Bước 4 — Chạy ứng dụng

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
```

API chạy tại: **http://localhost:8080**  
Swagger UI tại: **http://localhost:8080/docs**

---

## 🧪 Chạy Tests

```bash
pytest -v
```

**Kết quả mong đợi:**

```
collected 13 items

tests/test_products.py::test_root                      PASSED
tests/test_products.py::test_health                    PASSED
tests/test_products.py::test_get_products              PASSED
tests/test_products.py::test_get_products_structure    PASSED
tests/test_products.py::test_get_product_by_id         PASSED
tests/test_products.py::test_get_product_not_found     PASSED
tests/test_products.py::test_create_product            PASSED
tests/test_products.py::test_create_product_empty_name PASSED
tests/test_products.py::test_create_product_negative_price PASSED
tests/test_products.py::test_update_product            PASSED
tests/test_products.py::test_update_product_not_found  PASSED
tests/test_products.py::test_delete_product            PASSED
tests/test_products.py::test_delete_product_not_found  PASSED

13 passed in 0.26s
```

---

## 🐳 📅 Day 2 — Docker Fundamentals

### Bước 1 — Chuẩn bị Dockerfile & .dockerignore
*(Đã cấu hình sẵn chuẩn production với Multi-stage build và bảo mật non-root)*

### Bước 2 — Build image

```bash
docker build -t fastapi-demo-project:v1.0.0 .
```

### Bước 3 — Chạy container

```bash
docker run -d -p 8080:8080 --name fastapi-test fastapi-demo-project:v1.0.0
```

Truy cập: **http://localhost:8080/docs**

### Bước 4 — Kiểm tra trạng thái

```bash
# Xem danh sách container đang chạy
docker ps
```

### Bước 5 — Xem logs / Bắt bệnh

```bash
docker logs fastapi-test
```

*(Kết quả mong đợi: `Application startup complete.`)*

---

## ☁️ Deploy lên Google Cloud Run

### 📅 Day 1 — Thiết lập GCP lần đầu *(chỉ làm 1 lần)*

#### Bước 1 — Đăng nhập Google Cloud

```bash
gcloud auth login
```

#### Bước 2 — Tạo GCP Project mới

```bash
gcloud projects create khanh-fastapi-deploy-937 --name="Khanh FastAPI Deploy"
```

#### Bước 3 — Đặt project làm mặc định

```bash
gcloud config set project khanh-fastapi-deploy-937
```

#### Bước 4 — Kiểm tra project đang dùng

```bash
# Xem project ID hiện tại
gcloud config get-value project

# Xem chi tiết project
gcloud projects describe khanh-fastapi-deploy-937
```

#### Bước 5 — Bật các API cần thiết

```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com iam.googleapis.com
```

> ✅ **Sau Day 1**, project GCP đã sẵn sàng. Không cần lặp lại các bước này.

---

### 📅 Day 3+ — Build & Deploy *(làm mỗi lần muốn deploy)*

#### Bước 1 — Tạo Artifact Registry repository *(chỉ làm 1 lần)*

```bash
gcloud artifacts repositories create fastapi-repo \
    --repository-format=docker \
    --location=asia-southeast1 \
    --description="Kho chua Docker Image cua FastAPI Demo"
```

#### Bước 2 — Cấu hình Docker authentication

```bash
gcloud auth configure-docker asia-southeast1-docker.pkg.dev
```

#### Bước 3 — Build image

```bash
docker build -t asia-southeast1-docker.pkg.dev/khanh-fastapi-deploy-937/fastapi-repo/fastapi-demo-project:latest .
```

#### Bước 4 — Push image lên Artifact Registry

```bash
docker push asia-southeast1-docker.pkg.dev/khanh-fastapi-deploy-937/fastapi-repo/fastapi-demo-project:latest
```

#### Bước 5 — Deploy lên Cloud Run

```bash
gcloud run deploy fastapi-demo-project \
    --image asia-southeast1-docker.pkg.dev/khanh-fastapi-deploy-937/fastapi-repo/fastapi-demo-project:latest \
    --platform managed \
    --region asia-southeast1 \
    --allow-unauthenticated \
    --port 8080
```

#### Bước 6 — Lấy URL service

```bash
gcloud run services describe fastapi-demo-project \
    --platform managed \
    --region asia-southeast1 \
    --format "value(status.url)"
```

Sau khi deploy xong, truy cập `<URL>/docs` để xem Swagger UI trên Cloud Run.

---

## ⚠️ Lưu ý quan trọng

> **Dữ liệu không được lưu trữ lâu dài!**  
> Mỗi khi container khởi động lại, dữ liệu sẽ reset về danh sách mẫu ban đầu.  
> Đây là thiết kế cố ý — mục tiêu của dự án là học Docker & Cloud Run, không phải persistence.

| Thông tin | Chi tiết |
|-----------|---------|
| GCP Project ID | `khanh-fastapi-deploy-937` |
| Region | `asia-southeast1` |
| Port mặc định | `8080` |
| Biến môi trường `PORT` | Cloud Run tự động inject, app hỗ trợ sẵn |
| Swagger UI | `<host>/docs` |
| ReDoc | `<host>/redoc` |
| Bước tiếp theo | Thêm database thật (PostgreSQL, Firestore...) |

