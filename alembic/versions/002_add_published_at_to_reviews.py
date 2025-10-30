"""Add published_at to external_reviews

Revision ID: 002_add_published_at
Revises: 001_initial
Create Date: 2025-10-29 20:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002_add_published_at'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add published_at column to external_reviews
    op.add_column('external_reviews', sa.Column('published_at', sa.DateTime(), nullable=True))

    # Fix rating column type from Float to String
    op.alter_column('external_reviews', 'rating',
               existing_type=sa.Float(),
               type_=sa.String(length=50),
               existing_nullable=True)

    # Fix author column length
    op.alter_column('external_reviews', 'author',
               existing_type=sa.String(length=100),
               type_=sa.String(length=255),
               existing_nullable=True)

    # Fix created_at to be non-nullable
    op.alter_column('external_reviews', 'created_at',
               existing_type=sa.DateTime(),
               nullable=False)


def downgrade() -> None:
    # Reverse the changes
    op.alter_column('external_reviews', 'created_at',
               existing_type=sa.DateTime(),
               nullable=True)

    op.alter_column('external_reviews', 'author',
               existing_type=sa.String(length=255),
               type_=sa.String(length=100),
               existing_nullable=True)

    op.alter_column('external_reviews', 'rating',
               existing_type=sa.String(length=50),
               type_=sa.Float(),
               existing_nullable=True)

    op.drop_column('external_reviews', 'published_at')
