from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas
from typing import List

router = APIRouter(prefix="/categories", tags=["category"])


@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category=category)


@router.get("/{cat_id}", response_model=schemas.Category)
def get_category(cat_id: int, db: Session = Depends(get_db)):
    return crud.get_category(cat_id, db)


@router.get("/", response_model=List[schemas.Category])
def get_categories(response: Response, db: Session = Depends(get_db)):
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return crud.get_categories(db)


@router.delete("/{cat_id}", response_model=schemas.Category)
def delete_category(cat_id: int, db: Session = Depends(get_db)):
    return crud.delete_category(db, cat_id)
