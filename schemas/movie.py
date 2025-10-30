from typing import Optional, List
from pydantic import BaseModel, field_serializer
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

    @field_serializer('release_date')
    def serialize_release_date(self, value: Optional[date]) -> Optional[str]:
        return value.isoformat() if value else None

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
