"""Make tmdb_id nullable in genres table

Revision ID: 006_make_tmdb_id_nullable
Revises: 005_add_voter_identifier
Create Date: 2025-10-30

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006_make_tmdb_id_nullable'
down_revision = '005_add_voter_identifier'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Make tmdb_id nullable in genres table to allow user-created genres
    op.alter_column('genres', 'tmdb_id',
                    existing_type=sa.Integer(),
                    nullable=True)


def downgrade() -> None:
    # Make tmdb_id not nullable again (requires all rows to have values)
    op.alter_column('genres', 'tmdb_id',
                    existing_type=sa.Integer(),
                    nullable=False)
