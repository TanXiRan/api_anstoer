from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

router = APIRouter(prefix="/poster", tags=["poster"])


@router.post("/", response_model=schemas.Poster)
def create_poster(poster: schemas.PosterCreate, db: Session = Depends(get_db)):
    return crud.create_poster(db=db, poster=poster)


@router.get("/{poster_id}", response_model=schemas.Poster)
def read_poster(poster_id: int, db: Session = Depends(get_db)):
    return crud.get_poster(db, poster_id=poster_id)


@router.delete("/{poster_id}")
def read_poster(poster_id: int, db: Session = Depends(get_db)):
    return crud.delete_poster(db, poster_id=poster_id)
