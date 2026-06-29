import os
import logging
import time
from fastapi import FastAPI, Request
import google.cloud.logging

from src.products.router import router as products_router

# 1. Khởi tạo Google Cloud Logging (tự động nhận dạng môi trường GCP)
try:
    client = google.cloud.logging.Client()
    client.setup_logging()
except Exception:
    # Fallback cho môi trường local chưa cấu hình xác thực Google
    logging.basicConfig(level=logging.INFO)

# Tạo một logger riêng cho ứng dụng
logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.INFO)

app = FastAPI(
    title="FastAPI Demo API",
    description="Dự án demo FastAPI để học Docker, CI/CD và deploy lên Google Cloud Run.",
    version="1.0.0",
)

# Đăng ký router của products
app.include_router(products_router)

# 2. Middleware để tự động ghi Log và bắt Trace ID
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Lấy Trace ID từ Google Cloud Run truyền vào (X-Cloud-Trace-Context)
    trace_header = request.headers.get("X-Cloud-Trace-Context", "unknown-trace")
    
    # Chuyển request đi tiếp
    response = await call_next(request)
    
    # Tính thời gian xử lý
    process_time = time.time() - start_time
    
    # Đóng gói dữ liệu Log
    log_data = {
        "method": request.method,
        "url": str(request.url.path),
        "status_code": response.status_code,
        "process_time_ms": round(process_time * 1000, 2),
        "trace": trace_header
    }
    
    # Phân loại mức độ nghiêm trọng (Severity)
    if response.status_code >= 500:
        logger.critical(f"Server Error - {log_data}", extra={"json_fields": log_data})
    elif response.status_code >= 400:
        logger.error(f"Client Error - {log_data}", extra={"json_fields": log_data})
    else:
        logger.info(f"Request OK - {log_data}", extra={"json_fields": log_data})
        
    return response


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    """Endpoint kiểm tra API đang hoạt động."""
    return {"message": "FastAPI Demo API is running"}


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Endpoint kiểm tra trạng thái sức khỏe của service."""
    return {"status": "healthy"}


@app.get("/crash", tags=["Test"])
async def crash_test():
    """Endpoint cố tình tạo lỗi 500 để test cảnh báo Alerting (Day 17)."""
    # Lỗi chia cho 0 sẽ tạo ra Internal Server Error (500)
    return 1 / 0


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=False)
