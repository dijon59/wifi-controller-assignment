"""create wifi controller tables real

Revision ID: d7b6d7b0f2a1
Revises: bc09d3b94d58
Create Date: 2026-06-16 18:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d7b6d7b0f2a1"
down_revision: Union[str, Sequence[str], None] = "bc09d3b94d58"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "venues",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ctr_venue_id", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("timezone", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_venues_ctr_venue_id"),
        "venues",
        ["ctr_venue_id"],
        unique=True,
    )

    op.create_table(
        "access_points",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("venue_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("ctr_access_point_id", sa.String(length=100), nullable=False),
        sa.Column("mac_address", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["venue_id"], ["venues.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_access_points_ctr_access_point_id"),
        "access_points",
        ["ctr_access_point_id"],
        unique=True,
    )

    op.create_table(
        "wifi_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ctr_session_id", sa.String(length=100), nullable=False),
        sa.Column("access_point_id", sa.Integer(), nullable=False),
        sa.Column("client_mac", sa.String(length=255), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("bytes_received", sa.BigInteger(), nullable=False),
        sa.Column("bytes_sent", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["access_point_id"], ["access_points.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_wifi_sessions_access_point_id"),
        "wifi_sessions",
        ["access_point_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_wifi_sessions_ctr_session_id"),
        "wifi_sessions",
        ["ctr_session_id"],
        unique=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_wifi_sessions_ctr_session_id"), table_name="wifi_sessions")
    op.drop_index(op.f("ix_wifi_sessions_access_point_id"), table_name="wifi_sessions")
    op.drop_table("wifi_sessions")
    op.drop_index(
        op.f("ix_access_points_ctr_access_point_id"),
        table_name="access_points",
    )
    op.drop_table("access_points")
    op.drop_index(op.f("ix_venues_ctr_venue_id"), table_name="venues")
    op.drop_table("venues")
