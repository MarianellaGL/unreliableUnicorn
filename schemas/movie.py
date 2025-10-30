from typing import Optional, List, Union
from pydantic import BaseModel, validator, Field, HttpUrl
from datetime import date


class GenreSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MovieCreate(BaseModel):
    """Schema for creating a new movie"""
    title: str = Field(..., min_length=1, max_length=255, description="Movie title")
    original_title: Optional[str] = Field(None, max_length=255, description="Original title")
    overview: Optional[str] = Field(None, max_length=5000, description="Movie overview/synopsis")
    release_date: Optional[str] = Field(None, description="Release date (YYYY-MM-DD format)")
    runtime: Optional[int] = Field(None, ge=1, description="Runtime in minutes")
    poster_url: Optional[str] = Field(None, max_length=500, description="URL to poster image")
    backdrop_url: Optional[str] = Field(None, max_length=500, description="URL to backdrop image")
    genre_names: List[str] = Field(default=[], description="List of genre names (e.g., ['Action', 'Drama'])")


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
    id: int
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
