"""create data sources table

Revision ID: cbb8ba11eb3f
Revises: bc8ab26d0fc8
Create Date: 2024-07-14 04:05:35.382567

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa

import uuid

# revision identifiers, used by Alembic.
revision: str = "cbb8ba11eb3f"
down_revision: Union[str, None] = "bc8ab26d0fc8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "data_sources",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            default=uuid.uuid4,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("data_sources")
