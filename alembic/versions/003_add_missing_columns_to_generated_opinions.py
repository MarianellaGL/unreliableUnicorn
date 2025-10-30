"""Add missing columns to generated_opinions

Revision ID: 003_fix_opinions
Revises: 002_add_published_at
Create Date: 2025-10-29 21:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003_fix_opinions'
down_revision: Union[str, None] = '002_add_published_at'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add absurdity_score column to generated_opinions
    op.add_column('generated_opinions',
                  sa.Column('absurdity_score', sa.Float(), nullable=False, server_default='0.0'))

    # Add generation_method column to generated_opinions
    op.add_column('generated_opinions',
                  sa.Column('generation_method', sa.String(length=100), nullable=True))

    # Remove the old 'tone' column if it exists (from the wrong migration)
    try:
        op.drop_column('generated_opinions', 'tone')
    except:
        pass  # Column might not exist


def downgrade() -> None:
    # Reverse the changes
    op.drop_column('generated_opinions', 'generation_method')
    op.drop_column('generated_opinions', 'absurdity_score')
