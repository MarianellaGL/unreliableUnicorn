from typing import Optional
from pydantic import BaseModel, Field


class OpinionCreate(BaseModel):
    """Schema for creating a new opinion"""
    author_name: Optional[str] = Field(None, max_length=255)
    content: str = Field(..., min_length=1, max_length=5000)


class OpinionResponse(BaseModel):
    """Response after creating an opinion"""
    id: int
    movie_id: int
    movie_title: str
    author_name: Optional[str]
    content: str
    created_at: str

    class Config:
        from_attributes = True


class TopOpinionResponse(BaseModel):
    """Response for top opinions"""
    id: int
    movie_id: int
    movie_title: str
    content: str
    absurdity_score: float
    generation_method: Optional[str]
    vote_count: int = 0
    up_votes: int = 0
    down_votes: int = 0
    lol_votes: int = 0
    wtf_votes: int = 0

    class Config:
        from_attributes = True
