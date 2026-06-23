# ── Build stage ────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# Không tạo file .pyc, log ra stdout ngay lập tức
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Thư mục làm việc trong container
WORKDIR /app

# Cài dependencies trước (tận dụng Docker layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code
COPY . .

# Tạo user không có quyền root để chạy ứng dụng (bảo mật)
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Google Cloud Run sẽ inject biến môi trường PORT
ENV PORT=8080
EXPOSE 8080

# Chạy ứng dụng
CMD uvicorn src.main:app --host 0.0.0.0 --port ${PORT}
