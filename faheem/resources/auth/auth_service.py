from faheem.config import logger
from faheem.resources.auth import auth_schemas, auth_dal, auth_helpers, auth_models

from fastapi import HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


def create_new_user(
    user: auth_schemas.UserCreate, db: Session = None
) -> auth_models.User:
    try:
        logger.info(f"Creating new user: {user.username} for {user.company_id}...")
        hashed_password = auth_helpers.Hash.hash_password(user.password)
        user.password = hashed_password
        new_user = auth_dal.create_new_user(user, db)
        logger.info(f"New user created: {new_user.username}")
        return new_user
    except Exception as e:
        logger.error(f"Unexpected error during user creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


def verify_login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = None
) -> auth_schemas.Token:
    try:
        user = auth_dal.get_user_per_username(request.username, db)

        if not auth_helpers.Hash.verify_password(
            plain_password=request.password, hashed_password=user.password
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid credentials",
            )

        access_token = auth_helpers.create_access_token(data={"user_id": str(user.id)})
        return access_token

    except SQLAlchemyError as s_e:
        logger.error(f"Failed to verify login due to a database error: {s_e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while accessing the database",
        )
    except HTTPException as h_e:
        logger.error(f"Failed to verify login due to an HTTP error: {h_e}")
        raise h_e
    except Exception as e:
        logger.error(f"Unexpected error during login verification: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
