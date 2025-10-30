from typing import Optional
from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    """Schema for creating an anonymous review"""
    author: Optional[str] = Field(None, max_length=255, description="Optional author name (default: 'Anonymous')")
    content: str = Field(..., min_length=10, max_length=5000, description="Review content")
    rating: Optional[str] = Field(None, max_length=50, description="Optional rating (e.g., '4/5', '8/10')")


class ReviewResponse(BaseModel):
    """Schema for review response"""
    id: int
    movie_id: int
    movie_title: str
    source: str
    author: Optional[str]
    content: str
    rating: Optional[str]
    created_at: str

    class Config:
        from_attributes = True
