"""add cod to paymentmethod enum

Revision ID: 579afdbb0cc2
Revises: bbee470b4873
Create Date: 2026-07-12 16:22:46.913693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '579afdbb0cc2'
down_revision: Union[str, Sequence[str], None] = 'f08a8e655ad6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.execute(
        "ALTER TYPE paymentmethod "
        "ADD VALUE IF NOT EXISTS 'COD'"
    )


def downgrade() -> None:
    pass