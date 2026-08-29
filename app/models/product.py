import uuid

from sqlalchemy import (
    Column,
    String,
    Text,
    Numeric,
    ForeignKey,
    DateTime,
    
)

from pgvector.sqlalchemy import Vector

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.tenant import Tenant
from app.models.product_base import ProductBase


class Product(Base):
    __tablename__ = "products"

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

    product_id = Column(
        String(100),
        nullable=False,
    )

    sku = Column(
        String(150),
        nullable=True,
    )

    name = Column(
        String(500),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    category = Column(
        String(200),
        nullable=True,
    )

    brand = Column(
        String(200),
        nullable=True,
    )

    price = Column(
        Numeric(12, 2),
        nullable=True,
    )

    currency = Column(
        String(10),
        nullable=True,
    )

    availability = Column(
        String(50),
        nullable=True,
    )

    tags = Column(
        Text,
        nullable=True,
    )

    image_url = Column(
        Text,
        nullable=True,
    )

    searchable_text = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    embedding = Column(
        Vector(384),
        nullable=True,
    )