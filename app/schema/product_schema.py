from uuid import UUID
from typing import Any


from pydantic import BaseModel
from decimal import Decimal
from typing import Optional



class ProductCreatePayload(BaseModel):
    product_id: Optional[str] = None
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






                 