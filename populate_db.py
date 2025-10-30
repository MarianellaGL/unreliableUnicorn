"""
Script to populate the UnreliableUnicorn database with movie data from TMDb
"""
import os
import random
from datetime import datetime
from dotenv import load_dotenv
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Movie, Genre, ExternalReview, GeneratedOpinion, ReviewSource

load_dotenv()

# Configuration
TMDB_API_KEY = os.getenv("TMDB_URL")  # Note: env var is named TMDB_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Fix Render's postgres:// URL to postgresql:// for SQLAlchemy
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Absurd opinion templates for generation
ABSURD_TEMPLATES = [
    "I cried, I laughed, then I realized I was watching the wrong movie 🎬",
    "This film changed my life. Now I only eat popcorn for breakfast.",
    "The plot twist? My seat was uncomfortable the whole time.",
    "10/10 would watch again, but only if forced at gunpoint 🔫",
    "I transcended to another dimension. Turns out it was just the bathroom.",
    "My popcorn had better character development than the protagonist.",
    "This movie cured my insomnia... by giving me nightmares instead.",
    "I left the theater questioning everything. Mostly why I paid for parking.",
    "The cinematography was stunning. I spent most of the time on my phone though.",
    "This film speaks to the human condition. Specifically, the condition of needing a refund.",
    "A masterpiece of cinema. My cat agreed, she slept through the whole thing.",
    "The director's vision was clear: make me regret all my life choices.",
    "I haven't felt this emotionally connected since my WiFi went down.",
    "The acting was so realistic, I forgot I was supposed to be entertained.",
    "This movie is a metaphor for life: confusing and too long.",
    "I laughed, I cried, I wondered if the exit was still unlocked 🚪",
    "The plot holes were so big, I fell into one and never came back.",
    "My expectations were low, and somehow they still weren't met.",
    "This film challenged everything I know about staying awake.",
    "A visual feast! Unfortunately I was expecting emotional nutrition.",
]

# Create database connection
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def fetch_genres():
    """Fetch movie genres from TMDb"""
    print("📚 Fetching genres from TMDb...")
    url = f"{TMDB_BASE_URL}/genre/movie/list"
    params = {"api_key": TMDB_API_KEY}

    with httpx.Client() as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("genres", [])


def fetch_popular_movies(pages=5):
    """Fetch popular movies from TMDb"""
    print(f"🎬 Fetching popular movies from TMDb (up to {pages} pages)...")
    movies = []

    with httpx.Client() as client:
        for page in range(1, pages + 1):
            print(f"   Fetching page {page}...")
            url = f"{TMDB_BASE_URL}/movie/popular"
            params = {"api_key": TMDB_API_KEY, "page": page}

            response = client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            movies.extend(data.get("results", []))

    print(f"   ✓ Fetched {len(movies)} movies")
    return movies


def fetch_movie_details(movie_id):
    """Fetch detailed movie information"""
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {"api_key": TMDB_API_KEY}

    with httpx.Client() as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        return response.json()


def fetch_movie_reviews(movie_id):
    """Fetch reviews for a movie from TMDb"""
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/reviews"
    params = {"api_key": TMDB_API_KEY, "page": 1}

    with httpx.Client() as client:
        response = client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])


def populate_genres(session):
    """Populate genres table"""
    genres_data = fetch_genres()

    for genre_data in genres_data:
        existing = session.query(Genre).filter_by(tmdb_id=genre_data["id"]).first()
        if not existing:
            genre = Genre(
                tmdb_id=genre_data["id"],
                name=genre_data["name"]
            )
            session.add(genre)

    session.commit()
    print(f"✓ Added {len(genres_data)} genres")
    return {g["id"]: g["name"] for g in genres_data}


def populate_movies(session, genre_map, num_pages=5):
    """Populate movies, reviews, and opinions"""
    movies_data = fetch_popular_movies(pages=num_pages)
    added_count = 0

    for i, movie_data in enumerate(movies_data, 1):
        try:
            # Check if movie already exists
            existing = session.query(Movie).filter_by(tmdb_id=movie_data["id"]).first()
            if existing:
                print(f"   [{i}/{len(movies_data)}] Skipping {movie_data.get('title')} (already exists)")
                continue

            print(f"   [{i}/{len(movies_data)}] Adding {movie_data.get('title')}...")

            # Fetch detailed info
            details = fetch_movie_details(movie_data["id"])

            # Create movie
            movie = Movie(
                tmdb_id=movie_data["id"],
                title=movie_data.get("title"),
                original_title=movie_data.get("original_title"),
                overview=movie_data.get("overview"),
                release_date=movie_data.get("release_date"),
                runtime=details.get("runtime"),
                poster_url=f"{TMDB_IMAGE_BASE}{movie_data['poster_path']}" if movie_data.get("poster_path") else None,
                backdrop_url=f"{TMDB_IMAGE_BASE}{movie_data['backdrop_path']}" if movie_data.get("backdrop_path") else None,
                vote_average=movie_data.get("vote_average"),
                vote_count=movie_data.get("vote_count"),
                popularity=movie_data.get("popularity")
            )
            session.add(movie)
            session.flush()  # Get the movie ID

            # Add genres
            for genre_id in movie_data.get("genre_ids", []):
                genre = session.query(Genre).filter_by(tmdb_id=genre_id).first()
                if genre:
                    movie.genres.append(genre)

            # Fetch and add reviews from TMDb
            reviews = fetch_movie_reviews(movie_data["id"])
            for review_data in reviews[:2]:  # Limit to 2 reviews per movie
                review = ExternalReview(
                    movie_id=movie.id,
                    source=ReviewSource.TMDB,
                    author=review_data.get("author"),
                    content=review_data.get("content")[:1000],  # Truncate long reviews
                    rating=str(review_data.get("author_details", {}).get("rating", "")),
                    url=review_data.get("url"),
                    created_at=datetime.utcnow()
                )
                session.add(review)

            # Generate 2-4 absurd opinions per movie
            num_opinions = random.randint(2, 4)
            for _ in range(num_opinions):
                opinion = GeneratedOpinion(
                    movie_id=movie.id,
                    content=random.choice(ABSURD_TEMPLATES),
                    absurdity_score=random.uniform(7.0, 10.0),
                    generation_method="template",
                    created_at=datetime.utcnow()
                )
                session.add(opinion)

            session.commit()
            added_count += 1

        except Exception as e:
            print(f"   ✗ Error adding {movie_data.get('title')}: {e}")
            session.rollback()
            continue

    print(f"✓ Successfully added {added_count} movies with reviews and opinions")


def main():
    """Main population function"""
    print("\n🦄 UnreliableUnicorn Database Population Script\n")
    print("=" * 60)

    if not TMDB_API_KEY:
        print("❌ Error: TMDB_URL not found in .env file")
        return

    if not DATABASE_URL:
        print("❌ Error: DATABASE_URL not found in .env file")
        return

    session = Session()

    try:
        # Step 1: Populate genres
        print("\n[1/2] Populating genres...")
        genre_map = populate_genres(session)

        # Step 2: Populate movies (with reviews and opinions)
        print("\n[2/2] Populating movies, reviews, and opinions...")
        populate_movies(session, genre_map, num_pages=5)  # Fetch 5 pages (~100 movies)

        # Summary
        print("\n" + "=" * 60)
        print("✅ Database population complete!\n")
        print("Summary:")
        print(f"   Genres: {session.query(Genre).count()}")
        print(f"   Movies: {session.query(Movie).count()}")
        print(f"   Reviews: {session.query(ExternalReview).count()}")
        print(f"   Generated Opinions: {session.query(GeneratedOpinion).count()}")
        print()

    except Exception as e:
        print(f"\n❌ Error during population: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
