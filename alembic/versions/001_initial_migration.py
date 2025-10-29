"""Initial migration - create all tables

Revision ID: 001_initial
Revises:
Create Date: 2025-10-29 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create genres table
    op.create_table('genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tmdb_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tmdb_id')
    )
    op.create_index(op.f('ix_genres_id'), 'genres', ['id'], unique=False)
    op.create_index(op.f('ix_genres_name'), 'genres', ['name'], unique=False)
    op.create_index(op.f('ix_genres_tmdb_id'), 'genres', ['tmdb_id'], unique=False)

    # Create movies table
    op.create_table('movies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tmdb_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('original_title', sa.String(length=255), nullable=True),
    sa.Column('overview', sa.Text(), nullable=True),
    sa.Column('release_date', sa.Date(), nullable=True),
    sa.Column('runtime', sa.Integer(), nullable=True),
    sa.Column('poster_url', sa.String(length=255), nullable=True),
    sa.Column('backdrop_url', sa.String(length=255), nullable=True),
    sa.Column('vote_average', sa.Float(), nullable=True),
    sa.Column('vote_count', sa.Integer(), nullable=True),
    sa.Column('popularity', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tmdb_id')
    )
    op.create_index(op.f('ix_movies_id'), 'movies', ['id'], unique=False)
    op.create_index(op.f('ix_movies_title'), 'movies', ['title'], unique=False)
    op.create_index(op.f('ix_movies_tmdb_id'), 'movies', ['tmdb_id'], unique=False)

    # Create movie_genres association table
    op.create_table('movie_genres',
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('movie_id', 'genre_id')
    )

    # Create external_reviews table
    op.create_table('external_reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('source', sa.String(length=50), nullable=False),
    sa.Column('author', sa.String(length=100), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('url', sa.String(length=500), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_external_reviews_id'), 'external_reviews', ['id'], unique=False)
    op.create_index(op.f('ix_external_reviews_movie_id'), 'external_reviews', ['movie_id'], unique=False)
    op.create_index(op.f('ix_external_reviews_source'), 'external_reviews', ['source'], unique=False)

    # Create generated_opinions table
    op.create_table('generated_opinions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('tone', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_generated_opinions_created_at'), 'generated_opinions', ['created_at'], unique=False)
    op.create_index(op.f('ix_generated_opinions_id'), 'generated_opinions', ['id'], unique=False)
    op.create_index(op.f('ix_generated_opinions_movie_id'), 'generated_opinions', ['movie_id'], unique=False)

    # Create user_opinions table
    op.create_table('user_opinions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('author_name', sa.String(length=100), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_opinions_created_at'), 'user_opinions', ['created_at'], unique=False)
    op.create_index(op.f('ix_user_opinions_id'), 'user_opinions', ['id'], unique=False)
    op.create_index(op.f('ix_user_opinions_movie_id'), 'user_opinions', ['movie_id'], unique=False)

    # Create opinion_votes table
    op.create_table('opinion_votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('generated_opinion_id', sa.Integer(), nullable=True),
    sa.Column('user_opinion_id', sa.Integer(), nullable=True),
    sa.Column('vote_type', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['generated_opinion_id'], ['generated_opinions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_opinion_id'], ['user_opinions.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_opinion_votes_generated_opinion_id'), 'opinion_votes', ['generated_opinion_id'], unique=False)
    op.create_index(op.f('ix_opinion_votes_id'), 'opinion_votes', ['id'], unique=False)
    op.create_index(op.f('ix_opinion_votes_user_opinion_id'), 'opinion_votes', ['user_opinion_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_opinion_votes_user_opinion_id'), table_name='opinion_votes')
    op.drop_index(op.f('ix_opinion_votes_id'), table_name='opinion_votes')
    op.drop_index(op.f('ix_opinion_votes_generated_opinion_id'), table_name='opinion_votes')
    op.drop_table('opinion_votes')

    op.drop_index(op.f('ix_user_opinions_movie_id'), table_name='user_opinions')
    op.drop_index(op.f('ix_user_opinions_id'), table_name='user_opinions')
    op.drop_index(op.f('ix_user_opinions_created_at'), table_name='user_opinions')
    op.drop_table('user_opinions')

    op.drop_index(op.f('ix_generated_opinions_movie_id'), table_name='generated_opinions')
    op.drop_index(op.f('ix_generated_opinions_id'), table_name='generated_opinions')
    op.drop_index(op.f('ix_generated_opinions_created_at'), table_name='generated_opinions')
    op.drop_table('generated_opinions')

    op.drop_index(op.f('ix_external_reviews_source'), table_name='external_reviews')
    op.drop_index(op.f('ix_external_reviews_movie_id'), table_name='external_reviews')
    op.drop_index(op.f('ix_external_reviews_id'), table_name='external_reviews')
    op.drop_table('external_reviews')

    op.drop_table('movie_genres')

    op.drop_index(op.f('ix_movies_tmdb_id'), table_name='movies')
    op.drop_index(op.f('ix_movies_title'), table_name='movies')
    op.drop_index(op.f('ix_movies_id'), table_name='movies')
    op.drop_table('movies')

    op.drop_index(op.f('ix_genres_tmdb_id'), table_name='genres')
    op.drop_index(op.f('ix_genres_name'), table_name='genres')
    op.drop_index(op.f('ix_genres_id'), table_name='genres')
    op.drop_table('genres')
