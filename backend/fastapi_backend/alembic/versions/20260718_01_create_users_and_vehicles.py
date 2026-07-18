"""Create users and vehicles tables.

Revision ID: 20260718_01
Revises:
Create Date: 2026-07-18
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "20260718_01"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)
    op.create_table(
        "vehicles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("make", sa.String(length=100), nullable=False),
        sa.Column("model", sa.String(length=100), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("price", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_vehicles_category"), "vehicles", ["category"], unique=False
    )
    op.create_index(op.f("ix_vehicles_make"), "vehicles", ["make"], unique=False)
    op.create_index(op.f("ix_vehicles_model"), "vehicles", ["model"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_vehicles_model"), table_name="vehicles")
    op.drop_index(op.f("ix_vehicles_make"), table_name="vehicles")
    op.drop_index(op.f("ix_vehicles_category"), table_name="vehicles")
    op.drop_table("vehicles")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
