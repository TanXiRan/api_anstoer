from fastapi import APIRouter, Depends, Response, Request, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import crud, schemas
import models
from sqlalchemy import desc


router = APIRouter(prefix="/animes", tags=["anime"])


@router.post("", response_model=schemas.AnimeResponse)
def create_anime(anime: schemas.AnimeCreate, db: Session = Depends(get_db)):
    return crud.create_anime(db=db, anime=anime)


@router.get("/{anime_id}", response_model=schemas.AnimeResponse)
def get_anime(anime_id: int, db: Session = Depends(get_db)):
    return crud.get_anime(db=db, anime_id=anime_id)


@router.get("", response_model=List[schemas.AnimeResponse])
def search_animes(
    request: Request,
    response: Response,
    title: str = None,
    alias: str = None,
    category: str = None,
    year: str = None,
    studio: str = None,
    skip: int = 0,
    limit: int = 30,
    sort_by: str = 'id',
    db: Session = Depends(get_db),
):
    return crud.search_animes(
        request,
        response,
        title,
        alias,
        category,
        year,
        studio,
        db,
        skip,
        limit,
        sort_by,
    )


@router.put("/{anime_id}", response_model=schemas.AnimeResponse)
def update_anime(
    anime_id: int, anime: schemas.AnimeCreate, db: Session = Depends(get_db)
):
    return crud.update_anime(anime_id=anime_id, db=db, anime=anime)


@router.patch("/{anime_id}", response_model=schemas.AnimeResponse)
def patch_anime(
    anime_id: int, anime: schemas.AnimeCreate, db: Session = Depends(get_db)
):
    return crud.patch_anime(anime_id=anime_id, db=db, anime=anime)


@router.delete("/{anime_id}", response_model=schemas.AnimeResponse)
def delete_anime(anime_id: int, db: Session = Depends(get_db)):
    return crud.delete_anime(db=db, anime_id=anime_id)
