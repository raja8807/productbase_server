import base64

import jwt
from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePublicNumbers,
    SECP256R1,
)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings


security = HTTPBearer()


def base64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def get_public_key():
    x = int.from_bytes(
        base64url_decode(settings.SUPABASE_JWT_X),
        byteorder="big",
    )

    y = int.from_bytes(
        base64url_decode(settings.SUPABASE_JWT_Y),
        byteorder="big",
    )

    public_numbers = EllipticCurvePublicNumbers(
        x,
        y,
        SECP256R1(),
    )

    public_key = public_numbers.public_key()

    return public_key.public_bytes(
        Encoding.PEM,
        PublicFormat.SubjectPublicKeyInfo,
    )


PUBLIC_KEY = get_public_key()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    
    try:
        # print(1)
        header = jwt.get_unverified_header(token)
        # print(2)

        if header.get("alg") != "ES256":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token algorithm",
            )

        # print(3)
        

        if header.get("kid") != settings.SUPABASE_JWT_KID:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token key",
            )

        # print(4)
        

        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["ES256"],
            audience="authenticated",
            leeway=10,
        )

        # print(5)


        return payload

    

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )

    except jwt.InvalidTokenError as error:

        # print(error)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


from uuid import UUID


def get_current_tenant(
    current_user=Depends(get_current_user),
) -> UUID:
    user_id = current_user.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token",
        )

    try:
        return UUID(user_id)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid tenant ID",
        )    