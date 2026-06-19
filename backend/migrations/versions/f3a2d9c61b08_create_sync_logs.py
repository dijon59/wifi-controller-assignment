"""create sync logs

Revision ID: f3a2d9c61b08
Revises: d7b6d7b0f2a1
Create Date: 2026-06-18 13:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f3a2d9c61b08"
down_revision: Union[str, Sequence[str], None] = "d7b6d7b0f2a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "sync_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("venues_synced", sa.Integer(), nullable=False),
        sa.Column("access_points_synced", sa.Integer(), nullable=False),
        sa.Column("sessions_synced", sa.Integer(), nullable=False),
        sa.Column("sessions_skipped", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("sync_logs")
