"""create raw data table

Revision ID: c4ad3b5e00ff
Revises: cbb8ba11eb3f
Create Date: 2024-07-14 04:12:16.323961

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa

import uuid


# revision identifiers, used by Alembic.
revision: str = "c4ad3b5e00ff"
down_revision: Union[str, None] = "cbb8ba11eb3f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "raw_data",
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
        sa.Column(
            "source_id",
            UUID(as_uuid=True),
            sa.ForeignKey("data_sources.id"),
            nullable=False,
        ),
        sa.Column("data_text", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, default=sa.func.now()),
    )


def downgrade() -> None:
    pass
