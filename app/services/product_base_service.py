from uuid import UUID

from sqlalchemy.orm import Session

from app.models.product_base import ProductBase


def get_product_base(
    db: Session,
    tenant_id: UUID,
):
    product_base = (
        db.query(ProductBase)
        .filter(ProductBase.tenant_id == tenant_id)
        .first()
    )

    if not product_base:
        product_base = ProductBase(
            tenant_id=tenant_id,
            name="My Products",
        )

        db.add(product_base)
        db.flush()

    return product_base