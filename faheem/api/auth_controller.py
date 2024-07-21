from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from faheem.db.database import get_db
from faheem.resources.auth import auth_service, auth_schemas

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/register",
    response_model=auth_schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register_user(user: auth_schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = auth_service.create_new_user(user, db)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Something went wrong while creating the user, {created_user}",
        )
    return {"username": user.username}


@router.post(
    path="/login", status_code=status.HTTP_200_OK, response_model=auth_schemas.Token
)
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    access_token = auth_service.verify_login(request, db)

    return {"access_token": access_token, "token_type": "bearer"}
