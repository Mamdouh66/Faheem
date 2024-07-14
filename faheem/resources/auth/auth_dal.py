import uuid
import sqlalchemy as sa

from faheem.resources.auth import auth_schemas, auth_models
from faheem.db.database import get_db

from sqlalchemy.orm import Session


def create_new_user(user: auth_schemas.UserCreate, db: Session = None):
    if db is None:
        db = next(get_db())

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
    db.close()
    return new_user


if __name__ == "__main__":
    print("Creating a new user....")
    new_user = auth_schemas.UserCreate(
        company_id=uuid.UUID("12b9edc6-93a8-4077-939c-8c91bf93d0d0"),
        username="Juan",
        password="12345678",
        role="user",
    )
    out = create_new_user(new_user)
    print(out)
