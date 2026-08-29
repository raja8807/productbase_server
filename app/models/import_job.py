import uuid

from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.database import Base


class ImportJob(Base):
    __tablename__ = "import_jobs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    tenant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id"),
        nullable=False,
        index=True,
    )

    product_base_id = Column(
        UUID(as_uuid=True),
        ForeignKey("product_bases.id"),
        nullable=False,
        index=True,
    )

    filename = Column(
        String(255),
        nullable=False,
    )

    status = Column(
        String(50),
        nullable=False,
        default="pending",
    )

    total_rows = Column(
        Integer,
        nullable=False,
        default=0,
    )

    processed_rows = Column(
        Integer,
        nullable=False,
        default=0,
    )

    failed_rows = Column(
        Integer,
        nullable=False,
        default=0,
    )

    error = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )