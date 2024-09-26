"""update email unique true

Revision ID: 67d8b60fd0a5
Revises: 1515ec705a26
Create Date: 2024-09-26 15:26:12.105552

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "67d8b60fd0a5"
down_revision: Union[str, None] = "1515ec705a26"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
