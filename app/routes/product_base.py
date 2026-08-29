from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.core.auth import get_current_tenant
from app.core.database import get_db

from app.services.product_base_service import get_product_base


router = APIRouter(
    prefix="/api/product_base",
    tags=["Product Base"],
)


@router.get("")
def get_product_base_endpoint(
    tenant_id: UUID = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    product_base = get_product_base(
        db=db,
        tenant_id=tenant_id,
    )

    if not product_base:
        raise HTTPException(
            status_code=404,
            detail="Product base not found",
        )

    return {
        "id": str(product_base.id),
        "name": product_base.name,
    }