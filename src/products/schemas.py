from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, description="Tên sản phẩm, không được để trống")
    price: float = Field(..., ge=0, description="Giá sản phẩm, phải >= 0")
    description: str = Field(default="", description="Mô tả sản phẩm")


class ProductCreate(ProductBase):
    """Schema dùng khi tạo mới sản phẩm (POST)."""
    pass


class ProductUpdate(BaseModel):
    """Schema dùng khi cập nhật sản phẩm (PUT). Tất cả field đều optional."""
    name: str | None = Field(default=None, min_length=1, description="Tên sản phẩm")
    price: float | None = Field(default=None, ge=0, description="Giá sản phẩm")
    description: str | None = Field(default=None, description="Mô tả sản phẩm")


class ProductResponse(ProductBase):
    """Schema trả về trong response."""
    id: int

    model_config = {"from_attributes": True}
