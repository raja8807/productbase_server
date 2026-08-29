"""change embedding dimension to 384

Revision ID: ec871ac41ffb
Revises: 3c2d96220703
"""

from typing import Sequence, Union

from alembic import op
from pgvector.sqlalchemy import VECTOR


revision: str = "ec871ac41ffb"
down_revision: Union[str, Sequence[str], None] = "3c2d96220703"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "products",
        "embedding",
        existing_type=VECTOR(dim=1536),
        type_=VECTOR(dim=384),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "products",
        "embedding",
        existing_type=VECTOR(dim=384),
        type_=VECTOR(dim=1536),
        existing_nullable=True,
    )