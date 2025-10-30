# 🦄 UnreliableUnicorn API

[![Docker Hub](https://img.shields.io/docker/v/marianellagl/unreliableunicorn?label=docker&logo=docker)](https://hub.docker.com/r/marianellagl/unreliableunicorn)
[![Docker Image Size](https://img.shields.io/docker/image-size/marianellagl/unreliableunicorn/latest)](https://hub.docker.com/r/marianellagl/unreliableunicorn)

**"The Critic You Shouldn't Trust"**

A playful REST API that serves real movie data mixed with nonsensical, sarcastic, or hilariously absurd opinions. It blends authentic reviews from TMDb with AI-generated humor, creating unpredictable movie critiques that make no sense—but are always entertaining.

## Features

- 🎬 **100 Real Movies** from TMDb with authentic metadata
- 📊 **19 Genres** (Action, Horror, Thriller, etc.)
- ⭐ **94 Real Reviews** from TMDb users
- 😂 **294 Absurd Opinions** with absurdity scores (7-10/10)
- 🗳️ **Voting System** (up, down, lol, wtf)
- 📝 **User-Generated Content**: Submit anonymous reviews for movies
- ➕ **Community Catalog**: Upload new movies with posters and metadata

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message with endpoint list |
| `/pelicula/random` | GET | Random movie with real review + fake opinion |
| `/pelicula/search` | GET | Search movies by title |
| `/pelicula/` | POST | **NEW!** Upload a new movie to the catalog |
| `/pelicula/{id}/opinion` | POST | Add your own opinion to a movie |
| `/pelicula/{id}/review` | POST | **NEW!** Submit an anonymous review for a movie |
| `/opiniones/top` | GET | Top-ranked absurd opinions |
| `/vote/opinion/{id}` | POST | Vote on a generated opinion |
| `/vote/user-opinion/{id}` | POST | Vote on a user opinion |
| `/health/db` | GET | Database health check |
| `/docs` | GET | Interactive API documentation |

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MySQL / PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Containerization**: Docker
- **External API**: TMDb API

## Quick Start

### Option 1: Using Docker Hub (Fastest)

Pull and run the pre-built image from Docker Hub:

```bash
# Pull the image
docker pull marianellagl/unreliableunicorn:latest

# Run with MySQL database
docker run -d \
  --name unreliableunicorn_api \
  -p 8000:8000 \
  -e DATABASE_URL="mysql+pymysql://root:YOUR_PASSWORD@host.docker.internal:3306/unreliableunicorn?charset=utf8mb4" \
  -e TMDB_URL="your_tmdb_api_key_here" \
  marianellagl/unreliableunicorn:latest
```

Then access:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs

### Option 2: Using Docker Compose (Full Setup)

Clone and run the complete stack with database included.

#### Prerequisites
- Docker & Docker Compose
- TMDb API Key (get it free at https://www.themoviedb.org/settings/api)

#### Setup

1. **Clone the repository**
```bash
git clone https://github.com/MarianellaGL/unreliableUnicorn.git
cd unreliableUnicorn
```

2. **Create `.env` file**
```bash
# Copy the example file and edit with your credentials
cp .env.example .env

# Then edit .env with your actual values:
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@db:3306/unreliableunicorn?charset=utf8mb4
DB_ROOT_PASSWORD=YOUR_PASSWORD
DB_PASSWORD=YOUR_PASSWORD
TMDB_URL=your_tmdb_api_key_here
```

3. **Start services**
```bash
docker-compose up -d --build
```

4. **Populate database**
```bash
docker exec unreliableunicorn_api python populate_db.py
```

5. **Access the API**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Database: localhost:3307 (MySQL Workbench)

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to Render.com (free tier available).

Quick deploy button:
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## Example Responses

### GET /pelicula/random

```json
{
  "title": "Interstellar",
  "poster_url": "https://image.tmdb.org/t/p/w500/...",
  "release_date": "2014-11-05",
  "runtime": 169,
  "vote_average": 8.462,
  "genres": ["Adventure", "Drama", "Science Fiction"],
  "real_review": "An ambitious, emotional, and visually stunning space epic.",
  "fake_opinion": "The plot twist? My seat was uncomfortable the whole time."
}
```

### POST /pelicula/ (Upload Movie)

**Request:**
```json
{
  "title": "My Favorite Film",
  "original_title": "Mon Film Préféré",
  "overview": "A captivating story about...",
  "release_date": "2024-12-01",
  "runtime": 120,
  "poster_url": "https://example.com/poster.jpg",
  "backdrop_url": "https://example.com/backdrop.jpg",
  "genre_names": ["Drama", "Romance"]
}
```

**Response:**
```json
{
  "id": 101,
  "title": "My Favorite Film",
  "original_title": "Mon Film Préféré",
  "overview": "A captivating story about...",
  "release_date": "2024-12-01",
  "runtime": 120,
  "poster_url": "https://example.com/poster.jpg",
  "backdrop_url": "https://example.com/backdrop.jpg",
  "vote_average": null,
  "vote_count": null,
  "genres": [
    {"id": 18, "name": "Drama"},
    {"id": 10749, "name": "Romance"}
  ]
}
```

### POST /pelicula/{movie_id}/review (Anonymous Review)

**Request:**
```json
{
  "author": "Anonymous",
  "content": "This movie was incredible! The cinematography and acting were top-notch.",
  "rating": "9/10"
}
```

**Response:**
```json
{
  "id": 250,
  "movie_id": 101,
  "movie_title": "My Favorite Film",
  "source": "user",
  "author": "Anonymous",
  "content": "This movie was incredible! The cinematography and acting were top-notch.",
  "rating": "9/10",
  "created_at": "2025-10-30T14:15:30"
}
```

### GET /opiniones/top?limit=3

```json
[
  {
    "id": 12,
    "movie_title": "Hunting Grounds",
    "content": "A masterpiece of cinema. My cat agreed, she slept through the whole thing.",
    "absurdity_score": 9.99,
    "vote_count": 0,
    "up_votes": 0,
    "down_votes": 0,
    "lol_votes": 0,
    "wtf_votes": 0
  }
]
```

## Project Structure

```
unreliableUnicorn/
├── models/              # SQLAlchemy database models
├── schemas/             # Pydantic request/response schemas
├── routers/             # FastAPI endpoint handlers
├── alembic/             # Database migrations
├── main.py              # Application entry point
├── database.py          # Database connection
├── populate_db.py       # TMDb data importer
├── docker-compose.yml   # Local development setup
├── dockerfile           # Container configuration
└── render.yaml          # Render.com deployment config
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## Development

### Run migrations
```bash
docker exec unreliableunicorn_api alembic upgrade head
```

### Create new migration
```bash
docker exec unreliableunicorn_api alembic revision --autogenerate -m "description"
```

### View data
```bash
docker exec unreliableunicorn_api python view_data.py
```

### Access MySQL
```bash
docker exec -it unreliableunicorn_db mysql -uroot -pYOUR_PASSWORD unreliableunicorn
```

## Contributing

This is a learning project, but feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## Future Enhancements

- [ ] User authentication (JWT)
- [x] ~~Search and filter endpoints~~ ✅ Implemented
- [x] ~~User-submitted reviews~~ ✅ Implemented
- [x] ~~Movie upload functionality~~ ✅ Implemented
- [ ] Vote functionality implementation
- [ ] NYT & Guardian API integration
- [ ] Frontend web app (React/Vue)
- [ ] More absurd opinion templates
- [ ] LLM-generated opinions
- [ ] Image upload service (instead of URLs)

## License

MIT License - feel free to use this project for learning!

## Credits

- Movie data: [TMDb API](https://www.themoviedb.org/documentation/api)
- Built with: FastAPI, SQLAlchemy, Docker
- Inspired by: The need for unreliable movie critics 🦄

---

Made with ❤️ and a bit of absurdity
