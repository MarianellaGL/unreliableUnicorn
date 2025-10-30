"""Make tmdb_id nullable in movies table

Revision ID: 007_make_movie_tmdb_id_nullable
Revises: 006_make_tmdb_id_nullable
Create Date: 2025-10-30

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '007_make_movie_tmdb_id_nullable'
down_revision = '006_make_tmdb_id_nullable'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Make tmdb_id nullable in movies table to allow user-created movies
    op.alter_column('movies', 'tmdb_id',
                    existing_type=sa.Integer(),
                    nullable=True)


def downgrade() -> None:
    # Make tmdb_id not nullable again (requires all rows to have values)
    op.alter_column('movies', 'tmdb_id',
                    existing_type=sa.Integer(),
                    nullable=False)
