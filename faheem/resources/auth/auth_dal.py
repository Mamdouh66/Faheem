import uuid
import sqlalchemy as sa

from faheem.resources.auth import auth_schemas, auth_models

from sqlalchemy.orm import Session


def create_new_user(user: auth_schemas.UserCreate, db: Session = None):
    new_user = auth_models.User(
        id=uuid.uuid4(),
        username=user.username,
        password=user.password,
        company_id=user.company_id,
        role=user.role,
        last_login=sa.func.now(),
        created_at=sa.func.now(),
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
