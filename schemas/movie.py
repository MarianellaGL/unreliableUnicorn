from typing import Optional, List, Union
from pydantic import BaseModel, validator
from datetime import date


class GenreSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MovieResponse(BaseModel):
    id: int
    title: str
    original_title: Optional[str]
    overview: Optional[str]
    release_date: Optional[str]
    runtime: Optional[int]
    poster_url: Optional[str]
    backdrop_url: Optional[str]
    vote_average: Optional[float]
    vote_count: Optional[int]
    genres: List[GenreSchema] = []

    @validator('release_date', pre=True)
    def convert_date_to_string(cls, v):
        if isinstance(v, date):
            return v.isoformat()
        return v

    class Config:
        from_attributes = True


class RandomMovieResponse(BaseModel):
    """Response for GET /pelicula/random"""
    title: str
    original_title: Optional[str]
    poster_url: Optional[str]
    backdrop_url: Optional[str]
    release_date: Optional[str]
    runtime: Optional[int]
    vote_average: Optional[float]
    genres: List[str] = []
    real_review: Optional[str] = None
    fake_opinion: str

    class Config:
        from_attributes = True
