import bcrypt

from datetime import datetime, timedelta

from faheem.config import settings, logger
from faheem.resources.auth import auth_schemas

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Hash:
    @staticmethod
    def hash_password(password):
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password.decode("utf-8")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        try:
            password_byte_enc = plain_password.encode("utf-8")
            hashed_password_enc = hashed_password.encode("utf-8")
            return bcrypt.checkpw(
                password=password_byte_enc, hashed_password=hashed_password_enc
            )
        except ValueError:
            logger.error("Failed to verify password")
            return False


def create_access_token(data: dict):
    to_encode = data.copy()

    expiration_time = datetime.now() + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expiration_time})

    encoded_jwt = jwt.encode(
        claims=to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token=token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
        token_data = auth_schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data
