"""add synced at to venues

Revision ID: ab14f9c3a0d2
Revises: f3a2d9c61b08
Create Date: 2026-06-18 16:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ab14f9c3a0d2"
down_revision: Union[str, Sequence[str], None] = "f3a2d9c61b08"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "venues",
        sa.Column("synced_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("venues", "synced_at")
