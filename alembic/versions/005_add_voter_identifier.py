"""Add voter_identifier column to opinion_votes

Revision ID: 005_add_voter_identifier
Revises: 004_add_user_review_source
Create Date: 2025-10-30

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005_add_voter_identifier'
down_revision = '004_add_user_review_source'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add voter_identifier column to opinion_votes table
    op.add_column('opinion_votes',
        sa.Column('voter_identifier', sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    # Remove voter_identifier column
    op.drop_column('opinion_votes', 'voter_identifier')
