from fastapi import APIRouter, Depends, Path, Query

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)
