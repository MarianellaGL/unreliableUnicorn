from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base


class GeneratedOpinion(Base):
    __tablename__ = 'generated_opinions'

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete='CASCADE'), nullable=False, index=True)
    content = Column(Text, nullable=False)
    absurdity_score = Column(Float, default=0.0, nullable=False)  # 0-10 scale for how absurd
    generation_method = Column(String(100), nullable=True)  # e.g., "template", "markov", "llm"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    movie = relationship("Movie", back_populates="generated_opinions")
    votes = relationship("OpinionVote", back_populates="generated_opinion", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<GeneratedOpinion(id={self.id}, movie_id={self.movie_id}, absurdity={self.absurdity_score})>"


class UserOpinion(Base):
    __tablename__ = 'user_opinions'

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id', ondelete='CASCADE'), nullable=False, index=True)
    author_name = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    movie = relationship("Movie", back_populates="user_opinions")
    votes = relationship("OpinionVote", back_populates="user_opinion", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<UserOpinion(id={self.id}, movie_id={self.movie_id}, author='{self.author_name}')>"
