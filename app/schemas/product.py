from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):
    tenant_id: str
    product_base_id: str

    product_id: str
    sku: Optional[str] = None
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[Decimal] = None
    currency: Optional[str] = None
    availability: Optional[str] = None
    tags: Optional[str] = None
    image_url: Optional[str] = None