import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.database import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    tenant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    environment = Column(
    String(10),
    nullable=False,
    default="development",
)

    key_prefix = Column(
        String(20),
        nullable=False,
        index=True,
    )

    key_hash = Column(
        Text,
        nullable=False,
        unique=True,
    )

    # When the key was last used
    last_used_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Optional expiration date
    expires_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Set when the key is revoked
    revoked_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )