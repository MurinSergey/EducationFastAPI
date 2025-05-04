"""user unique email column

Revision ID: 707a24c95cc5
Revises: 92d8f4dd4665
Create Date: 2025-05-04 18:52:24.729139

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "707a24c95cc5"
down_revision: Union[str, None] = "92d8f4dd4665"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
