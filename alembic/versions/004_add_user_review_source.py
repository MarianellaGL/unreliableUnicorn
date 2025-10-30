"""Add USER source to ReviewSource enum

Revision ID: 004_add_user_review_source
Revises: 003_fix_opinions
Create Date: 2025-10-30

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004_add_user_review_source'
down_revision = '003_fix_opinions'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add 'user' to the reviewsource enum in PostgreSQL
    op.execute("ALTER TYPE reviewsource ADD VALUE IF NOT EXISTS 'user'")


def downgrade() -> None:
    # Note: PostgreSQL doesn't support removing enum values easily
    # You would need to recreate the enum type if you want to remove the value
    pass
