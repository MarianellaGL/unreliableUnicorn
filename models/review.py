from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base
import enum


class ReviewSource(str, enum.Enum):
    TMDB = "tmdb"
    NYT = "nyt"
    GUARDIAN = "guardian"
    OMDB = "omdb"
    OTHER = "other"


class ExternalReview(Base):
    __tablename__ = 'external_reviews'

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete='CASCADE'), nullable=False, index=True)
    source = Column(Enum(ReviewSource), nullable=False, index=True)
    author = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    rating = Column(String(50), nullable=True)  # e.g., "4/5", "Fresh", "Critic's Pick"
    url = Column(String(500), nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    movie = relationship("Movie", back_populates="external_reviews")

    def __repr__(self):
        return f"<ExternalReview(id={self.id}, source='{self.source}', movie_id={self.movie_id})>"
