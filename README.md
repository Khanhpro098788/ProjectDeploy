# ☁️ Cloud Engineer Internship Portfolio
**Dự án:** FastAPI Demo API | **Nền tảng:** Google Cloud Platform (GCP)
**Công nghệ:** Docker, GitHub Actions, SST (IaC), Python (FastAPI)

Chào mừng đến với Cẩm nang Thực tập Cloud Engineering. Tài liệu này được thiết kế theo chuẩn lộ trình 4 tuần, ghi lại toàn bộ lý thuyết, mục tiêu và các dòng lệnh thực tế để tự động hóa một hệ thống Cloud Native hoàn chỉnh.

---

# 📅 WEEK 1: Docker + GCP Foundations
**Mục tiêu Tuần:** Xây dựng nền tảng vững chắc về Container hóa và sử dụng dòng lệnh Google Cloud (gcloud) để khởi tạo tài nguyên cơ bản.

## Day 1: GCP Setup & IAM Basics
🎯 **Mục tiêu (Output):** Khởi tạo thành công GCP project và thiết lập Service Account (tài khoản người máy) sẵn sàng cho việc tự động hóa.

📖 **Lý thuyết học thuật:**
- **VPC, Regions & Zones:** Hạ tầng vật lý của đám mây. Region là khu vực địa lý lớn (như Châu Á), Zone là các trung tâm dữ liệu nhỏ bên trong.
- **IAM (Identity and Access Management):** Chốt chặn bảo mật số một. Giúp kiểm soát Ai (Identity) được làm Gì (Role) trên Tài nguyên nào.
- **Least-Privilege:** Nguyên tắc bảo mật bắt buộc – Chỉ cấp những quyền tối thiểu nhất để hoàn thành công việc.

🛠️ **Các bước thực hành & Câu lệnh:**
```bash
# 1. Đăng nhập vào Google Cloud CLI
gcloud auth login

# 2. Tạo Project mới
gcloud projects create khanh-fastapi-deploy-937 --name="Khanh FastAPI Deploy"
gcloud config set project khanh-fastapi-deploy-937

# 3. Kích hoạt các API cần thiết
gcloud services enable run.googleapis.com artifactregistry.googleapis.com iam.googleapis.com

# 4. Tạo Service Account chuyên dụng cho CI/CD
gcloud iam service-accounts create github-actions-bot --display-name="GitHub Actions Bot"

# 5. Phân quyền (Roles) cho Service Account
gcloud projects add-iam-policy-binding khanh-fastapi-deploy-937 \
  --member="serviceAccount:github-actions-bot@khanh-fastapi-deploy-937.iam.gserviceaccount.com" \
  --role="roles/run.admin"
```

---

## Day 2: Docker Fundamentals
🎯 **Mục tiêu (Output):** Chạy ứng dụng FastAPI cục bộ (local) bên trong một Docker Container thay vì chạy trực tiếp trên máy tính.

📖 **Lý thuyết học thuật:**
- **Image vs Container:** Image là bản thiết kế đông lạnh (chỉ đọc), Container là phiên bản sống đang chạy của bản thiết kế đó.
- **Layer Caching:** Docker build hình ảnh theo từng lớp. Việc sắp xếp lệnh trong `Dockerfile` khôn ngoan (ví dụ copy `requirements.txt` trước) sẽ tận dụng bộ nhớ đệm, giúp build cực nhanh.
- **.dockerignore:** File chặn các rác/thư mục nhạy cảm (như `.env`, `__pycache__`) lọt vào trong Image.

🛠️ **Các bước thực hành & Câu lệnh:**
```bash
# 1. Build Docker Image từ thư mục hiện tại (.)
docker build -t fastapi-demo-project:v1.0.0 .

# 2. Chạy Container ẩn dưới nền (-d) và map cổng (8080:8080)
docker run -d -p 8080:8080 --name fastapi-test fastapi-demo-project:v1.0.0

# 3. Theo dõi log và trạng thái
docker ps
docker logs fastapi-test

# 4. Dừng và xóa sau khi test xong
docker stop fastapi-test
docker rm fastapi-test
```

---

## Day 3: Advanced Docker & Artifact Registry
🎯 **Mục tiêu (Output):** Tối ưu hóa dung lượng Image và lưu trữ phiên bản an toàn trên kho đám mây Artifact Registry.

📖 **Lý thuyết học thuật:**
- **Multi-stage Builds:** Tách quá trình build thành 2 giai đoạn: Giai đoạn 1 (Builder) chứa các bộ cài cồng kềnh, Giai đoạn 2 (Runtime) chỉ nhặt tệp chạy cuối cùng sang. Giúp Image thu nhỏ tối đa.
- **Artifact Registry:** Nơi lưu trữ tập trung và an toàn các Docker Image của doanh nghiệp trên GCP.

🛠️ **Các bước thực hành & Câu lệnh:**
```bash
# 1. Tạo kho lưu trữ trên Artifact Registry
gcloud artifacts repositories create fastapi-repo \
  --repository-format=docker \
  --location=asia-southeast1 \
  --description="Kho chua Docker Image"

# 2. Cấu hình xác thực Docker CLI với GCP
gcloud auth configure-docker asia-southeast1-docker.pkg.dev

# 3. Gắn tag cho Image theo chuẩn GCP
docker tag fastapi-demo-project:v1.0.0 \
  asia-southeast1-docker.pkg.dev/khanh-fastapi-deploy-937/fastapi-repo/fastapi-demo-project:v1.0.0

# 4. Push Image lên đám mây
docker push asia-southeast1-docker.pkg.dev/khanh-fastapi-deploy-937/fastapi-repo/fastapi-demo-project:v1.0.0
```

---

## Day 4: Deploying Containers to Cloud Run
🎯 **Mục tiêu (Output):** Triển khai mã nguồn thành công lên một dịch vụ Public Cloud Run có thể truy cập bằng trình duyệt.

📖 **Lý thuyết học thuật:**
- **Cloud Run Execution Model:** Máy chủ Serverless. Tự động "bừng tỉnh" khi có Request và tự động "tắt ngủ" (Scale to zero) khi không có ai dùng.
- **Revision:** Mỗi lần tung bản cập nhật mới sẽ sinh ra một "Bản sửa đổi" (Revision). Nếu bản mới lỗi, ta có thể lùi (rollback) về Revision cũ lập tức.

🛠️ **Các bước thực hành & Câu lệnh:**
```bash
# 1. Deploy Container từ Artifact Registry lên Cloud Run
gcloud run deploy fastapi-demo-project \
  --image=asia-southeast1-docker.pkg.dev/khanh-fastapi-deploy-937/fastapi-repo/fastapi-demo-project:v1.0.0 \
  --region=asia-southeast1 \
  --platform=managed \
  --allow-unauthenticated \
  --port=8080

# 2. Copy URL hiển thị trên terminal để truy cập web
```

---

## Day 5: Networking Basics & Compute Engine
🎯 **Mục tiêu (Output):** Hiểu cách mạng nội bộ hoạt động bằng cách dựng một máy ảo (VM) bảo mật trong một mạng tùy chỉnh.

📖 **Lý thuyết học thuật:**
- **VPC (Virtual Private Cloud):** Mạng nội bộ ảo, cô lập hệ thống của bạn với Internet bên ngoài.
- **Firewall Rules:** Tường lửa bảo vệ. Xác định rõ cổng nào (port) và địa chỉ IP nào được phép đi vào (Ingress) hoặc đi ra (Egress).

🛠️ **Các bước thực hành & Câu lệnh:**
```bash
# 1. Tạo mạng VPC tùy chỉnh
gcloud compute networks create khanh-vpc --subnet-mode=custom

# 2. Tạo Subnet (Mạng con)
gcloud compute networks subnets create khanh-subnet \
  --network=khanh-vpc \
  --region=asia-southeast1 \
  --range=10.0.1.0/24

# 3. Mở cổng Firewall cho SSH (Nên giới hạn theo IP cá nhân)
gcloud compute firewall-rules create allow-ssh \
  --network=khanh-vpc \
  --allow=tcp:22 \
  --source-ranges=0.0.0.0/0

# 4. Tạo Compute Engine VM
gcloud compute instances create khanh-server \
  --subnet=khanh-subnet \
  --zone=asia-southeast1-a
```

---

# 📅 WEEK 2: GitHub Actions CI/CD + sst.dev IaC
**Mục tiêu Tuần:** Chuyển đổi toàn bộ thao tác thủ công thành các luồng tự động (Pipelines) và Code hóa cơ sở hạ tầng (IaC).

## Day 6: GitHub Actions Fundamentals (CI)
🎯 **Mục tiêu (Output):** Xây dựng luồng CI (Continuous Integration) tự động chạy Test mỗi khi có người push code.

📖 **Lý thuyết học thuật:**
- **CI/CD Pipeline:** Hệ thống băng chuyền. Code mới đẩy lên sẽ tự động được kiểm duyệt (Build & Test) trước khi đưa ra ngoài (Deploy).
- **GitHub Runner:** Máy ảo dùng 1 lần do GitHub cung cấp để chạy các tác vụ trong Pipeline.

🛠️ **Các bước thực hành & Câu lệnh:**
```yaml
# 1. Tạo file .github/workflows/ci.yml
# 2. Khai báo Job Test (Ghi vào file)
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest -v
```

---

## Day 7: Continuous Deployment with GitHub Actions
🎯 **Mục tiêu (Output):** Tự động hóa hoàn toàn quy trình đóng gói (Docker) và tung bản cập nhật lên Cloud Run.

📖 **Lý thuyết học thuật:**
- **Service Account Keys / Secrets:** Két sắt an toàn của GitHub giúp ẩn các mật khẩu (credentials) khi thao tác với GCP.
- **Rollback Flow:** Luồng quay lui. Khi CD đẩy bản lỗi, ta có thể rollback trên Cloud Run UI hoặc Revert commit Git để CD tự build lại bản cũ.

🛠️ **Các bước thực hành & Câu lệnh:**
```yaml
# 1. Tạo Secret GCP_CREDENTIALS trên GitHub Settings
# 2. Cấu hình Job Deploy trong ci.yml:
  deploy:
    needs: test
    steps:
      - id: auth
        uses: google-github-actions/auth@v2
        with:
          credentials_json: '${{ secrets.GCP_CREDENTIALS }}'
      - run: gcloud auth configure-docker asia-southeast1-docker.pkg.dev
      # (Cấu hình Docker Build & Gcloud Run Deploy tiếp theo...)
```

---

## Day 8: sst.dev Core Concepts
🎯 **Mục tiêu (Output):** Khởi tạo thành công cấu trúc dự án SST và thiết lập chiến lược Quản lý Môi trường.

📖 **Lý thuyết học thuật:**
- **Infrastructure as Code (IaC):** Dùng code (TypeScript) để quy định kiến trúc mạng lưới, thay vì cấu hình bằng giao diện bấm chuột dễ sai sót.
- **SST Stages:** Cơ chế nhân bản môi trường độc lập cực nhanh (ví dụ: `dev` cho tester, `prod` cho khách hàng).

🛠️ **Các bước thực hành & Câu lệnh:**
```bash
# 1. Khởi tạo package.json cho SST
npm init -y
npm install sst

# 2. Tạo file sst.config.ts với nội dung thiết lập Stage (Bảo vệ prod, xóa dev)
```

---

## Day 9: sst.dev + Cloud Run Infrastructure
🎯 **Mục tiêu (Output):** Khai báo và triển khai Cloud Run hoàn toàn bằng SST, loại bỏ hoàn toàn việc gõ lệnh `gcloud`.

📖 **Lý thuyết học thuật:**
- **SST Constructs:** Các mảnh ghép lập trình (ví dụ `gcp.cloudrun.Service`) được map trực tiếp với các dịch vụ mạng của Google.
- **Reproducible Environments:** Mọi tài nguyên mạng được tạo ra đều chính xác 100% nhờ chạy chung một kịch bản code.

🛠️ **Các bước thực hành & Câu lệnh:**
```bash
# 1. Cài đặt thư viện giao tiếp GCP của Pulumi/SST
npm install @pulumi/gcp @pulumi/pulumi

# 2. Khai báo Cloud Run bằng Code trong sst.config.ts
# (Sử dụng lệnh new gcp.cloudrun.Service và new gcp.cloudrun.IamMember)

# 3. Triển khai kiến trúc tự động
npx sst deploy --stage dev
```

---

## Day 10: Evaluation Project
🎯 **Mục tiêu (Output):** Hoàn thiện 100% đánh giá cá nhân: Code Docker hóa, IaC chạy mượt mà, CI/CD tự động, Image lưu chuẩn chỉ.

📖 **Lý thuyết học thuật:**
- Đây là cột mốc tổng kết chặng 1. Đảm bảo toàn bộ kiến trúc được kết nối liền mạch: Code -> GitHub Actions -> Artifact Registry -> SST -> Cloud Run.

🛠️ **Các bước thực hành & Câu lệnh:**
```bash
# 1. Thay đổi text hiển thị trong mã nguồn src/main.py
# 2. Ghi nhận thay đổi lên Git để kích hoạt luồng tự động
git add src/main.py
git commit -m "feat: passed day 10 evaluation"
git push
# 3. Theo dõi màn hình GitHub Actions chuyển sang màu xanh (Success).
```

---

# 📅 WEEK 3: Security, IAM & Networking in Practice
**Mục tiêu Tuần:** Đưa dự án đạt chuẩn bảo mật doanh nghiệp (Production-ready).

## Day 11: Advanced IAM
🎯 **Mục tiêu (Output):** Thiết kế lại ma trận phân quyền (IAM Matrix) với tài khoản CI/CD giới hạn quyền lực tuyệt đối.

📖 **Lý thuyết học thuật:**
- **Permission Auditing:** Dò tìm các đặc quyền đang bị cấp thừa mứa và thu hồi lại để chống Hacker đánh cắp mật khẩu leo thang (Privilege Escalation).
- **Runtime Service Account:** Tài khoản chuyên dụng được gán cho chính Cloud Run lúc hoạt động, thay vì dùng tài khoản mặc định của Compute Engine.

🛠️ **Các bước thực hành & Câu lệnh:**
```bash
# 1. Tạo Service Account riêng cho Runtime Cloud Run
gcloud iam service-accounts create cloudrun-runtime-sa

# 2. Thu hồi các quyền rác không cần thiết của CI/CD bot
gcloud projects remove-iam-policy-binding khanh-fastapi-deploy-937 \
  --member="serviceAccount:github-actions-bot@..." \
  --role="roles/owner" # (Ví dụ minh họa nếu cấp sai)
```

---

## Day 12: Private Services & Access Control
🎯 **Mục tiêu (Output):** Cấu hình Cloud Run thành dịch vụ nội bộ (Private), không cho phép Public Internet truy cập trực tiếp.

📖 **Lý thuyết học thuật:**
- **IAM-based service invocation:** Chế độ ẩn của Cloud Run. Người gọi (Client) bắt buộc phải truyền chuỗi mã JWT Token vào Header để chứng minh danh tính.

🛠️ **Các bước thực hành & Câu lệnh:**
```bash
# 1. Xóa bỏ quyền allUsers của Cloud Run (Biến nó thành Private)
gcloud run services remove-iam-policy-binding fastapi-demo-project \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --region=asia-southeast1

# 2. Sinh mã Identity Token để gọi thử dịch vụ bảo mật
gcloud auth print-identity-token

# 3. Dùng cURL gọi API kèm Token
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" https://[CLOUD_RUN_URL]
```

---

## Day 13: Networking in Practice
🎯 **Mục tiêu (Output):** Cấu hình Ingress/Egress cho Cloud Run và test các luồng bị chặn.

📖 **Lý thuyết học thuật:**
- **Ingress/Egress Control:** Ingress là quy định thiết bị nào được phép đi vào máy chủ. Egress là quy định máy chủ được phép kết nối ra dịch vụ ngoài nào (ví dụ: cấm máy chủ tự ý gọi ra Internet để tải virus).

🛠️ **Các bước thực hành & Câu lệnh:**
```bash
# 1. Giới hạn Ingress: Chỉ cho phép lưu lượng từ mạng nội bộ (Internal)
gcloud run deploy fastapi-demo-project \
  --ingress=internal \
  --region=asia-southeast1 \
  --image=...
```

---

## Day 14: System Design for Cloud Engineers
🎯 **Mục tiêu (Output):** Thiết kế sơ đồ kiến trúc Capstone Project cuối cùng và phân tích các kịch bản chịu lỗi.

📖 **Lý thuyết học thuật:**
- **Stateless vs Stateful:** Cloud Run yêu cầu ứng dụng Stateless (không giữ trạng thái trong ổ cứng) để có thể nhân bản ra 1000 containers cùng lúc. Stateful (có lưu trữ) phù hợp với cơ sở dữ liệu.

🛠️ **Các bước thực hành & Câu lệnh:**
- *Ngày này chủ yếu dùng các công cụ vẽ sơ đồ (như Draw.io / Mermaid) để thảo luận và Document.*

---

## Day 15: Refactor & Hardening Day
🎯 **Mục tiêu (Output):** Dọn dẹp lại toàn bộ file rác, tối ưu CI Pipeline và tối ưu tốc độ Docker build.

📖 **Lý thuyết học thuật:**
- **Hardening:** Kỹ thuật gia cố hệ thống. Rà soát mọi lỗ hổng bảo mật, dọn các image cũ để tối ưu chi phí lưu trữ.

🛠️ **Các bước thực hành & Câu lệnh:**
```bash
# 1. Dọn dẹp các bản nháp trên Cloud Run
gcloud run revisions list
gcloud run revisions delete [REVISION_CU]

# 2. Kiểm tra lại toàn bộ file sst.config.ts để dọn code rác
```

---

# 📅 WEEK 4: Observability & Final Capstone
**Mục tiêu Tuần:** Triển khai hệ thống giám sát, cảnh báo lỗi và bảo vệ luận án thực tập (Capstone Project).

## Day 16: Cloud Logging
🎯 **Mục tiêu (Output):** Cấu hình Logs và truy vấn nhật ký lỗi chuyên nghiệp.

📖 **Lý thuyết học thuật:**
- **Centralized Logging:** Thu thập toàn bộ log từ hàng trăm containers về một nơi duy nhất (Cloud Logging) để dễ dàng dò tìm bug.

🛠️ **Các bước thực hành & Câu lệnh:**
```bash
# 1. Đọc trực tiếp log của Cloud Run qua CLI
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=fastapi-demo-project" --limit 10
```

---

## Day 17: Cloud Monitoring & Alerting
🎯 **Mục tiêu (Output):** Tạo Dashboard biểu đồ trực quan và cài đặt cảnh báo khi máy chủ sập.

📖 **Lý thuyết học thuật:**
- **Metrics & Dashboards:** Đo lường các chỉ số (CPU, RAM, Request Time) và trực quan hóa thành biểu đồ.
- **Alerting Policies:** Luật cảnh báo. Ví dụ: Nếu tỷ lệ lỗi HTTP 500 vượt mức 5%, lập tức gửi tin nhắn vào Slack/Email của kỹ sư trực hệ thống.

🛠️ **Các bước thực hành & Câu lệnh:**
- *Sử dụng giao diện Google Cloud Monitoring UI để tạo Alert Policy và Dashboard hoặc viết code Terraform/SST để định nghĩa biểu đồ.*

---

## Day 18: Production Readiness & Failure Testing
🎯 **Mục tiêu (Output):** Viết Kịch bản ứng phó sự cố (Runbooks) và giả lập lỗi sập hệ thống (Crash).

📖 **Lý thuyết học thuật:**
- **Postmortem:** Tài liệu khám nghiệm tử thi hệ thống sau khi xảy ra sự cố. Ghi rõ nguyên nhân (Root Cause) và biện pháp phòng tránh trong tương lai.

🛠️ **Các bước thực hành & Câu lệnh:**
```bash
# 1. Giả lập một lỗi sập bằng cách deploy image lỗi
# 2. Lập tức thực hiện lệnh Rollback khẩn cấp
gcloud run services update-traffic fastapi-demo-project --to-revisions=[REVISION_ON_DINH]=100
```

---

## Day 19: Final Capstone Build
🎯 **Mục tiêu (Output):** Khâu nối toàn bộ hạ tầng từ Week 1 đến Week 4 thành một dự án End-to-End tuyệt đối tự động.

📖 **Lý thuyết học thuật:**
- Cột mốc hoàn thiện tác phẩm tốt nghiệp. Toàn bộ hạ tầng do SST quản lý, Docker hóa bảo mật, CI/CD băng chuyền chuẩn xác, đi kèm hệ thống cảnh báo Monitoring.

🛠️ **Các bước thực hành & Câu lệnh:**
- *Rà soát và tổng duyệt lại toàn bộ các công đoạn đã thiết lập.*

---

## Day 20: Final Evaluation
🎯 **Mục tiêu (Output):** Thuyết trình và biểu diễn (Live Demo) đồ án tốt nghiệp trước Mentor.

📖 **Lý thuyết học thuật:**
- Đánh giá toàn diện năng lực của Kỹ sư Cloud (Cloud Engineer) với các trụ cột: Architecture (Kiến trúc), Automation (Tự động hóa), Security (Bảo mật), và Observability (Giám sát).

🛠️ **Các bước thực hành & Câu lệnh:**
- **Capstone Requirements:**
  - [x] All infrastructure defined with SST
  - [x] Clean Dockerfile and reproducible builds
  - [x] GitHub Actions CI/CD pipeline
  - [x] Secure IAM with least privilege
  - [x] Monitoring dashboards and alerting
  - [x] Log queries and runbooks
  - [x] Live debugging demonstration
