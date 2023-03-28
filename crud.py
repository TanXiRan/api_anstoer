from fastapi import HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
import models
import schemas
import os
from urllib import parse


def create_category_if_not_exist(db: Session, cat_name: str):
    db_cat = db.query(models.Category).filter_by(name=cat_name).first()
    if not db_cat:
        db_cat = models.Category(name=cat_name)
        db.add(db_cat)
        db.commit()
        db.refresh(db_cat)
    return db_cat


def create_poster_if_not_exist(db: Session, poster_path: str):
    db_poster = (
        db.query(models.Poster).filter(models.Poster.path == poster_path).first()
    )
    if not db_poster:
        db_poster = models.Poster(path=poster_path)
    return db_poster


def get_anime(db: Session, anime_id: int):
    return db.query(models.Anime).filter(models.Anime.id == anime_id).first()


def get_animes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Anime).offset(skip).limit(limit).all()


def search_animes(
    request: Request,
    response: Response,
    title: str,
    alias: str,
    category: str,
    year: str,
    studio: str,
    db: Session,
    skip: int,
    limit: int,
    sort_by: str,
):
    db_query = db.query(models.Anime)
    if title:
        db_query = db_query.filter(models.Anime.title.contains(title))
    if alias:
        db_query = db_query.filter(models.Anime.title.contains(alias))
    if category:
        db_category = (
            db.query(models.Category).filter(models.Category.name == category).first()
        )
        if not db_category:
            raise HTTPException(404, {"detail": '没有相关分类的动漫'})
        db_query = db_query.join(models.Anime.categories).filter(
            models.Category.id == db_category.id
        )
    if year:
        db_query = db_query.filter(models.Anime.year == year)
    if studio:
        print('hhh', len(db_query.all()))
        db_query = db_query.filter(models.Anime.studio.contains(studio))
        print(len(db_query.all()))
    if sort_by.startswith('-'):
        data = db_query.order_by(desc(sort_by)).offset(skip).limit(limit).all()
    data = db_query.order_by(sort_by).offset(skip).limit(limit).all()

    next_skip = skip + limit
    next_url = None
    if next_skip < len(db_query.all()):
        query_dict = {
            'title': title,
            'alias': alias,
            'category': category,
            'year': year,
            'studio': studio,
            'skip': next_skip,
            'limit': limit,
            'sort_by': sort_by,
        }
        next_url = parse.urlencode(
            {key: value for key, value in query_dict.items() if query_dict[key]}
        )

    if next_url:
        response.headers['next_url'] = f'{request.base_url}animes?{next_url}'
    return data


def create_anime(db: Session, anime: schemas.AnimeCreate):
    anime_dict = anime.dict()
    categories = []
    posters = []
    if anime_dict.get("categories", None):
        categories = anime_dict.pop("categories")
    if anime_dict.get("posters", None):
        posters = anime_dict.pop("posters")

    db_anime = models.Anime(**anime_dict)
    for category in categories:
        db_cat = create_category_if_not_exist(db, cat_name=category)
        db_anime.categories.append(db_cat)

    for poster in posters:
        db_poster = create_poster_if_not_exist(db, poster_path=poster)
        db_anime.posters.append(db_poster)

    db.add(db_anime)
    db.commit()
    db.refresh(db_anime)
    return db_anime


def update_anime(anime_id: int, db: Session, anime: schemas.AnimeCreate):
    db_anime = db.query(models.Anime).filter(models.Anime.id == anime_id).first()
    print(anime.dict())
    anime_dict = anime.dict()
    categories = []
    posters = []
    if anime_dict.get("categories", None):
        categories = anime_dict.pop("categories")
    if anime_dict.get("posters", None):
        posters = anime_dict.pop("posters")
    for field, value in anime_dict.items():
        print(field, value)
        setattr(db_anime, field, value)

    new_categories = [
        create_category_if_not_exist(db, cat_name=category) for category in categories
    ]
    new_posters = [
        create_poster_if_not_exist(db, poster_path=poster) for poster in posters
    ]

    print(new_categories, '\n', new_posters)
    db_anime.categories = new_categories
    db_anime.posters = new_posters

    db.commit()
    db.refresh(db_anime)
    return db_anime


def patch_anime(anime_id: int, db: Session, anime: schemas.AnimeCreate):
    db_anime = db.query(models.Anime).filter(models.Anime.id == anime_id).first()
    anime_dict = anime.dict(exclude_unset=True)
    categories = []
    posters = []
    if anime_dict.get("categories", None):
        categories = anime_dict.pop("categories")
    if anime_dict.get("posters", None):
        posters = anime_dict.pop("posters")
    for field, value in anime_dict.items():
        print(field, value)
        setattr(db_anime, field, value)

    new_categories = [
        create_category_if_not_exist(db, cat_name=category) for category in categories
    ]
    new_posters = [
        create_poster_if_not_exist(db, poster_path=poster) for poster in posters
    ]

    print(new_categories, '\n', new_posters)
    db_anime.categories = new_categories
    db_anime.posters = new_posters

    db.commit()
    db.refresh(db_anime)
    return db_anime


def delete_anime(db: Session, anime_id: int):
    db_anime = db.query(models.Anime).filter(models.Anime.id == anime_id).first()
    db.delete(db_anime)
    db.commit()
    return db_anime


def get_poster(db: Session, poster_id: int):
    return db.query(models.Poster).filter(models.Poster.id == poster_id).first()


async def create_poster(db: Session, poster: schemas.PosterCreate):
    db_poster = models.Poster(**poster)
    db.add(db_poster)
    db.commit()
    db.refresh(db_poster)
    return db_poster


def delete_poster(db: Session, poster_id: int):
    db_poster = db.query(models.Poster).filter(models.Poster.id == poster_id).first()
    db.delete(db_poster)
    db.commit()
    if os.path.exists(db_poster.path):
        os.remove(db_poster.path)
    return db_poster


def create_category(db: Session, category: schemas.CategoryCreate):
    try:
        db_category = db.query(models.Category).filter_by(name=category.name).first()
        if db_category:
            return db_category
        print("not created")
        print(category.dict())
        # name=category.name
        db_category = models.Category(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        print(e)
        raise HTTPException(status.HTTP_404_NOT_FOUND, {"msg": "failed create"})


def get_category(cat_id: int, db: Session):
    db_category = db.query(models.Category).filter_by(cat_id=cat_id).first()
    if not db_category:
        raise HTTPException(404, {"msg": "category not found"})
    return db_category


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    db_categories = db.query(models.Category).offset(skip).limit(limit).all()
    if not db_categories:
        raise HTTPException(404, {"msg": "no categories"})
    return db_categories


def delete_category(cat_id: int, db: Session):
    db_category = db.query(models.Category).filter_by(cat_id=cat_id).first()
    if not db_category:
        raise HTTPException(404, {"msg": "category not found"})
    db.delete(db_category)
    db.commit()
    return db_category
