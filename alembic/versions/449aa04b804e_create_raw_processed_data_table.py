"""create raw processed_data table

Revision ID: 449aa04b804e
Revises: c4ad3b5e00ff
Create Date: 2024-07-14 04:20:25.592195

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa

import uuid


# revision identifiers, used by Alembic.
revision: str = "449aa04b804e"
down_revision: Union[str, None] = "c4ad3b5e00ff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "processed_data",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            default=uuid.uuid4,
        ),
        sa.Column(
            "raw_data_id",
            UUID(as_uuid=True),
            sa.ForeignKey("raw_data.id"),
            nullable=False,
        ),
        sa.Column("cleaned_text", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("processed_data")
