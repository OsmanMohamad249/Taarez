"""Add categories and designs tables

Revision ID: f8c9d1e2a3b4
Revises: adf611fe0bc0
Create Date: 2025-11-09 22:15:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f8c9d1e2a3b4"
down_revision: Union[str, Sequence[str], None] = "adf611fe0bc0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create categories table
    op.create_table(
        "categories",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_categories_name"), "categories", ["name"], unique=True)

    # Create designs table
    op.create_table(
        "designs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("style_type", sa.String(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("designer_id", sa.UUID(), nullable=False),
        sa.Column("category_id", sa.UUID(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["designer_id"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_designs_title"), "designs", ["title"], unique=False)
    op.create_index(op.f("ix_designs_style_type"), "designs", ["style_type"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_designs_style_type"), table_name="designs")
    op.drop_index(op.f("ix_designs_title"), table_name="designs")
    op.drop_table("designs")
    op.drop_index(op.f("ix_categories_name"), table_name="categories")
    op.drop_table("categories")
