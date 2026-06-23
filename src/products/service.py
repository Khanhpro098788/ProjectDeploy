from src.products.schemas import ProductCreate, ProductResponse, ProductUpdate

# Dữ liệu mẫu lưu trong danh sách Python (thay thế database)
_products: list[dict] = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 15000000,
        "description": "Laptop dùng để học lập trình",
    },
    {
        "id": 2,
        "name": "Mouse",
        "price": 250000,
        "description": "Chuột không dây",
    },
    {
        "id": 3,
        "name": "Keyboard",
        "price": 500000,
        "description": "Bàn phím cơ",
    },
]

# Bộ đếm ID tự động tăng
_next_id: int = 4


def get_all_products() -> list[ProductResponse]:
    """Trả về toàn bộ danh sách sản phẩm."""
    return [ProductResponse(**p) for p in _products]


def get_product_by_id(product_id: int) -> ProductResponse | None:
    """Tìm sản phẩm theo ID. Trả về None nếu không tìm thấy."""
    for product in _products:
        if product["id"] == product_id:
            return ProductResponse(**product)
    return None


def create_product(data: ProductCreate) -> ProductResponse:
    """Tạo sản phẩm mới và thêm vào danh sách."""
    global _next_id
    new_product = {
        "id": _next_id,
        "name": data.name,
        "price": data.price,
        "description": data.description,
    }
    _products.append(new_product)
    _next_id += 1
    return ProductResponse(**new_product)


def update_product(product_id: int, data: ProductUpdate) -> ProductResponse | None:
    """Cập nhật sản phẩm theo ID. Trả về None nếu không tìm thấy."""
    for product in _products:
        if product["id"] == product_id:
            if data.name is not None:
                product["name"] = data.name
            if data.price is not None:
                product["price"] = data.price
            if data.description is not None:
                product["description"] = data.description
            return ProductResponse(**product)
    return None


def delete_product(product_id: int) -> bool:
    """Xóa sản phẩm theo ID. Trả về True nếu xóa thành công, False nếu không tìm thấy."""
    for index, product in enumerate(_products):
        if product["id"] == product_id:
            _products.pop(index)
            return True
    return False
