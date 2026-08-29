from uuid import UUID

from sqlalchemy.orm import Session

from app.models.product_base import ProductBase


def get_product_base(
    db: Session,
    tenant_id: UUID,
):
    return (
        db.query(ProductBase)
        .filter(
            ProductBase.tenant_id == tenant_id
        )
        .first()
    )