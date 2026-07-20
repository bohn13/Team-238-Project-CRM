"""normalize doctor employment type values

Revision ID: 0004_doctor_employment_type
Revises: 0003_doctors_profiles
Create Date: 2026-07-11 00:00:00.000000

"""

from typing import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0004_doctor_employment_type"
down_revision: str | Sequence[str] | None = "0003_doctors_profiles"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            UPDATE doctors
            SET employment_type = CASE employment_type
                WHEN 'full_time' THEN 'full-time'
                WHEN 'part_time' THEN 'part-time'
                ELSE employment_type
            END
            WHERE employment_type IN ('full_time', 'part_time')
            """
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            UPDATE doctors
            SET employment_type = CASE employment_type
                WHEN 'full-time' THEN 'full_time'
                WHEN 'part-time' THEN 'part_time'
                ELSE employment_type
            END
            WHERE employment_type IN ('full-time', 'part-time')
            """
        )
    )
