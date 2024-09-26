"""add username and name for users

Revision ID: 1515ec705a26
Revises: 1af28269de2e
Create Date: 2024-09-26 14:53:54.163034

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1515ec705a26"
down_revision: Union[str, None] = "1af28269de2e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("username", sa.String(length=200), nullable=False))
    op.add_column("users", sa.Column("name", sa.String(length=200), nullable=False))


def downgrade() -> None:
    op.drop_column("users", "name")
    op.drop_column("users", "username")
