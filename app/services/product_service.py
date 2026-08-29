from uuid import UUID

from sqlalchemy.orm import Session

from app.models.product import Product


def get_products(
    db: Session,
    tenant_id: UUID,
):
    products = (
        db.query(
            Product.id,
            Product.product_id,
            Product.sku,
            Product.name,
            Product.description,
            Product.category,
            Product.brand,
            Product.price,
            Product.currency,
            Product.availability,
            Product.tags,
            Product.image_url,
        )
        .filter(
            Product.tenant_id == tenant_id
        )
        .all()
    )

    return [
        dict(product._mapping)
        for product in products
    ]

def clear_all_products(
    db: Session,
    tenant_id: UUID,
):
    deleted_count = (
        db.query(Product)
        .filter(Product.tenant_id == tenant_id)
        .delete(synchronize_session=False)
    )

    db.commit()

    return deleted_count