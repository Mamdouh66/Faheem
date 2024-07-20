from datetime import datetime, timedelta

from config import settings

from passlib.context import CryptContext  # type: ignore
from jose import JWTError, jwt  # type: ignore

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
