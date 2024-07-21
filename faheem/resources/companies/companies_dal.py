import uuid
import sqlalchemy as sa

from faheem.resources.companies import companies_schemas, companies_models
from faheem.config import logger

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic_core import ValidationError


def add_company(company: companies_schemas.CompanyCreate, db: Session = None):
    try:
        company = companies_models.Company(
            id=uuid.uuid4(),
            name=company.name,
            description=company.description,
            competitor=company.competitor,
            created_at=sa.func.now(),
        )
        db.add(company)
        db.commit()
        db.refresh(company)
        return company
    except ValidationError as e:
        logger.error(f"Validation Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
    except SQLAlchemyError as e:
        logger.error(f"SQLAlchemy Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
