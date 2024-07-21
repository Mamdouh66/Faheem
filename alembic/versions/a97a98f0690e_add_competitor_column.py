"""add competitor column

Revision ID: a97a98f0690e
Revises: 1a6ca58da895
Create Date: 2024-07-21 03:14:00.589496

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a97a98f0690e"
down_revision: Union[str, None] = "1a6ca58da895"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "companies",
        sa.Column(
            "competitor",
            sa.ARRAY(sa.String(length=255)),
            nullable=False,
            server_default="{}",
        ),
    )
    op.alter_column("companies", "competitor", server_default=None)


def downgrade() -> None:
    op.drop_column("companies", "competitor")
