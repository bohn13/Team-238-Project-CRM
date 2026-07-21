"""merge doctor and patient migration heads

Revision ID: b7f2c8a1d9e0
Revises: 0004_doctor_employment_type, 28cd672bb90f
Create Date: 2026-07-20 00:00:00.000000

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "b7f2c8a1d9e0"
down_revision: Union[str, Sequence[str], None] = (
    "0004_doctor_employment_type",
    "28cd672bb90f",
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Merge migration branches."""


def downgrade() -> None:
    """Split migration branches."""
