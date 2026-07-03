"""align users with project schema

Revision ID: 0002_users_schema
Revises: 0001_create_users_auth_tables
Create Date: 2026-07-03 00:00:00.000000

"""

from typing import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0002_users_schema"
down_revision: str | Sequence[str] | None = "0001_create_users_auth_tables"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("role", sa.String(length=20), nullable=True))
    op.add_column("users", sa.Column("first_name", sa.String(length=50), nullable=True))
    op.add_column("users", sa.Column("last_name", sa.String(length=50), nullable=True))
    op.add_column("users", sa.Column("phone_number", sa.String(length=20), nullable=True))
    op.add_column("users", sa.Column("source", sa.String(length=30), nullable=True))

    op.execute(
        sa.text(
            """
            UPDATE users
            SET role = LOWER(user_groups.name::text)
            FROM user_groups
            WHERE users.group_id = user_groups.id
            """
        )
    )
    op.execute(sa.text("UPDATE users SET role = 'doctor' WHERE role IS NULL"))
    op.execute(sa.text("UPDATE users SET first_name = '' WHERE first_name IS NULL"))
    op.execute(sa.text("UPDATE users SET last_name = '' WHERE last_name IS NULL"))

    op.alter_column("users", "role", nullable=False)
    op.alter_column("users", "first_name", nullable=False)
    op.alter_column("users", "last_name", nullable=False)

    op.alter_column(
        "users",
        "hashed_password",
        new_column_name="password_hash",
        existing_type=sa.String(length=255),
        nullable=True,
    )
    op.alter_column(
        "users",
        "email",
        existing_type=sa.String(),
        type_=sa.String(length=50),
        nullable=True,
    )
    op.alter_column(
        "users",
        "created_at",
        new_column_name="registration_date",
        existing_type=sa.DateTime(timezone=True),
        existing_server_default=sa.text("now()"),
    )

    op.create_unique_constraint("uq_users_phone_number", "users", ["phone_number"])
    op.drop_constraint("users_group_id_fkey", "users", type_="foreignkey")
    op.drop_column("users", "group_id")
    op.drop_column("users", "is_active")
    op.drop_column("users", "updated_at")
    op.drop_table("user_groups")
    sa.Enum(name="usergroupenum").drop(op.get_bind(), checkfirst=True)


def downgrade() -> None:
    user_group_enum = sa.Enum(
        "SUPERADMIN", "ADMIN", "DOCTOR", "PATIENT", name="usergroupenum"
    )
    user_group_enum.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "user_groups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", user_group_enum, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.execute(
        sa.text(
            """
            INSERT INTO user_groups (name)
            VALUES
                ('SUPERADMIN'::usergroupenum),
                ('ADMIN'::usergroupenum),
                ('DOCTOR'::usergroupenum),
                ('PATIENT'::usergroupenum)
            ON CONFLICT (name) DO NOTHING
            """
        )
    )

    op.add_column("users", sa.Column("updated_at", sa.DateTime(timezone=True)))
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=True))
    op.add_column("users", sa.Column("group_id", sa.Integer(), nullable=True))
    op.execute(sa.text("UPDATE users SET is_active = TRUE WHERE is_active IS NULL"))
    op.execute(
        sa.text(
            """
            UPDATE users
            SET group_id = user_groups.id
            FROM user_groups
            WHERE UPPER(users.role) = user_groups.name::text
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE users
            SET group_id = (SELECT id FROM user_groups WHERE name = 'DOCTOR')
            WHERE group_id IS NULL
            """
        )
    )
    op.alter_column("users", "is_active", nullable=False)
    op.alter_column("users", "group_id", nullable=False)
    op.create_foreign_key(
        "users_group_id_fkey", "users", "user_groups", ["group_id"], ["id"]
    )

    op.drop_constraint("uq_users_phone_number", "users", type_="unique")
    op.drop_column("users", "source")
    op.drop_column("users", "phone_number")
    op.drop_column("users", "last_name")
    op.drop_column("users", "first_name")
    op.drop_column("users", "role")
    op.execute(sa.text("UPDATE users SET email = '' WHERE email IS NULL"))
    op.execute(sa.text("UPDATE users SET password_hash = '' WHERE password_hash IS NULL"))
    op.alter_column("users", "email", existing_type=sa.String(length=50), nullable=False)
    op.alter_column(
        "users",
        "password_hash",
        new_column_name="hashed_password",
        existing_type=sa.String(length=255),
        nullable=False,
    )
    op.alter_column(
        "users",
        "registration_date",
        new_column_name="created_at",
        existing_type=sa.DateTime(timezone=True),
        existing_server_default=sa.text("now()"),
    )
