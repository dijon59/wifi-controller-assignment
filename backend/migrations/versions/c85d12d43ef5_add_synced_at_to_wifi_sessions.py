"""add synced at to wifi sessions

Revision ID: c85d12d43ef5
Revises: ab14f9c3a0d2
Create Date: 2026-06-18 16:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c85d12d43ef5"
down_revision: Union[str, Sequence[str], None] = "ab14f9c3a0d2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "wifi_sessions",
        sa.Column("synced_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("wifi_sessions", "synced_at")
