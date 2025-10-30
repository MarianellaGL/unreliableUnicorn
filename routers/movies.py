import random
from fastapi import APIRouter, HTTPException, Depends, Query, Security
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional, List

from models import Movie, ExternalReview, GeneratedOpinion, UserOpinion, Genre
from models.review import ReviewSource
from schemas.movie import RandomMovieResponse, MovieResponse, MovieCreate, MovieDetailResponse
from schemas.opinion import OpinionCreate, OpinionResponse, GeneratedOpinionCreate, GeneratedOpinionResponse
from schemas.review import ReviewCreate, ReviewResponse
from database import get_db
from auth import verify_api_key

router = APIRouter(prefix="/pelicula", tags=["movies"])


@router.get("/random", response_model=RandomMovieResponse)
def get_random_movie(db: Session = Depends(get_db)):
    """
    Returns a random movie with one real review and one fake, funny opinion.

    The magic of UnreliableUnicorn: mixing authentic reviews with absurd opinions!
    """
    # Get a random movie (PostgreSQL uses random(), MySQL uses rand())
    movie = db.query(Movie).order_by(func.random()).first()

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

    # Convert date to string if it exists
    release_date_str = movie.release_date.isoformat() if movie.release_date else None

    return RandomMovieResponse(
        id=movie.id,
        title=movie.title,
        original_title=movie.original_title,
        poster_url=movie.poster_url,
        backdrop_url=movie.backdrop_url,
        release_date=release_date_str,
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
    db: Session = Depends(get_db),
    api_key: str = Security(verify_api_key)
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


@router.post("/{movie_id}/absurd-opinion", response_model=GeneratedOpinionResponse, status_code=201)
def add_absurd_opinion(
    movie_id: int,
    opinion_data: GeneratedOpinionCreate,
    db: Session = Depends(get_db),
    api_key: str = Security(verify_api_key)
):
    """
    Create an absurd/generated opinion for a movie.

    Generate hilarious, nonsensical, or satirical opinions with an absurdity score.
    Perfect for adding humor to movie reviews!
    """
    # Check if movie exists
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie with id {movie_id} not found")

    # Create new generated opinion
    new_opinion = GeneratedOpinion(
        movie_id=movie_id,
        content=opinion_data.content,
        absurdity_score=opinion_data.absurdity_score,
        generation_method=opinion_data.generation_method or "manual"
    )

    db.add(new_opinion)
    db.commit()
    db.refresh(new_opinion)

    return GeneratedOpinionResponse(
        id=new_opinion.id,
        movie_id=new_opinion.movie_id,
        movie_title=movie.title,
        content=new_opinion.content,
        absurdity_score=new_opinion.absurdity_score,
        generation_method=new_opinion.generation_method,
        created_at=new_opinion.created_at.isoformat()
    )


@router.post("/{movie_id}/review", response_model=ReviewResponse, status_code=201)
def add_anonymous_review(
    movie_id: int,
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    api_key: str = Security(verify_api_key)
):
    """
    Submit an anonymous review for a movie.

    Help fill in the gaps! If a movie doesn't have real reviews yet,
    you can submit your own honest take on it.
    """
    # Check if movie exists
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie with id {movie_id} not found")

    # Create new anonymous review
    new_review = ExternalReview(
        movie_id=movie_id,
        source=ReviewSource.USER,
        author=review_data.author if review_data.author else "Anonymous",
        content=review_data.content,
        rating=review_data.rating
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return ReviewResponse(
        id=new_review.id,
        movie_id=new_review.movie_id,
        movie_title=movie.title,
        source=new_review.source.value,
        author=new_review.author,
        content=new_review.content,
        rating=new_review.rating,
        created_at=new_review.created_at.isoformat()
    )


@router.post("/", response_model=MovieResponse, status_code=201)
def create_movie(
    movie_data: MovieCreate,
    db: Session = Depends(get_db),
    api_key: str = Security(verify_api_key)
):
    """
    Upload a new movie to the catalog.

    Don't see your favorite movie? Add it yourself! Include title, overview,
    release date, and image URLs. We'll add it to our unreliable collection!
    """
    # Check if movie already exists by title
    existing_movie = db.query(Movie).filter(
        or_(
            Movie.title == movie_data.title,
            Movie.original_title == movie_data.title
        )
    ).first()

    if existing_movie:
        raise HTTPException(
            status_code=409,
            detail=f"Movie '{movie_data.title}' already exists in the catalog"
        )

    # Create new movie
    new_movie = Movie(
        title=movie_data.title,
        original_title=movie_data.original_title,
        overview=movie_data.overview,
        release_date=movie_data.release_date,
        runtime=movie_data.runtime,
        poster_url=movie_data.poster_url,
        backdrop_url=movie_data.backdrop_url
    )

    # Handle genres
    for genre_name in movie_data.genre_names:
        # Try to find existing genre or create new one
        genre = db.query(Genre).filter(Genre.name == genre_name).first()
        if not genre:
            genre = Genre(name=genre_name)
            db.add(genre)
        new_movie.genres.append(genre)

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return new_movie


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


@router.get("/{movie_id}", response_model=MovieDetailResponse)
def get_movie_by_id(
    movie_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific movie by its ID.

    Returns detailed information including a random real review and fake opinion.
    """
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie with id {movie_id} not found")

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

    return MovieDetailResponse(
        id=movie.id,
        title=movie.title,
        original_title=movie.original_title,
        overview=movie.overview,
        poster_url=movie.poster_url,
        backdrop_url=movie.backdrop_url,
        release_date=movie.release_date,
        runtime=movie.runtime,
        vote_average=movie.vote_average,
        vote_count=movie.vote_count,
        genres=movie.genres,
        real_review=real_review_text,
        fake_opinion=fake_opinion_text
    )
