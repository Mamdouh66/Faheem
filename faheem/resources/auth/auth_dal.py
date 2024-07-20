import uuid
import sqlalchemy as sa

from faheem.resources.auth import auth_schemas, auth_models, auth_helpers
from faheem.config import logger

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic_core import ValidationError


def create_new_user(
    user: auth_schemas.UserCreate, db: Session = None
) -> auth_models.User | None:
    try:
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
    except ValidationError as v_e:
        logger.error(f"Failed to validate model: {v_e}")
        return None
    except Exception as e:
        logger.error(f"Failed to create new user: {e}")
        return None
    return new_user


def get_current_user(
    token: str = Depends(auth_helpers.oauth2_scheme), db: Session = None
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = auth_helpers.verify_access_token(
        token=token, credentials_exception=credentials_exception
    )

    user = db.query(auth_models.User).filter(auth_models.User.id == token.id).first()

    return user


def get_user_per_username(username: str, db: Session = None):
    try:
        user = (
            db.query(auth_models.User)
            .filter(auth_models.User.username == username)
            .first()
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with username '{username}' not found",
            )
        return user
    except SQLAlchemyError as e:
        logger.error(f"Failed to get user due to a database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while accessing the database",
        )
