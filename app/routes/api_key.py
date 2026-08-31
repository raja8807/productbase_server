# create_api_key
from uuid import UUID

from fastapi import (
    APIRouter,
    
    Depends,
)

from sqlalchemy.orm import Session

from app.core.auth import get_current_tenant
from app.core.database import get_db

from app.services.api_key_service import create_api_key, get_api_keys, delete_api_key
from app.schema.api_key_scheme import ApiKeyResponse, ApiKeyCreate

router = APIRouter(
    prefix="/api/api-key",
    tags=["API Keys"],
)

@router.post("")
def create_api_key_endpoint(
    payload: ApiKeyCreate,
    tenant_id: UUID = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    return create_api_key(
        db=db,
        tenant_id=tenant_id,
        name=payload.name,
        environment=payload.environment,
        expiration=payload.expiration,
    )


@router.get("", response_model=list[ApiKeyResponse])
def get_api_keys_endpoint(
    tenant_id: UUID = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    return get_api_keys(
        db=db,
        tenant_id=tenant_id,
    )


@router.delete("/{api_key_id}")
def delete_api_key_endpoint(
    api_key_id: UUID,
    tenant_id: UUID = Depends(get_current_tenant),
    db: Session = Depends(get_db),
):
    return delete_api_key(
        db=db,
        tenant_id=tenant_id,
        api_key_id=api_key_id,
    )
    

