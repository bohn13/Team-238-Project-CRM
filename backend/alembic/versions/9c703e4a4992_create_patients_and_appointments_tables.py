"""create patients and appointments tables

Revision ID: 9c703e4a4992
Revises: 0003_doctors_profiles
Create Date: 2026-07-15 19:26:57.150190

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9c703e4a4992"
down_revision: Union[str, Sequence[str], None] = "0003_doctors_profiles"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "patients",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "gender",
            sa.String(length=20),
            nullable=True,
        ),
        sa.Column(
            "date_of_birth",
            sa.Date(),
            nullable=True,
        ),
        sa.Column(
            "address",
            sa.String(length=255),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "appointments",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "patient_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "doctor_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "date_time",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "duration",
            sa.Integer(),
            server_default="30",
            nullable=False,
        ),
        sa.Column(
            "reason_for_visit",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["doctor_id"],
            ["doctors.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["patient_id"],
            ["patients.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_appointments_doctor_date_time",
        "appointments",
        [
            "doctor_id",
            "date_time",
        ],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "ix_appointments_doctor_date_time",
        table_name="appointments",
    )
    op.drop_table("appointments")
    op.drop_table("patients")
