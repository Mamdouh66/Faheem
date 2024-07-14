"""create companies table

Revision ID: bc8ab26d0fc8
Revises:
Create Date: 2024-07-14 03:42:10.221547

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

import uuid

# revision identifiers, used by Alembic.
revision: str = "bc8ab26d0fc8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "companies",
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
    op.drop_table("companies")
