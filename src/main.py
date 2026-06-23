import os

from fastapi import FastAPI

from src.products.router import router as products_router

app = FastAPI(
    title="FastAPI Demo API",
    description="Dự án demo FastAPI để học Docker, CI/CD và deploy lên Google Cloud Run.",
    version="1.0.0",
)

# Đăng ký router của products
app.include_router(products_router)


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    """Endpoint kiểm tra API đang hoạt động."""
    return {"message": "FastAPI Demo API is running"}


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Endpoint kiểm tra trạng thái sức khỏe của service."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("src.main:app", host="0.0.0.0", port=port, reload=False)
