import sqlalchemy as sa
import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from faheem.db.database import Base
from faheem.resources.companies.companies_models import Company


class User(Base):
    __tablename__ = "users"

    id = sa.Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    company_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
    )
    username = sa.Column(sa.String, unique=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now(), nullable=False)
    is_active = sa.Column(sa.Boolean, default=True, nullable=False)
    last_login = sa.Column(sa.DateTime, nullable=True)
    role = sa.Column(sa.String, default="user", nullable=False)

    company = relationship("Company")
