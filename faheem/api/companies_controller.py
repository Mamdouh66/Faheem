from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from faheem.db.database import get_db
from faheem.resources.companies import companies_service, companies_schemas

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
)


@router.post(
    "/add",
    response_model=companies_schemas.CompanyOut,
    status_code=status.HTTP_201_CREATED,
)
def add_company(
    request: companies_schemas.CompanyCreate, db: Session = Depends(get_db)
):
    return companies_service.add_company(request, db)
