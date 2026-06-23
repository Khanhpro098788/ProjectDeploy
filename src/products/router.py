from fastapi import APIRouter, HTTPException, status

from src.products import service
from src.products.schemas import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(
    prefix="/api/products",
    tags=["Products"],
)


@router.get(
    "/",
    response_model=list[ProductResponse],
    summary="Lấy danh sách sản phẩm",
    description="Trả về toàn bộ danh sách sản phẩm hiện có.",
)
async def get_products() -> list[ProductResponse]:
    return service.get_all_products()


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Lấy sản phẩm theo ID",
    description="Trả về sản phẩm theo ID. Trả HTTP 404 nếu không tìm thấy.",
)
async def get_product(product_id: int) -> ProductResponse:
    product = service.get_product_by_id(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sản phẩm có ID {product_id} không tồn tại.",
        )
    return product


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo sản phẩm mới",
    description="Tạo sản phẩm mới và thêm vào danh sách tạm thời.",
)
async def create_product(data: ProductCreate) -> ProductResponse:
    return service.create_product(data)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Cập nhật sản phẩm",
    description="Cập nhật thông tin sản phẩm theo ID. Trả HTTP 404 nếu không tìm thấy.",
)
async def update_product(product_id: int, data: ProductUpdate) -> ProductResponse:
    product = service.update_product(product_id, data)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sản phẩm có ID {product_id} không tồn tại.",
        )
    return product


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Xóa sản phẩm",
    description="Xóa sản phẩm theo ID. Trả HTTP 404 nếu không tìm thấy.",
)
async def delete_product(product_id: int) -> None:
    deleted = service.delete_product(product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sản phẩm có ID {product_id} không tồn tại.",
        )
