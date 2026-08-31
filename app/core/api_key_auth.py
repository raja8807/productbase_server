import hashlib
from datetime import datetime, timezone
from uuid import UUID

from fastapi import Header, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.api_key import ApiKey


def get_api_key_tenant(
    x_api_key: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> UUID:

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required",
        )

    key_hash = hashlib.sha256(
        x_api_key.encode("utf-8")
    ).hexdigest()

    api_key = (
        db.query(ApiKey)
        .filter(
            ApiKey.key_hash == key_hash,
        )
        .first()
    )

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    # Revoked
    if api_key.revoked_at is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key has been revoked",
        )

    # Expired
    if (
        api_key.expires_at is not None
        and api_key.expires_at <= datetime.now(timezone.utc)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key has expired",
        )

    # Update last used
    api_key.last_used_at = datetime.now(timezone.utc)
    db.commit()

    return api_key.tenant_id