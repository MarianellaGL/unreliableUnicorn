import random
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional, List

from models import Movie, ExternalReview, GeneratedOpinion, UserOpinion
from schemas.movie import RandomMovieResponse, MovieResponse
from schemas.opinion import OpinionCreate, OpinionResponse
from database import get_db

router = APIRouter(prefix="/pelicula", tags=["movies"])


@router.get("/random", response_model=RandomMovieResponse)
def get_random_movie(db: Session = Depends(get_db)):
    """
    Returns a random movie with one real review and one fake, funny opinion.

    The magic of UnreliableUnicorn: mixing authentic reviews with absurd opinions!
    """
    # Get a random movie
    movie = db.query(Movie).order_by(func.rand()).first()

    if not movie:
        raise HTTPException(status_code=404, detail="No movies found in database")

    # Get a random real review (if exists)
    real_review_text = None
    if movie.external_reviews:
        random_review = random.choice(movie.external_reviews)
        real_review_text = random_review.content

    # Get a random fake opinion
    fake_opinion_text = "This movie is unreliable... like a unicorn!"
    if movie.generated_opinions:
        random_opinion = random.choice(movie.generated_opinions)
        fake_opinion_text = random_opinion.content

    # Format genres as list of names
    genre_names = [genre.name for genre in movie.genres]

    return RandomMovieResponse(
        title=movie.title,
        original_title=movie.original_title,
        poster_url=movie.poster_url,
        backdrop_url=movie.backdrop_url,
        release_date=movie.release_date,
        runtime=movie.runtime,
        vote_average=movie.vote_average,
        genres=genre_names,
        real_review=real_review_text,
        fake_opinion=fake_opinion_text
    )


@router.post("/{movie_id}/opinion", response_model=OpinionResponse, status_code=201)
def add_opinion(
    movie_id: int,
    opinion_data: OpinionCreate,
    db: Session = Depends(get_db)
):
    """
    Adds a new (possibly ridiculous) opinion for a movie.

    Submit your own take on the movie - absurd or not, we won't judge!
    """
    # Check if movie exists
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie with id {movie_id} not found")

    # Create new user opinion
    new_opinion = UserOpinion(
        movie_id=movie_id,
        author_name=opinion_data.author_name,
        content=opinion_data.content
    )

    db.add(new_opinion)
    db.commit()
    db.refresh(new_opinion)

    return OpinionResponse(
        id=new_opinion.id,
        movie_id=new_opinion.movie_id,
        movie_title=movie.title,
        author_name=new_opinion.author_name,
        content=new_opinion.content,
        created_at=new_opinion.created_at.isoformat()
    )


@router.get("/search", response_model=List[MovieResponse])
def search_movies(
    q: str = Query(..., min_length=1, description="Search query for movie title"),
    limit: int = Query(default=10, ge=1, le=50, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Search for movies by title.

    Returns movies that match the search query in their title or original title.
    """
    search_pattern = f"%{q}%"

    movies = db.query(Movie).filter(
        or_(
            Movie.title.ilike(search_pattern),
            Movie.original_title.ilike(search_pattern)
        )
    ).limit(limit).all()

    if not movies:
        raise HTTPException(status_code=404, detail=f"No movies found matching '{q}'")

    return movies
