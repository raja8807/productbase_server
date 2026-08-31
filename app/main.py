

from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import engine
from app.services.embedding_service import create_embedding

from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends

from app.core.auth import get_current_tenant

# from contextlib import asynccontextmanager
# from app.services.embedding_service import get_model


from app.routes.products import router as products_router
from app.routes.product_base import router as product_base_router
from app.routes.import_job import router as import_job_router
from app.routes.api_key import router as api_key_router

from app.routes.v1.products import router as product_v1_router

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Loading embedding model...")

#     get_model()

#     print("Embedding model loaded.")

#     yield


app = FastAPI(
    title="ProductBase API",
    # lifespan=lifespan,
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
    tenant_id = Depends(get_current_tenant),
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
