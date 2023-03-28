from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Float
from sqlalchemy.orm import relationship
from database import Base


class Anime(Base):
    __tablename__ = "animes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), unique=True, nullable=False)
    alias = Column(String(128))
    created_time = Column(DateTime, server_default=func.now())
    updated_time = Column(DateTime, onupdate=func.now())
    watch_count = Column(Integer, default=1)
    year = Column(String(8))
    rating = Column(Float, default=10.0)
    region = Column(String(32))
    studio = Column(String(32))
    release_date = Column(String(32))
    end_date = Column(String(32))
    description = Column(String(255))
    watch_dates = Column(String(128))
    categories = relationship(
        "Category",
        secondary="anime_category",
        back_populates="animes",
        overlaps="animes",
    )
    posters = relationship("Poster", back_populates="anime")


class Poster(Base):
    __tablename__ = "posters"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(255), nullable=False)
    anime_id = Column(Integer, ForeignKey("animes.id"))
    anime = relationship("Anime", back_populates="posters")


class AnimeCategory(Base):
    __tablename__ = "anime_category"
    an_cat_id = Column(Integer, primary_key=True, index=True)
    anime_id = Column(Integer, ForeignKey('animes.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(24), unique=True, nullable=False)
    animes = relationship(
        'Anime',
        secondary="anime_category",
        back_populates='categories',
        overlaps="categories",
    )
