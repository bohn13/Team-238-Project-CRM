"""create doctors profiles

Revision ID: 0003_doctors_profiles
Revises: 0002_users_schema
Create Date: 2026-07-04 00:00:00.000000

"""

from typing import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0003_doctors_profiles"
down_revision: str | Sequence[str] | None = "0002_users_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.alter_column("users", "is_active", server_default=None)

    op.create_table(
        "doctors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("specialization", sa.String(length=100), nullable=False),
        sa.Column("years_experience", sa.Integer(), nullable=True),
        sa.Column("employment_type", sa.String(length=20), nullable=True),
        sa.Column("avatar_url", sa.String(length=512), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )


def downgrade() -> None:
    op.drop_table("doctors")
    op.drop_column("users", "is_active")
