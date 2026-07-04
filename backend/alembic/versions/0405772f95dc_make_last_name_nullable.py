"""make last_name nullable

Revision ID: 0405772f95dc
Revises: d428ca4db1fe
Create Date: 2026-07-04 16:14:14.126146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0405772f95dc'
down_revision: Union[str, Sequence[str], None] = 'd428ca4db1fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        "customers",
        "last_name",
        existing_type=sa.VARCHAR(length=100),
        nullable=True,
        schema="store",
    )


def downgrade():
    op.alter_column(
        "customers",
        "last_name",
        existing_type=sa.VARCHAR(length=100),
        nullable=False,
        schema="store",
    )
    # ### end Alembic commands ###
