from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.auth import get_current_tenant
from app.core.database import engine
from app.routes.api_key import router as api_key_router
from app.routes.import_job import router as import_job_router
from app.routes.product_base import router as product_base_router
from app.routes.products import router as products_router
from app.routes.v1.products import router as product_v1_router


app = FastAPI(
    title="ProductBase API",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "ProductBase API is running"
    }


@app.get("/db-test")
def database_test():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1")
        )

        return {
            "database": result.scalar()
        }


@app.get("/tenant-test")
def tenant_test(
    tenant_id=Depends(get_current_tenant),
):
    return {
        "tenant_id": str(tenant_id)
    }


app.include_router(products_router)
app.include_router(product_base_router)
app.include_router(import_job_router)
app.include_router(api_key_router)

app.include_router(
    product_v1_router,
    prefix="/api/v1",
)