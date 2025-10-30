from fastapi import APIRouter, HTTPException, Depends, Request, Security
from sqlalchemy.orm import Session
from typing import Optional

from models import GeneratedOpinion, UserOpinion, OpinionVote
from schemas.vote import VoteCreate, VoteResponse
from database import get_db
from auth import verify_api_key

router = APIRouter(prefix="/vote", tags=["votes"])


@router.post("/opinion/{opinion_id}", response_model=VoteResponse, status_code=201)
def vote_on_generated_opinion(
    opinion_id: int,
    vote_data: VoteCreate,
    request: Request,
    db: Session = Depends(get_db),
    api_key: str = Security(verify_api_key)
):
    """
    Vote on a generated opinion.

    Vote types:
    - UP: You liked it
    - DOWN: You didn't like it
    - LOL: It made you laugh
    - WTF: It's so absurd you can't even
    """
    # Check if opinion exists
    opinion = db.query(GeneratedOpinion).filter(GeneratedOpinion.id == opinion_id).first()
    if not opinion:
        raise HTTPException(status_code=404, detail=f"Generated opinion with id {opinion_id} not found")

    # Use provided voter_identifier or fall back to IP address
    voter_id = vote_data.voter_identifier or request.client.host

    # Create vote
    new_vote = OpinionVote(
        generated_opinion_id=opinion_id,
        vote_type=vote_data.vote_type,
        voter_identifier=voter_id
    )

    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)

    return VoteResponse(
        id=new_vote.id,
        opinion_id=opinion_id,
        vote_type=new_vote.vote_type,
        message=f"Your {vote_data.vote_type.value.upper()} vote has been registered!"
    )


@router.post("/user-opinion/{opinion_id}", response_model=VoteResponse, status_code=201)
def vote_on_user_opinion(
    opinion_id: int,
    vote_data: VoteCreate,
    request: Request,
    db: Session = Depends(get_db),
    api_key: str = Security(verify_api_key)
):
    """
    Vote on a user-submitted opinion.

    Vote types:
    - UP: You liked it
    - DOWN: You didn't like it
    - LOL: It made you laugh
    - WTF: It's so absurd you can't even
    """
    # Check if opinion exists
    opinion = db.query(UserOpinion).filter(UserOpinion.id == opinion_id).first()
    if not opinion:
        raise HTTPException(status_code=404, detail=f"User opinion with id {opinion_id} not found")

    # Use provided voter_identifier or fall back to IP address
    voter_id = vote_data.voter_identifier or request.client.host

    # Create vote
    new_vote = OpinionVote(
        user_opinion_id=opinion_id,
        vote_type=vote_data.vote_type,
        voter_identifier=voter_id
    )

    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)

    return VoteResponse(
        id=new_vote.id,
        opinion_id=opinion_id,
        vote_type=new_vote.vote_type,
        message=f"Your {vote_data.vote_type.value.upper()} vote has been registered!"
    )
