from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

from database import engine
from routers import movies, opinions, votes

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not defined. Check your .env file")

app = FastAPI(
    title="UnreliableUnicorn API",
    description="The Critic You Shouldn't Trust - Real movie data mixed with absurd opinions!",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movies.router)
app.include_router(opinions.router)
app.include_router(votes.router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to UnreliableUnicorn API",
        "tagline": "The Critic You Shouldn't Trust",
        "endpoints": {
            "random_movie": "/pelicula/random",
            "search_movies": "/pelicula/search?q=interstellar",
            "add_opinion": "/pelicula/{id}/opinion",
            "top_opinions": "/opiniones/top",
            "vote_on_opinion": "/vote/opinion/{id}",
            "vote_on_user_opinion": "/vote/user-opinion/{id}",
            "health_check": "/health/db",
            "docs": "/docs"
        }
    }


@app.get("/health/db")
def health_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"db": "ok"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
