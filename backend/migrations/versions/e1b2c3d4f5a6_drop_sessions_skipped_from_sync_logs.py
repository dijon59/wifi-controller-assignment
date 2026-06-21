"""drop sessions skipped from sync logs

Revision ID: e1b2c3d4f5a6
Revises: c85d12d43ef5
Create Date: 2026-06-21 13:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e1b2c3d4f5a6"
down_revision: Union[str, Sequence[str], None] = "c85d12d43ef5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("sync_logs", "sessions_skipped")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "sync_logs",
        sa.Column("sessions_skipped", sa.Integer(), nullable=False, server_default="0"),
    )
    op.alter_column("sync_logs", "sessions_skipped", server_default=None)
