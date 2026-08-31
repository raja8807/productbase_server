import hashlib
import secrets

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.api_key import ApiKey




import hashlib
import secrets


def generate_api_key(environment: str) -> tuple[str, str, str]:
    """
    Returns:
        raw_key
        key_prefix
        key_hash
    """

    if environment == "production":
        api_key_prefix = "pb_live_"
    elif environment == "development":
        api_key_prefix = "pb_test_"
    else:
        raise ValueError("Invalid environment")

    random_part = secrets.token_urlsafe(32)

    raw_key = f"{api_key_prefix}{random_part}"

    key_prefix = raw_key[:16]

    key_hash = hashlib.sha256(
        raw_key.encode("utf-8")
    ).hexdigest()

    return raw_key, key_prefix, key_hash



from datetime import datetime, timedelta, timezone


def create_api_key(
    db: Session,
    tenant_id: UUID,
    name: str,
    environment:str,
    expiration: str,
):
    # expiration: "never", "30", "60", "90", "365"

    raw_key, key_prefix, key_hash = generate_api_key(environment)

    expires_at = None

    if expiration != "never":
        days = int(expiration)
        expires_at = datetime.now(timezone.utc) + timedelta(days=days)

    api_key = ApiKey(
        tenant_id=tenant_id,
        name=name,
        key_prefix=key_prefix,
        key_hash=key_hash,
        environment=environment,
        expires_at=expires_at,
    )

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return {
        "raw_key": raw_key,
        "name": name,
        "expires_at": api_key.expires_at,
    }

def get_api_keys(
    db: Session,
    tenant_id: UUID,
):
    keys = (
        db.query(ApiKey)
        .filter(
            ApiKey.tenant_id == tenant_id
        )
        .order_by(ApiKey.created_at.desc())
        .all()
    )

    return keys

def delete_api_key(
        db:Session,
        tenant_id : UUID,
        api_key_id : UUID,
):
    api_key = db.query(ApiKey).filter(
        ApiKey.id == api_key_id and ApiKey.tenant_id == tenant_id
    ).first()

    if(not api_key):
        return False

    db.delete(api_key)
    db.commit()

    return True
