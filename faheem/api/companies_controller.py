from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from faheem.db.database import get_db

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
)


@router.get("/add")
def add_company(db: Session = Depends(get_db)):
    return {"message": "Create a new company"}
