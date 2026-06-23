# ══════════════════════════════════════════════════════════════════
# STAGE 1: builder — cài dependencies vào virtual environment riêng
# ══════════════════════════════════════════════════════════════════
FROM python:3.11-slim AS builder

# Không tạo file .pyc, log ra stdout ngay lập tức
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Cài dependencies vào thư mục /app/venv (cô lập hoàn toàn)
COPY requirements.txt .
RUN python -m venv /app/venv \
    && /app/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /app/venv/bin/pip install --no-cache-dir -r requirements.txt


# ══════════════════════════════════════════════════════════════════
# STAGE 2: runtime — chỉ copy những gì cần thiết, bỏ file rác
# ══════════════════════════════════════════════════════════════════
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Chỉ copy virtual environment đã cài sẵn từ stage builder
COPY --from=builder /app/venv /app/venv

# Copy source code (file rác đã bị loại bởi .dockerignore)
COPY src/ ./src/

# Tạo user non-root để chạy ứng dụng (bảo mật, không dùng root)
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Google Cloud Run sẽ inject biến môi trường PORT
ENV PORT=8080
EXPOSE 8080

# Dùng venv Python để chạy ứng dụng
CMD ["/app/venv/bin/uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
