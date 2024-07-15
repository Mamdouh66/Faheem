from faheem.config import logger
from faheem.resources.auth import auth_schemas, auth_dal, auth_helpers

from sqlalchemy.orm import Session


def create_new_user(user: auth_schemas.UserCreate, db: Session = None):
    logger.info(f"Creating new user: {user.username} for {user.company_id}...")
    hashed_password = auth_helpers.Hash.bcrypt(user.password)
    user.password = hashed_password
    new_user = auth_dal.create_new_user(user, db)
    return new_user
