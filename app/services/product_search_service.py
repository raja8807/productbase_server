from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.product import Product


def search_products(
    db: Session,
    tenant_id: UUID,
    query_embedding: list[float],
    query: str,
    limit: int = 10,
):
    distance = Product.embedding.cosine_distance(
        query_embedding
    ).label("distance")

    similarity = (
        1 - distance
    ).label("similarity")

    keyword_score = func.greatest(
        func.similarity(Product.name, query),
        func.similarity(Product.description, query),
        func.similarity(Product.brand, query),
        func.similarity(Product.category, query),
    ).label("keyword_score")

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
            distance,
            similarity,
            keyword_score,
        )
        .filter(
            Product.tenant_id == tenant_id,
            Product.embedding.isnot(None),
            distance <= 0.75,
        )
        .order_by(
            similarity.desc(),
            keyword_score.desc(),
        )
        .limit(limit)
        .all()
    )

    return [
        {
            **dict(product._mapping),
            "distance": float(product.distance),
            "similarity": float(product.similarity),
            "keyword_score": float(product.keyword_score),
        }
        for product in products
    ]



