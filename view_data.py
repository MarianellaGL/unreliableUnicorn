"""
Simple script to view data in the UnreliableUnicorn database
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Movie, Genre, GeneratedOpinion, ExternalReview

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def main():
    session = Session()

    print("\n" + "="*80)
    print("🦄 UNRELIABLEUNICORN DATABASE VIEWER")
    print("="*80)

    # Count summary
    print("\n📊 DATABASE SUMMARY:")
    print(f"   Total Movies: {session.query(Movie).count()}")
    print(f"   Total Genres: {session.query(Genre).count()}")
    print(f"   Total Reviews: {session.query(ExternalReview).count()}")
    print(f"   Total Generated Opinions: {session.query(GeneratedOpinion).count()}")

    # Show some movies
    print("\n🎬 SAMPLE MOVIES (First 10):")
    print("-" * 80)
    movies = session.query(Movie).limit(10).all()
    for movie in movies:
        genres_str = ", ".join([g.name for g in movie.genres]) if movie.genres else "No genres"
        print(f"\n   [{movie.id}] {movie.title} ({movie.release_date})")
        print(f"       Rating: {movie.vote_average}/10 | Genres: {genres_str}")
        print(f"       Reviews: {len(movie.external_reviews)} | Opinions: {len(movie.generated_opinions)}")

    # Show absurd opinions
    print("\n😂 SAMPLE ABSURD OPINIONS:")
    print("-" * 80)
    opinions = session.query(GeneratedOpinion).join(Movie).limit(10).all()
    for opinion in opinions:
        print(f"\n   🎭 {opinion.movie.title}:")
        print(f"      \"{opinion.content}\"")
        print(f"      Absurdity Score: {opinion.absurdity_score:.2f}/10")

    # Show popular genres
    print("\n🏷️  GENRE DISTRIBUTION:")
    print("-" * 80)
    genres = session.query(Genre).all()
    genre_counts = []
    for genre in genres:
        count = len(genre.movies)
        genre_counts.append((genre.name, count))

    genre_counts.sort(key=lambda x: x[1], reverse=True)
    for genre_name, count in genre_counts[:10]:
        print(f"   {genre_name}: {count} movies")

    print("\n" + "="*80)
    print("✅ Data viewing complete!")
    print("="*80 + "\n")

    session.close()


if __name__ == "__main__":
    main()
