"""add product embeddings

Revision ID: 3c2d96220703
Revises: e8defb64ffdf
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import VECTOR


revision: str = "3c2d96220703"
down_revision: Union[str, Sequence[str], None] = "e8defb64ffdf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column(
            "embedding",
            VECTOR(dim=1536),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "products",
        "embedding",
    )