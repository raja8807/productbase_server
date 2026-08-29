# ProductBase Backend

Backend API for **ProductBase**, an AI-powered product catalog platform.

ProductBase lets applications upload a product catalog, generate embeddings for the catalog, store them in PostgreSQL with `pgvector`, and search products using natural-language queries.

## Features

- Multi-tenant product data isolation
- Supabase authentication with JWT verification
- Tenant ID derived from the authenticated Supabase user
- Product Base management
- Excel (`.xlsx`) product catalog import
- Background import jobs with progress tracking
- Product validation during import
- 384-dimensional text embeddings
- PostgreSQL + pgvector semantic search
- Hybrid search using vector similarity and PostgreSQL `pg_trgm`
- Tenant-scoped product listing and deletion
- Alembic database migrations
- FastAPI interactive API documentation

## Architecture

```text
Client / Frontend
       |
       | Bearer JWT
       v
   FastAPI API
       |
       +---- Supabase JWT verification
       |          |
       |          v
       |      tenant_id
       |
       +---- Product APIs
       |
       +---- Import Jobs
       |          |
       |          v
       |      Excel parsing
       |          |
       |          v
       |      Embeddings
       |
       +---- Search
                  |
                  v
          PostgreSQL + pgvector
```

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- pgvector
- Sentence Transformers
- `sentence-transformers/all-MiniLM-L6-v2`
- Supabase Auth
- PyJWT
- Cryptography
- OpenPyXL
- Alembic
- Pydantic Settings

## Project Structure

```text
productbase_app/
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── core/
│   │   ├── auth.py
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   ├── import_job.py
│   │   ├── product.py
│   │   ├── product_base.py
│   │   └── tenant.py
│   ├── routes/
│   │   ├── import_job.py
│   │   ├── product_base.py
│   │   └── products.py
│   ├── schemas/
│   │   └── product.py
│   ├── services/
│   │   ├── embedding_service.py
│   │   ├── import_job_service.py
│   │   ├── product_base_service.py
│   │   ├── product_import_service.py
│   │   ├── product_search_service.py
│   │   └── product_service.py
│   └── main.py
├── .env.example
├── .gitignore
├── alembic.ini
└── LICENSE
```

## Requirements

- Python 3.11+
- PostgreSQL
- PostgreSQL `pgvector` extension
- A Supabase project

The embedding model is downloaded the first time the application starts and may take some time on the first run.

## Installation

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pgvector sentence-transformers openpyxl pydantic-settings python-dotenv pyjwt cryptography python-multipart
```

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DATABASE

SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY

SUPABASE_JWT_KID=YOUR_JWT_KID
SUPABASE_JWT_X=YOUR_JWT_PUBLIC_KEY_X
SUPABASE_JWT_Y=YOUR_JWT_PUBLIC_KEY_Y
```

Do not commit `.env` or any secret credentials to GitHub.

For local development, create an `.env.example` containing placeholders only.

## Database Setup

Make sure PostgreSQL has the pgvector extension enabled:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

The project uses Alembic for schema migrations.

Run:

```bash
python -m alembic upgrade head
```

Create a new migration after changing SQLAlchemy models:

```bash
python -m alembic revision --autogenerate -m "your migration message"
```

Then apply it:

```bash
python -m alembic upgrade head
```

## Running the API

Start the development server:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive documentation:

```text
http://127.0.0.1:8000/docs
```

## Authentication

ProductBase uses Supabase Auth on the frontend.

The frontend sends the Supabase access token:

```http
Authorization: Bearer <access_token>
```

The backend verifies the JWT locally using the Supabase ES256/P-256 public key.

The JWT `sub` claim is used as the tenant ID.

```text
Supabase user.id
       =
JWT sub
       =
ProductBase tenant_id
```

This means clients do not need to send `tenant_id` in normal API requests.

## Product Import

Upload an Excel catalog using:

```http
POST /api/products/import
```

Request:

```text
Content-Type: multipart/form-data

file = products.xlsx
```

The authenticated tenant is automatically used.

Only `.xlsx` files are currently supported.

### Required Excel columns

```text
product_id
name
description
```

### Supported columns

```text
product_id
sku
name
description
category
brand
price
currency
availability
tags
image_url
```

The import flow:

```text
Excel upload
    ↓
Create / find Product Base
    ↓
Create Import Job
    ↓
Background processing
    ↓
Read Excel
    ↓
Validate products
    ↓
Build searchable text
    ↓
Generate embeddings
    ↓
Store products + embeddings
    ↓
Mark job completed
```

## Import Job Status

Check a specific import job:

```http
GET /api/import_job/{job_id}
```

Check whether the tenant currently has an active import:

```http
GET /api/import_job/jobs/active
```

Active jobs are:

```text
pending
processing
```

The frontend can use the active-job endpoint to restore import state after a page refresh.

## Product APIs

### List products

```http
GET /api/products
```

Returns products belonging to the authenticated tenant.

The embedding vector is intentionally not returned.

### Semantic / Hybrid Search

```http
GET /api/products/search?q=comfortable running shoes
```

The backend:

```text
Search query
    ↓
Create query embedding
    ↓
pgvector cosine similarity
    +
PostgreSQL text similarity
    ↓
Tenant filtering
    ↓
Ranked products
```

Search uses:

- Vector similarity from `pgvector`
- PostgreSQL `pg_trgm` text similarity
- Tenant isolation
- A configurable result limit

Example:

```text
GET /api/products/search?q=something comfortable for jogging
```

### Delete all products for the current tenant

```http
DELETE /api/products
```

The operation is restricted to the authenticated tenant.

### Product Base

Get the current tenant's Product Base:

```http
GET /api/product_base
```

Each tenant is restricted to one Product Base by the database uniqueness constraint.

## Embeddings

ProductBase currently uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The generated embeddings are:

```text
384 dimensions
```

Searchable text is constructed from product information such as:

```text
Product
Description
Category
Brand
Keywords / Tags
```

The embedding model is loaded once during application startup and reused for subsequent requests.

## Search Example

A query such as:

```text
I need something comfortable for jogging every morning
```

can retrieve products whose catalog descriptions contain related concepts such as:

```text
Lightweight cushioned running footwear
```

This is the main difference between semantic search and simple keyword matching.

## Multi-Tenancy

Every product and import job is associated with a tenant:

```text
tenant_id
```

The backend derives the tenant ID from the authenticated JWT rather than trusting a tenant ID supplied by the client.

For example, product search applies:

```python
Product.tenant_id == tenant_id
```

This prevents one authenticated tenant from searching or deleting another tenant's products.

## Development Notes

The embedding model is loaded during FastAPI startup. The first startup can therefore be slower while the model is downloaded and initialized.

For development:

```bash
python -m uvicorn app.main:app --reload
```

Avoid committing:

```text
venv/
.env
__pycache__/
*.pyc
```

These are already covered by the project's `.gitignore`.

## Current Scope

ProductBase is currently an MVP backend focused on:

- Product catalog ingestion
- AI embeddings
- Semantic product search
- Hybrid search
- Tenant isolation
- Import job tracking
- Supabase authentication

Future improvements can include:

- Search filters and facets
- Better ranking / reranking
- Pagination
- Import history
- Scheduled catalog synchronization
- More file formats
- Product updates and upserts
- Search analytics
- LLM-powered catalog answers
- Production background workers
- Vector indexes for larger catalogs

## License

See [LICENSE](LICENSE).
