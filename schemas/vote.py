from pydantic import BaseModel
from models.vote import VoteType


class VoteCreate(BaseModel):
    """Schema for creating a vote on an opinion"""
    vote_type: VoteType
    voter_identifier: str = None  # Optional IP or session ID


class VoteResponse(BaseModel):
    """Response after voting"""
    id: int
    opinion_id: int
    vote_type: VoteType
    message: str = "Vote registered successfully!"

    class Config:
        from_attributes = True
