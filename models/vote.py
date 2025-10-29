from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base
import enum


class VoteType(str, enum.Enum):
    UP = "up"
    DOWN = "down"
    LOL = "lol"
    WTF = "wtf"


class OpinionVote(Base):
    __tablename__ = 'opinion_votes'

    id = Column(Integer, primary_key=True, index=True)
    generated_opinion_id = Column(Integer, ForeignKey('generated_opinions.id', ondelete='CASCADE'), nullable=True, index=True)
    user_opinion_id = Column(Integer, ForeignKey('user_opinions.id', ondelete='CASCADE'), nullable=True, index=True)
    vote_type = Column(Enum(VoteType), nullable=False)
    voter_identifier = Column(String(255), nullable=True)  # IP or session ID for anonymous voting
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    generated_opinion = relationship("GeneratedOpinion", back_populates="votes")
    user_opinion = relationship("UserOpinion", back_populates="votes")

    # Constraint: exactly one opinion_id must be set
    __table_args__ = (
        CheckConstraint(
            '(generated_opinion_id IS NOT NULL AND user_opinion_id IS NULL) OR '
            '(generated_opinion_id IS NULL AND user_opinion_id IS NOT NULL)',
            name='ck_opinion_votes_one_opinion'
        ),
    )

    def __repr__(self):
        opinion_id = self.generated_opinion_id or self.user_opinion_id
        opinion_type = "generated" if self.generated_opinion_id else "user"
        return f"<OpinionVote(id={self.id}, {opinion_type}_opinion_id={opinion_id}, vote='{self.vote_type}')>"
