from uuid import UUID

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    Query
)

from sqlalchemy.orm import Session

from app.core.auth import get_current_tenant
from app.core.database import get_db
from app.models.import_job import ImportJob
from app.models.product_base import ProductBase
from app.services.product_import_service import process_import_job
from app.services.product_service import get_products, clear_all_products
from app.services.product_search_service import search_products
from app.services.embedding_service import create_embedding

router = APIRouter(
    prefix="/api/products",
    tags=["Products"],
)


@router.get("")
def get_products_endpoint(
    tenant_id: UUID = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    return get_products(
        db=db,
        tenant_id=tenant_id,
    )

@router.get("/search")
def search_product_endpoint(
    q: str = Query(..., min_length=1),
    tenant_id: UUID = Depends(get_current_tenant),
    # tenant_id: UUID = "d5292d6e-d251-43ae-9379-9421b69f2517",
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

@router.delete("")
def clear_products(
    tenant_id: UUID = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    deleted_count = clear_all_products(
        db=db,
        tenant_id=tenant_id,
    )

    return {
        "success": True,
        "deleted": deleted_count,
    }

@router.post("/import")
async def import_product_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    tenant_id: UUID = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File is required.",
        )

    if not file.filename.lower().endswith(".xlsx"):
        raise HTTPException(
            status_code=400,
            detail="Only .xlsx files are supported.",
        )

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    product_base = (
    db.query(ProductBase)
    .filter(
        ProductBase.tenant_id == tenant_id
    )
    .first()
)

    if not product_base:
        product_base = ProductBase(
        tenant_id=tenant_id,
        name="My Products",
    )

    db.add(product_base)
    db.flush()

    product_base_id = product_base.id

    job = ImportJob(
    tenant_id=tenant_id,
    product_base_id=product_base_id,
    filename=file.filename,
    status="pending",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    background_tasks.add_task(
        process_import_job,
        job.id,
        file_bytes,
        tenant_id,
        product_base_id,
    )

    return {
        "success": True,
        "job_id": str(job.id),
        "status": job.status,
    }