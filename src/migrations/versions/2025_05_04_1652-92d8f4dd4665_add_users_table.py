"""add users table

Revision ID: 92d8f4dd4665
Revises: 2c1bf0cf5a7e
Create Date: 2025-05-04 16:52:15.122837

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "92d8f4dd4665"
down_revision: Union[str, None] = "2c1bf0cf5a7e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("hash_password", sa.String(length=100), nullable=False),
        sa.Column("nickname", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
