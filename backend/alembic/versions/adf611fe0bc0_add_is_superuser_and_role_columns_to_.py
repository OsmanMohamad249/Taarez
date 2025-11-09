"""Add is_superuser and role columns to user model

Revision ID: adf611fe0bc0
Revises: 7dcaee9ea011
Create Date: 2025-11-09 17:24:17.987815

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "adf611fe0bc0"
down_revision: Union[str, Sequence[str], None] = "7dcaee9ea011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add is_superuser column
    op.add_column(
        "users",
        sa.Column(
            "is_superuser", sa.Boolean(), nullable=False, server_default="false"
        ),
    )

    # Add role column with enum type
    op.execute("CREATE TYPE userrole AS ENUM ('admin', 'customer', 'designer', 'tailor')")
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.Enum("admin", "customer", "designer", "tailor", name="userrole"),
            nullable=False,
            server_default="customer",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop role column
    op.drop_column("users", "role")
    op.execute("DROP TYPE userrole")

    # Drop is_superuser column
    op.drop_column("users", "is_superuser")
