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

### 📅 Day 3 — Artifact Registry *(Xây nhà kho đám mây)*

#### Bước 1 — Tạo nhà kho chứa Code *(chỉ làm 1 lần)*

```bash
gcloud artifacts repositories create fastapi-demo \
    --repository-format=docker \
    --location=asia-southeast1 \
    --description="Kho chua Docker Image cua Khanh FastAPI"
```

#### Bước 2 — Cấp thẻ ra vào cho Docker

```bash
gcloud auth configure-docker asia-southeast1-docker.pkg.dev
```

#### Bước 3 — Viết địa chỉ giao hàng (Tag Image)

```bash
docker tag fastapi-demo-project:v1.0.0 asia-southeast1-docker.pkg.dev/khanh-fastapi-deploy-937/fastapi-demo/fastapi-demo-project:v1.0.0
```

#### Bước 4 — Phóng tàu không gian (Push Image)

```bash
docker push asia-southeast1-docker.pkg.dev/khanh-fastapi-deploy-937/fastapi-demo/fastapi-demo-project:v1.0.0
```

> ✅ **Kết quả Day 3:** Chiếc hộp của bạn đã rời khỏi máy tính cá nhân và được lưu trữ vĩnh viễn, an toàn trên Google Artifact Registry.

---

### 📅 Day 4 — Deploying to Cloud Run *(Ra mắt công chúng)*

#### Bước 1 — Triển khai Ứng dụng

```bash
gcloud run deploy fastapi-demo-project \
    --image asia-southeast1-docker.pkg.dev/khanh-fastapi-deploy-937/fastapi-demo/fastapi-demo-project:v1.0.0 \
    --platform managed \
    --region asia-southeast1 \
    --allow-unauthenticated \
    --port 8080
```

#### Bước 2 — Lấy URL service

```bash
gcloud run services describe fastapi-demo-project \
    --platform managed \
    --region asia-southeast1 \
    --format "value(status.url)"
```

> 🎉 **Thành quả:** Ứng dụng đã online 24/7!  
> Truy cập Swagger UI tại: **[https://fastapi-demo-project-990324417574.asia-southeast1.run.app/docs](https://fastapi-demo-project-990324417574.asia-southeast1.run.app/docs)**

---

### 📅 Day 5 — Networking & Compute Engine *(Xây dựng hệ thống riêng)*

Thay vì dùng Cloud Run, hôm nay chúng ta tự thiết lập một khu vực mạng (VPC) và khởi tạo máy ảo (VM) trên Compute Engine để kiểm soát 100% hệ thống.

#### Bước 0 — Bật API Compute Engine
```bash
gcloud services enable compute.googleapis.com
```

#### Bước 1 — Tạo Custom VPC
*(Tạo mạng ảo độc lập tên `khanh-vpc`)*
```bash
gcloud compute networks create khanh-vpc --subnet-mode=custom
```

#### Bước 2 — Phân lô bán nền (Tạo Subnet)
*(Cắt dải IP `10.0.1.0/24` tại Singapore)*
```bash
gcloud compute networks subnets create khanh-subnet \
    --network=khanh-vpc \
    --region=asia-southeast1 \
    --range=10.0.1.0/24
```

#### Bước 3 — Tạo Firewall Rule (Mở cổng SSH)
*(Mở cổng 22 để có thể điều khiển máy chủ từ xa)*
```bash
gcloud compute firewall-rules create khanh-allow-ssh \
    --network=khanh-vpc \
    --allow=tcp:22 \
    --direction=INGRESS
```

#### Bước 4 — Khởi tạo Máy ảo (VM)
*(Mua một máy ảo cấu hình `e2-micro` và đặt vào Subnet đã tạo)*
```bash
gcloud compute instances create khanh-server \
    --zone=asia-southeast1-a \
    --machine-type=e2-micro \
    --network=khanh-vpc \
    --subnet=khanh-subnet
```

#### Bước 5 — SSH vào Máy ảo
*(Chiếm quyền điều khiển máy ảo)*
```bash
gcloud compute ssh khanh-server --zone=asia-southeast1-a
```

---

### 📅 Day 6 — GitHub Actions (CI Pipeline)

Hôm nay chúng ta tự động hóa khâu kiểm tra và đóng gói ứng dụng (Continuous Integration). Thay vì gõ lệnh bằng tay, một con Robot (GitHub Runner) sẽ tự làm mỗi khi có code mới.

#### Bước 1 — Tạo cấu trúc thư mục Workflow
Tạo thư mục `.github/workflows/` trong dự án của bạn.

#### Bước 2 — Viết kịch bản tự động hóa (`ci.yml`)
Tạo file `.github/workflows/ci.yml` với nội dung sau:
- **Trigger:** Kích hoạt mỗi khi push lên nhánh `main`.
- **Job 1 (Test):** Cài đặt Python 3.12, tải thư viện, chạy `pytest`.
- **Job 2 (Build):** Thử build Docker Image để kiểm tra cú pháp (Dry Run).

*(Xem code chi tiết trong file `.github/workflows/ci.yml` của dự án)*

#### Bước 3 — Đẩy code lên GitHub
```bash
git add .
git commit -m "ci: add GitHub Actions workflow"
git push
```

#### Bước 4 — Kiểm tra kết quả
- Lên trang Github của bạn, chuyển sang tab **Actions**.
- Xem trực tiếp con Robot đang cài đặt môi trường và báo cáo kết quả (Pass/Fail).

---

### 📅 Day 7 — Continuous Deployment (CD Pipeline)

Hôm nay là mảnh ghép cuối cùng. Bạn cấp quyền cho GitHub Actions có thể tự động thay bạn đẩy code lên Google Cloud (Cloud Run) mỗi khi bạn chạy lệnh `git push`.

#### Bước 1 — Cấp thẻ nhân viên (Service Account) cho GitHub
*(Tạo một tài khoản Robot và cấp các quyền quản trị Cloud Run, ghi Artifact Registry)*

```bash
# 1. Tạo tài khoản Robot
gcloud iam service-accounts create github-actions-bot \
    --display-name="GitHub Actions Bot"

# 2. Cấp quyền quản lý Cloud Run
gcloud projects add-iam-policy-binding khanh-fastapi-deploy-937 \
    --member="serviceAccount:github-actions-bot@khanh-fastapi-deploy-937.iam.gserviceaccount.com" \
    --role="roles/run.admin"

# 3. Cấp quyền ghi vào Artifact Registry
gcloud projects add-iam-policy-binding khanh-fastapi-deploy-937 \
    --member="serviceAccount:github-actions-bot@khanh-fastapi-deploy-937.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer"

# 4. Cấp quyền mạo danh Service Account (bắt buộc cho Cloud Run)
gcloud projects add-iam-policy-binding khanh-fastapi-deploy-937 \
    --member="serviceAccount:github-actions-bot@khanh-fastapi-deploy-937.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"
```

#### Bước 2 — Lấy chìa khóa (Tạo JSON Key)
*(Tải khóa bí mật của Robot về máy tính)*
```bash
gcloud iam service-accounts keys create gcp-key.json \
    --iam-account=github-actions-bot@khanh-fastapi-deploy-937.iam.gserviceaccount.com
```

#### Bước 3 — Lưu trữ khóa bảo mật (GitHub Secrets)
File `gcp-key.json` cực kỳ bảo mật. Ta sẽ cất nó vào két sắt của Github:
1. Dùng lệnh `type gcp-key.json | clip` để copy nội dung file.
2. Lên trình duyệt, mở tab **Settings** -> **Secrets and variables** -> **Actions** trong Github của bạn.
3. Bấm **New repository secret**.
4. Nhập tên là: **`GCP_CREDENTIALS`** và dán nội dung vào.
5. Quay lại máy tính, **xóa file JSON** (`del gcp-key.json`) để không bị lộ.

#### Bước 4 — Cập nhật luồng CI/CD (`ci.yml`)
Trong file `.github/workflows/ci.yml`, ta thêm **Job 2 (Build & Deploy)** để:
1. Đăng nhập vào Google Cloud bằng khóa bí mật (`google-github-actions/auth@v2`).
2. Build Docker Image với tag là mã Commit của bạn (`github.sha`).
3. Push Image đó lên Artifact Registry.
4. Chạy lệnh `gcloud run deploy` để tự động tung bản cập nhật mới nhất lên mạng!

> 🎉 **Thành quả Tối thượng:** 
> Từ bây giờ, bạn chỉ cần sửa code trên máy tính, chạy `git push`, Github Actions sẽ tự động Deploy. Website của bạn sẽ được tự động cập nhật phiên bản mới nhất!

---

### 📅 Day 8 — SST & Infrastructure as Code (IaC)

Bắt đầu từ Tuần 2, chúng ta chuyển sang tư duy **Cơ sở hạ tầng dưới dạng Mã (IaC)**. Thay vì click tay tạo máy chủ hay gõ lệnh `gcloud`, ta dùng framework **SST (sst.dev)** để viết code thiết kế hạ tầng. 

#### Bước 1 — Thuê "Kiến trúc sư" SST
Để tải công cụ quản lý hạ tầng SST về, chúng ta cần tạo file `package.json` trong dự án:

Tạo file **`package.json`** với nội dung:
```json
{
  "name": "fastapi-demo-project",
  "version": "1.0.0",
  "scripts": {
    "dev": "sst dev",
    "build": "sst build",
    "deploy": "sst deploy",
    "remove": "sst remove"
  },
  "devDependencies": {
    "sst": "latest"
  }
}
```
*(Đây là thẻ chứng minh thư giúp hệ thống biết dự án này có sử dụng SST. Bạn không cần chạy lệnh `npm install` lúc này).*

#### Bước 2 — Bản vẽ thiết kế Hạ tầng (`sst.config.ts`)
Tạo file **`sst.config.ts`**. Đây sẽ là trung tâm điều khiển của hệ thống mạng.

```typescript
/// <reference path="./.sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return {
      name: "fastapi-demo",
      // Chiến lược giữ lại tài nguyên:
      // - Nếu là môi trường production: Giữ lại tài nguyên (retain) để tránh xóa nhầm dữ liệu
      // - Nếu là môi trường dev/staging: Xóa sạch (remove) khi chạy sst remove để tiết kiệm tiền
      removal: input?.stage === "production" ? "retain" : "remove",
      home: "aws",
    };
  },
  async run() {
    // ---------------------------------------------------------
    // Định nghĩa Cơ sở hạ tầng (Infrastructure) tại đây
    // ---------------------------------------------------------
    
    console.log(`Đang triển khai môi trường (stage): ${$app.stage}`);
  },
});
```

#### Bước 3 — Chiến lược Môi trường (Stages)
Khái niệm cốt lõi của SST là **Stages**. Nó cho phép ta nhân bản (clone) toàn bộ hạ tầng thành nhiều phiên bản độc lập để kiểm thử an toàn. Dự án này quy định 3 môi trường:
1. `dev`: Dành cho lập trình viên thử nghiệm trên máy cá nhân (`npx sst deploy --stage dev`). Dễ dàng xóa bỏ.
2. `staging`: Bản nháp y hệt bản thật dùng để Test.
3. `production`: Sản phẩm thật cho người dùng (`npx sst deploy --stage production`). Chế độ bảo vệ nghiêm ngặt, không tự động xóa tài nguyên.

*(Ở các Ngày tiếp theo, ta sẽ dùng lệnh `sst deploy` để ra lệnh cho Kiến trúc sư SST đọc bản vẽ `sst.config.ts` và tự động xây dựng máy chủ trên GCP!)*

---

### 📅 Day 9 — SST + Cloud Run Infrastructure

Hôm nay chúng ta sẽ bắt tay vào viết "Bản vẽ hạ tầng" thực sự. Mục tiêu là dùng code TypeScript để tự động hóa hoàn toàn lệnh `gcloud run deploy` mà bạn từng gõ mỏi tay ở Ngày 4.

#### Bước 1 — Cài đặt thư viện Google Cloud
Vì SST hỗ trợ nhiều nền tảng (AWS, Cloudflare, Google Cloud...), ta cần tải bộ thư viện giao tiếp riêng cho Google Cloud (`@pulumi/gcp`).

```bash
npm install @pulumi/gcp @pulumi/pulumi
```

#### Bước 2 — Khai báo Cloud Run trong Bản vẽ thiết kế
Thay vì mở màn hình đen gõ lệnh `gcloud`, ta sẽ viết đoạn code sau vào file `sst.config.ts` (bên trong hàm `run`):

```typescript
// 1. Chỉ định Image Docker
const imageUrl = "asia-southeast1-docker.pkg.dev/khanh-fastapi-deploy-937/fastapi-demo/fastapi-demo-project:latest";

// 2. Khai báo dịch vụ Cloud Run
const service = new gcp.cloudrun.Service(`fastapi-service-${$app.stage}`, {
  location: "asia-southeast1",
  template: {
    spec: {
      containers: [{
        image: imageUrl,
        ports: [{ containerPort: 8080 }],
      }],
    },
  },
});

// 3. Mở quyền truy cập công khai (Allow unauthenticated)
new gcp.cloudrun.IamMember(`public-access-${$app.stage}`, {
  service: service.name,
  location: service.location,
  role: "roles/run.invoker",
  member: "allUsers",
});

// 4. In ra đường link trang web sau khi hoàn thành
return {
  WebsiteURL: service.statuses[0].url,
};
```

#### Bước 3 — Triển khai (Deploy)
Khi file thiết kế đã hoàn tất, bạn chỉ cần gõ 1 lệnh duy nhất để tạo ra 1 môi trường hoàn chỉnh:

```bash
npx sst deploy --stage dev
```
*(SST sẽ phân tích bản vẽ, gọi lên API của Google Cloud, tự động tạo cấu hình, khởi động Cloud Run và in ra một đường link URL cho bạn ngay trên màn hình đen!)*

> 💡 **Khả năng Tái tạo (Reproducible):** 
> Nếu bạn muốn tạo thêm một môi trường `staging`, bạn chỉ việc gõ `npx sst deploy --stage staging`. SST sẽ tự động tạo ra một Cloud Run thứ 2 hoàn toàn độc lập mà không ảnh hưởng tới cái cũ. Sức mạnh của IaC là đây!

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

