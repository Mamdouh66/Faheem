import sqlalchemy as sa
import uuid

from sqlalchemy.dialects.postgresql import UUID

from faheem.db.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = sa.Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    competitors = sa.Column(
        sa.ARRAY(sa.String(length=255)), nullable=False, server_default="{}"
    )
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now(), nullable=False)
