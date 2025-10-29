# UnreliableUnicorn API Architecture

## Database Schema

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   movies    │────────>│ movie_genres │<────────│   genres    │
│             │         │  (junction)  │         │             │
│ id (PK)     │         │ movie_id     │         │ id (PK)     │
│ tmdb_id     │         │ genre_id     │         │ tmdb_id     │
│ title       │         └──────────────┘         │ name        │
│ overview    │                                  └─────────────┘
│ poster_url  │
│ runtime     │
│ ...         │
└─────┬───────┘
      │
      │ (one-to-many)
      │
      ├─────────────────────────────────────────────────┐
      │                                                   │
      ▼                                                   ▼
┌──────────────────┐                          ┌───────────────────┐
│ external_reviews │                          │ generated_opinions│
│                  │                          │                   │
│ id (PK)          │                          │ id (PK)           │
│ movie_id (FK)    │                          │ movie_id (FK)     │
│ source (enum)    │                          │ content           │
│ author           │                          │ absurdity_score   │
│ content          │                          │ generation_method │
│ rating           │                          └────────┬──────────┘
└──────────────────┘                                   │
                                                       │
                                                       ▼
                                             ┌──────────────────┐
                                             │  opinion_votes   │
                                             │                  │
                                             │ id (PK)          │
                                             │ opinion_id (FK)  │
                                             │ vote_type (enum) │
                                             │  - UP            │
                                             │  - DOWN          │
                                             │  - LOL           │
                                             │  - WTF           │
                                             └──────────────────┘
```

## Project Structure

```
unreliableUnicorn/
│
├── models/                  # Database models (SQLAlchemy ORM)
│   ├── base.py             # Base model with metadata
│   ├── movie.py            # Movie & Genre models
│   ├── review.py           # ExternalReview model
│   ├── opinion.py          # GeneratedOpinion & UserOpinion models
│   ├── vote.py             # OpinionVote model
│   └── __init__.py         # Exports all models
│
├── schemas/                 # API request/response schemas (Pydantic)
│   ├── movie.py            # MovieResponse, RandomMovieResponse
│   ├── opinion.py          # OpinionCreate, OpinionResponse, TopOpinionResponse
│   └── __init__.py
│
├── routers/                 # API endpoints (FastAPI routers)
│   ├── movies.py           # /pelicula/* endpoints
│   ├── opinions.py         # /opiniones/* endpoints
│   └── __init__.py
│
├── alembic/                 # Database migrations
│   ├── versions/           # Migration files
│   └── env.py              # Alembic configuration
│
├── main.py                  # FastAPI application entry point
├── database.py              # Database connection & session management
├── populate_db.py           # Script to populate database with TMDb data
├── docker-compose.yml       # Docker services configuration
├── dockerfile               # Container build instructions
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (DATABASE_URL, TMDB_API_KEY)
```

## Data Flow Explained

### Example: GET /pelicula/random

```
1. User Request
   │
   │  GET http://localhost:8000/pelicula/random
   │
   ▼
2. FastAPI (main.py)
   │
   │  Routes request to movies.router
   │
   ▼
3. Router (routers/movies.py)
   │
   │  @router.get("/random")
   │  def get_random_movie(db: Session = Depends(get_db))
   │
   ▼
4. Database Query (SQLAlchemy)
   │
   │  movie = db.query(Movie).order_by(func.rand()).first()
   │  - Fetches random movie from database
   │  - Includes relationships (genres, reviews, opinions)
   │
   ▼
5. Business Logic
   │
   │  - Pick random review from movie.external_reviews
   │  - Pick random opinion from movie.generated_opinions
   │  - Extract genre names from movie.genres
   │
   ▼
6. Response Schema (Pydantic)
   │
   │  RandomMovieResponse(
   │      title=movie.title,
   │      genres=[genre.name for genre in movie.genres],
   │      real_review=random_review.content,
   │      fake_opinion=random_opinion.content
   │  )
   │
   ▼
7. JSON Response
   │
   │  {
   │    "title": "Interstellar",
   │    "genres": ["Adventure", "Drama", "Science Fiction"],
   │    "real_review": "An ambitious space epic...",
   │    "fake_opinion": "The plot twist? My seat was uncomfortable."
   │  }
   │
   ▼
8. User receives response
```

## Key Concepts

### 1. SQLAlchemy Models (models/*.py)
These define the database tables and relationships:

```python
# models/movie.py
class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)

    # Relationships - SQLAlchemy automatically handles JOINs
    genres = relationship("Genre", secondary=movie_genres)
    external_reviews = relationship("ExternalReview")
    generated_opinions = relationship("GeneratedOpinion")
```

When you query a Movie, you can automatically access:
- `movie.genres` → List of Genre objects
- `movie.external_reviews` → List of ExternalReview objects
- `movie.generated_opinions` → List of GeneratedOpinion objects

### 2. Pydantic Schemas (schemas/*.py)
These validate API input/output:

```python
# schemas/movie.py
class RandomMovieResponse(BaseModel):
    title: str
    genres: List[str]
    real_review: Optional[str]
    fake_opinion: str
```

Pydantic ensures:
- Data validation (types match)
- Automatic JSON serialization
- API documentation generation

### 3. FastAPI Routers (routers/*.py)
These handle HTTP requests:

```python
# routers/movies.py
@router.get("/random", response_model=RandomMovieResponse)
def get_random_movie(db: Session = Depends(get_db)):
    # db: Session is automatically injected by FastAPI
    # get_db() provides a database connection for this request

    movie = db.query(Movie).order_by(func.rand()).first()
    # ... business logic ...
    return RandomMovieResponse(...)
```

### 4. Dependency Injection (database.py)
```python
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provides database session
    finally:
        db.close()  # Always closes connection
```

FastAPI automatically:
1. Calls `get_db()` before the request
2. Passes the database session to your function
3. Closes the connection after the response

## The Three Endpoints Explained

### 1. GET /pelicula/random

**What it does**: Returns a random movie with a real review and a fake opinion

**How it works**:
1. Query random movie: `db.query(Movie).order_by(func.rand()).first()`
2. Pick random review: `random.choice(movie.external_reviews)`
3. Pick random opinion: `random.choice(movie.generated_opinions)`
4. Format response with movie data, genres, review, and opinion

**The magic**: Combines real TMDb data with absurd generated opinions!

### 2. POST /pelicula/{movie_id}/opinion

**What it does**: Adds a new user opinion to a movie

**How it works**:
1. Validate movie exists: `db.query(Movie).filter(Movie.id == movie_id).first()`
2. Create new UserOpinion object
3. Save to database: `db.add(new_opinion)` → `db.commit()`
4. Return the created opinion with timestamp

**Input**: JSON with `author_name` and `content`
**Output**: The saved opinion with ID and timestamp

### 3. GET /opiniones/top

**What it does**: Returns top opinions ranked by absurdity score

**How it works**:
1. Complex SQL query with JOINs:
   - JOIN Movie (to get movie title)
   - LEFT JOIN OpinionVote (to count votes)
2. Group by opinion ID
3. Calculate vote counts using SQL CASE statements
4. Order by absurdity_score DESC
5. Limit results

**The query** (simplified):
```sql
SELECT
    opinion.id,
    movie.title,
    opinion.content,
    opinion.absurdity_score,
    COUNT(votes) as vote_count,
    SUM(CASE WHEN vote_type='UP' THEN 1 ELSE 0 END) as up_votes
FROM generated_opinions opinion
JOIN movies movie ON opinion.movie_id = movie.id
LEFT JOIN opinion_votes votes ON opinion.id = votes.opinion_id
GROUP BY opinion.id
ORDER BY absurdity_score DESC
LIMIT 10
```

## How Data Gets Populated

The `populate_db.py` script:

1. **Fetches from TMDb API**:
   - `GET https://api.themoviedb.org/3/genre/movie/list` → Genres
   - `GET https://api.themoviedb.org/3/movie/popular` → Popular movies
   - `GET https://api.themoviedb.org/3/movie/{id}/reviews` → Reviews

2. **Creates database records**:
   ```python
   movie = Movie(
       tmdb_id=movie_data["id"],
       title=movie_data["title"],
       poster_url=f"https://image.tmdb.org/t/p/w500{poster_path}"
   )
   db.add(movie)
   ```

3. **Generates absurd opinions**:
   ```python
   opinion = GeneratedOpinion(
       movie_id=movie.id,
       content=random.choice(ABSURD_TEMPLATES),
       absurdity_score=random.uniform(7.0, 10.0)
   )
   db.add(opinion)
   ```

## Docker Setup

```yaml
# docker-compose.yml
services:
  api:
    build: .           # Builds from dockerfile
    ports:
      - "8000:8000"    # Exposes API on localhost:8000
    depends_on:
      - db             # Waits for database to be healthy

  db:
    image: mysql:8.0
    ports:
      - "3307:3306"    # Exposes MySQL on localhost:3307
    volumes:
      - mysql_data:/var/lib/mysql  # Persists data
```

## Environment Variables (.env)

```
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@db:3306/unreliableunicorn
DB_ROOT_PASSWORD=YOUR_PASSWORD
DB_PASSWORD=YOUR_PASSWORD
TMDB_URL=your_api_key_here
```

- `DATABASE_URL`: Connection string for the database
  - Format: `dialect+driver://user:password@host:port/database`
  - `db` resolves to the database container within Docker network
- `TMDB_URL`: Your TMDb API key for fetching movie data

## Summary

**The Flow**:
1. User makes HTTP request
2. FastAPI routes to appropriate handler
3. Handler queries database using SQLAlchemy
4. Data is processed/formatted
5. Pydantic validates the response
6. JSON is returned to user

**The Mix**:
- **Real data**: Movies, genres, reviews from TMDb
- **Fake data**: Absurd opinions generated from templates
- **User data**: Opinions submitted via POST endpoint

**The Result**:
An API that mixes reality with absurdity, creating "The Critic You Shouldn't Trust" 🦄
