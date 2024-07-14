"""create users table

Revision ID: 1ebc2bed7d00
Revises: 45c55a4a92d7
Create Date: 2024-07-14 04:24:38.796313

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa

import uuid


# revision identifiers, used by Alembic.
revision: str = "1ebc2bed7d00"
down_revision: Union[str, None] = "45c55a4a92d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            default=uuid.uuid4,
        ),
        sa.Column(
            "company_id",
            UUID(as_uuid=True),
            sa.ForeignKey("companies.id"),
            nullable=False,
        ),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, default=sa.func.now()),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, default=True),
        sa.Column("role", sa.String(), nullable=False, default="user"),
    )


def downgrade() -> None:
    pass
