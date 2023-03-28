from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class AnimeBase(BaseModel):
    title: str
    alias: Optional[str]
    watch_count: int = 1
    year: Optional[str]
    rating: float = 10.0
    region: str = "日本"
    studio: Optional[str]
    release_date: Optional[str]
    end_date: Optional[str]
    description: Optional[str]
    watch_dates: Optional[str]


class AnimeCreate(AnimeBase):
    posters: List[str] = []
    categories: List[str] = []


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class PosterBase(BaseModel):
    path: str


class PosterCreate(PosterBase):
    path: str


class PosterOut(PosterBase):
    id: int
    anime_id: int

    class Config:
        orm_mode = True


class Poster(PosterBase):
    id: int
    path: str
    anime_id: int
    anime: AnimeBase

    class Config:
        orm_mode = True


class AnimeResponse(AnimeBase):
    id: int
    created_time: datetime
    updated_time: datetime = None
    posters: List[PosterOut] = []
    categories: List[CategoryOut] = []
    # nextUrl: Optional(str)

    class Config:
        orm_mode = True


class Category(CategoryBase):
    id: int
    animes: List[AnimeResponse] = []

    class Config:
        orm_mode = True
