from faheem.config import logger
from faheem.resources.companies import (
    companies_schemas,
    companies_dal,
    companies_models,
)

from fastapi import HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


def add_company(
    company: companies_schemas.CompanyCreate, db: Session = None
) -> companies_models.Company:
    try:
        logger.info(f"Adding new company: {company.name}")
        new_company = companies_dal.add_company(company, db)
        logger.info(f"New company added: {new_company.name}")
        company_out = companies_schemas.CompanyOut(
            name=new_company.name,
            description=new_company.description,
            competitor=new_company.competitor,
        )
        return company_out

    except SQLAlchemyError as s_e:
        logger.error(f"Failed to add company due to a database error: {s_e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while accessing the database",
        )
    except HTTPException as h_e:
        logger.error(f"Failed to add company due to an HTTP error: {h_e}")
        raise h_e
    except Exception as e:
        logger.error(f"Unexpected error during company addition: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
