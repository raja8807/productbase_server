from datetime import datetime
from uuid import UUID

from typing import Literal
from pydantic import BaseModel


class ApiKeyResponse(BaseModel):
    id: UUID
    name: str
    environment : str
    key_prefix: str
    last_used_at: datetime | None = None
    expires_at: datetime | None = None
    revoked_at: datetime | None = None
    created_at: datetime

    
class ApiKeyCreate(BaseModel):
    name: str
    expiration: Literal["never", "30", "60", "90", "365"]
    environment: Literal["production", "development"]