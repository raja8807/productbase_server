from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.api_key_auth import get_api_key_tenant
from app.core.database import get_db

from app.services.embedding_service import create_embedding
from app.services.product_search_service import search_products



router = APIRouter(
    prefix="/products",
    tags=["V1 Products"],
)

@router.get("/search")
def search_product_endpoint(
    q: str = Query(..., min_length=1),
    tenant_id: UUID = Depends(get_api_key_tenant),
    db: Session = Depends(get_db),
):
    query_embedding = create_embedding(q)

    products = search_products(
        db=db,
        tenant_id=tenant_id,
        query_embedding=query_embedding,
        query=q,
    )

    return {
        "query": q,
        "results": products,
    }