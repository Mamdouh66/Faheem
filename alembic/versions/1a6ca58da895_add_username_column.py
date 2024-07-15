"""add username column

Revision ID: 1a6ca58da895
Revises: 1ebc2bed7d00
Create Date: 2024-07-15 00:57:26.772659

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1a6ca58da895"
down_revision: Union[str, None] = "1ebc2bed7d00"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("username", sa.String(length=16), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "username")
