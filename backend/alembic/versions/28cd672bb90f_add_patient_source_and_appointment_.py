"""add patient source and appointment channel

Revision ID: 28cd672bb90f
Revises: 9c703e4a4992
Create Date: 2026-07-17 19:17:11.433343

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "28cd672bb90f"
down_revision: Union[str, Sequence[str], None] = "9c703e4a4992"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "appointments",
        sa.Column(
            "channel",
            sa.String(length=30),
            nullable=True,
        ),
    )

    op.add_column(
        "patients",
        sa.Column(
            "source",
            sa.String(length=30),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "patients",
        "source",
    )

    op.drop_column(
        "appointments",
        "channel",
    )
