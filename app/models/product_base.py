import uuid

from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class ProductBase(Base):
    __tablename__ = "product_bases"

    __table_args__ = (
    UniqueConstraint(
        "tenant_id",
        name="uq_product_bases_tenant_id",
    ),
    )

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

    name = Column(
        String(255),
        nullable=False,
    )

    status = Column(
        String(50),
        default="empty",
        nullable=False,
    )