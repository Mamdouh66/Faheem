from datetime import datetime, timedelta

from faheem.config import settings
from faheem.resources.auth import auth_schemas

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class Hash:
    def bcrypt(password: str):
        hashed_password = password_context.hash(password)
        return hashed_password

    def verify(hashed_password, plain_password):
        return password_context.verify(plain_password, hashed_password)


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
