from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base


# Association table for many-to-many relationship between movies and genres
movie_genres = Table(
    'movie_genres',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True)
)


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, unique=True, nullable=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    original_title = Column(String(255), nullable=True)
    overview = Column(Text, nullable=True)
    release_date = Column(String(50), nullable=True)
    runtime = Column(Integer, nullable=True)  # in minutes
    poster_url = Column(String(500), nullable=True)
    backdrop_url = Column(String(500), nullable=True)
    vote_average = Column(Float, nullable=True)
    vote_count = Column(Integer, nullable=True)
    popularity = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
    external_reviews = relationship("ExternalReview", back_populates="movie", cascade="all, delete-orphan")
    generated_opinions = relationship("GeneratedOpinion", back_populates="movie", cascade="all, delete-orphan")
    user_opinions = relationship("UserOpinion", back_populates="movie", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Movie(id={self.id}, title='{self.title}')>"


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, unique=True, nullable=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)

    # Relationships
    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")

    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"
