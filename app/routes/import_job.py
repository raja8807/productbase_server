from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.core.auth import get_current_tenant
from app.core.database import get_db

from app.services.import_job_service import get_import_status, get_active_import_job




router = APIRouter(
    prefix="/api/import_job",
    tags=["import Job"],
)

@router.get("/{job_id}")
def import_status(
    job_id: UUID,
    tenant_id: UUID = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    job = get_import_status(
        db=db,
        job_id=job_id,
        tenant_id=tenant_id,
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Import job not found",
        )

    return {
        "id": str(job.id),
        "filename": job.filename,
        "status": job.status,
        "total_rows": job.total_rows,
        "processed_rows": job.processed_rows,
        "failed_rows": job.failed_rows,
        "error": job.error,
        "created_at": job.created_at,
        "completed_at": job.completed_at,
    }


@router.get("/jobs/active")
def active_import(
    tenant_id: UUID = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    job = get_active_import_job(
        db=db,
        tenant_id=tenant_id,
    )

    if not job:
        return {
            "active": False,
            "job": None,
        }

    return {
        "active": True,
        "job": {
            "id": str(job.id),
            "filename": job.filename,
            "status": job.status,
            "total_rows": job.total_rows,
            "processed_rows": job.processed_rows,
            "failed_rows": job.failed_rows,
        },
    }

    