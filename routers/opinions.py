from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List

from models import GeneratedOpinion, Movie, OpinionVote, VoteType
from schemas.opinion import TopOpinionResponse
from database import get_db

router = APIRouter(prefix="/opiniones", tags=["opinions"])


@router.get("/top", response_model=List[TopOpinionResponse])
def get_top_opinions(
    limit: int = Query(default=10, ge=1, le=100, description="Number of opinions to return"),
    db: Session = Depends(get_db)
):
    """
    Lists the top absurd or most up-voted generated opinions.

    Ranked by a combination of absurdity score and vote balance.
    Because the best opinions are the ones that make you question reality!
    """
    # Build query with vote counts
    opinions_query = db.query(
        GeneratedOpinion.id,
        GeneratedOpinion.movie_id,
        Movie.title.label("movie_title"),
        GeneratedOpinion.content,
        GeneratedOpinion.absurdity_score,
        GeneratedOpinion.generation_method,
        func.count(OpinionVote.id).label("vote_count"),
        func.sum(case((OpinionVote.vote_type == VoteType.UP, 1), else_=0)).label("up_votes"),
        func.sum(case((OpinionVote.vote_type == VoteType.DOWN, 1), else_=0)).label("down_votes"),
        func.sum(case((OpinionVote.vote_type == VoteType.LOL, 1), else_=0)).label("lol_votes"),
        func.sum(case((OpinionVote.vote_type == VoteType.WTF, 1), else_=0)).label("wtf_votes"),
    ).join(
        Movie, GeneratedOpinion.movie_id == Movie.id
    ).outerjoin(
        OpinionVote, GeneratedOpinion.id == OpinionVote.generated_opinion_id
    ).group_by(
        GeneratedOpinion.id
    ).order_by(
        # Sort by absurdity score first, then by vote balance
        GeneratedOpinion.absurdity_score.desc(),
        (func.sum(case((OpinionVote.vote_type == VoteType.UP, 1), else_=0)) -
         func.sum(case((OpinionVote.vote_type == VoteType.DOWN, 1), else_=0))).desc()
    ).limit(limit)

    results = opinions_query.all()

    # Format response
    response = []
    for row in results:
        response.append(TopOpinionResponse(
            id=row.id,
            movie_id=row.movie_id,
            movie_title=row.movie_title,
            content=row.content,
            absurdity_score=row.absurdity_score,
            generation_method=row.generation_method,
            vote_count=row.vote_count or 0,
            up_votes=row.up_votes or 0,
            down_votes=row.down_votes or 0,
            lol_votes=row.lol_votes or 0,
            wtf_votes=row.wtf_votes or 0
        ))

    return response
