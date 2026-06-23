import pytest
from collections.abc import AsyncGenerator

from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Tạo async test client dùng ASGITransport (httpx)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ──────────────────────────────────────────────
# Root & Health
# ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_root(client: AsyncClient) -> None:
    """GET / phải trả về message đúng."""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FastAPI Demo API is running"}


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    """GET /health phải trả về status healthy."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


# ──────────────────────────────────────────────
# GET danh sách sản phẩm
# ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_products(client: AsyncClient) -> None:
    """GET /api/products/ phải trả về danh sách có ít nhất 1 sản phẩm."""
    response = await client.get("/api/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_products_structure(client: AsyncClient) -> None:
    """Mỗi sản phẩm phải có đủ các field: id, name, price, description."""
    response = await client.get("/api/products/")
    assert response.status_code == 200
    products = response.json()
    for product in products:
        assert "id" in product
        assert "name" in product
        assert "price" in product
        assert "description" in product


# ──────────────────────────────────────────────
# GET sản phẩm theo ID
# ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_product_by_id(client: AsyncClient) -> None:
    """GET /api/products/1 phải trả về sản phẩm Laptop."""
    response = await client.get("/api/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Laptop"


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient) -> None:
    """GET /api/products/9999 phải trả về HTTP 404."""
    response = await client.get("/api/products/9999")
    assert response.status_code == 404
    assert "detail" in response.json()


# ──────────────────────────────────────────────
# POST tạo sản phẩm mới
# ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_product(client: AsyncClient) -> None:
    """POST /api/products/ phải tạo sản phẩm mới và trả về HTTP 201."""
    payload = {
        "name": "Monitor",
        "price": 3500000,
        "description": "Màn hình 27 inch",
    }
    response = await client.post("/api/products/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Monitor"
    assert data["price"] == 3500000
    assert data["description"] == "Màn hình 27 inch"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_product_empty_name(client: AsyncClient) -> None:
    """POST với tên rỗng phải trả về HTTP 422 (validation error)."""
    payload = {
        "name": "",
        "price": 100000,
        "description": "Mô tả",
    }
    response = await client.post("/api/products/", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_product_negative_price(client: AsyncClient) -> None:
    """POST với giá âm phải trả về HTTP 422 (validation error)."""
    payload = {
        "name": "Sản phẩm lỗi",
        "price": -100,
        "description": "Giá âm không hợp lệ",
    }
    response = await client.post("/api/products/", json=payload)
    assert response.status_code == 422


# ──────────────────────────────────────────────
# PUT cập nhật sản phẩm
# ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_product(client: AsyncClient) -> None:
    """PUT /api/products/2 phải cập nhật đúng field được gửi."""
    payload = {"price": 300000}
    response = await client.put("/api/products/2", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 2
    assert data["price"] == 300000


@pytest.mark.asyncio
async def test_update_product_not_found(client: AsyncClient) -> None:
    """PUT /api/products/9999 phải trả về HTTP 404."""
    payload = {"name": "Không tồn tại"}
    response = await client.put("/api/products/9999", json=payload)
    assert response.status_code == 404


# ──────────────────────────────────────────────
# DELETE xóa sản phẩm
# ──────────────────────────────────────────────

@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient) -> None:
    """DELETE /api/products/3 phải xóa thành công và trả về HTTP 204."""
    response = await client.delete("/api/products/3")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_product_not_found(client: AsyncClient) -> None:
    """DELETE /api/products/9999 phải trả về HTTP 404."""
    response = await client.delete("/api/products/9999")
    assert response.status_code == 404
