"""create model_results table

Revision ID: 45c55a4a92d7
Revises: 449aa04b804e
Create Date: 2024-07-14 04:22:43.400530

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa

import uuid


# revision identifiers, used by Alembic.
revision: str = "45c55a4a92d7"
down_revision: Union[str, None] = "449aa04b804e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "model_results",
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            default=uuid.uuid4,
        ),
        sa.Column(
            "processed_data_id",
            UUID(as_uuid=True),
            sa.ForeignKey("processed_data.id"),
            nullable=False,
        ),
        sa.Column("sentiment", sa.String(), nullable=False),
        sa.Column("probability", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, default=sa.func.now()),
    )


def downgrade() -> None:
    pass
