from uuid import UUID

from sqlalchemy.orm import Session

from app.models.import_job import ImportJob


def get_import_status(
    db: Session,
    job_id: UUID,
    tenant_id: UUID,
):
    job = (
        db.query(ImportJob)
        .filter(
            ImportJob.id == job_id,
            ImportJob.tenant_id == tenant_id,
        )
        .first()
    )

    return job


def get_active_import_job(
    db: Session,
    tenant_id: UUID,
):
    return (
        db.query(ImportJob)
        .filter(
            ImportJob.tenant_id == tenant_id,
            ImportJob.status.in_(["pending", "processing"]),
        )
        .first()
    )