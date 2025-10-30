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
    # The source column in external_reviews is stored as String(50), not as an enum
    # So this migration is a no-op - the 'user' value can be inserted directly
    # No schema changes needed since it's just a string field
    pass


def downgrade() -> None:
    # Note: PostgreSQL doesn't support removing enum values easily
    # You would need to recreate the enum type if you want to remove the value
    pass
