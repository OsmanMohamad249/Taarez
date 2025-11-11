"""Add Fabric and Color models and update Design model for Phase 1

Revision ID: a1b2c3d4e5f6
Revises: f8c9d1e2a3b4
Create Date: 2025-11-11 02:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "f8c9d1e2a3b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create fabrics table
    op.create_table(
        "fabrics",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("base_price", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_fabrics_name"), "fabrics", ["name"], unique=True)

    # Create colors table
    op.create_table(
        "colors",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("hex_code", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_colors_name"), "colors", ["name"], unique=True)

    # Create design_fabric association table
    op.create_table(
        "design_fabric",
        sa.Column("design_id", sa.UUID(), nullable=False),
        sa.Column("fabric_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["design_id"],
            ["designs.id"],
        ),
        sa.ForeignKeyConstraint(
            ["fabric_id"],
            ["fabrics.id"],
        ),
        sa.PrimaryKeyConstraint("design_id", "fabric_id"),
    )

    # Create design_color association table
    op.create_table(
        "design_color",
        sa.Column("design_id", sa.UUID(), nullable=False),
        sa.Column("color_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["design_id"],
            ["designs.id"],
        ),
        sa.ForeignKeyConstraint(
            ["color_id"],
            ["colors.id"],
        ),
        sa.PrimaryKeyConstraint("design_id", "color_id"),
    )

    # Update designs table - rename columns and add new fields
    # Rename title to name
    op.alter_column("designs", "title", new_column_name="name")
    
    # Rename price to base_price
    op.alter_column("designs", "price", new_column_name="base_price")
    
    # Rename image_url to base_image_url
    op.alter_column("designs", "image_url", new_column_name="base_image_url")
    
    # Rename designer_id to owner_id
    op.alter_column("designs", "designer_id", new_column_name="owner_id")
    
    # Add customization_rules JSON column
    op.add_column("designs", sa.Column("customization_rules", postgresql.JSON(astext_type=sa.Text()), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove customization_rules from designs
    op.drop_column("designs", "customization_rules")
    
    # Rename columns back
    op.alter_column("designs", "owner_id", new_column_name="designer_id")
    op.alter_column("designs", "base_image_url", new_column_name="image_url")
    op.alter_column("designs", "base_price", new_column_name="price")
    op.alter_column("designs", "name", new_column_name="title")
    
    # Drop association tables
    op.drop_table("design_color")
    op.drop_table("design_fabric")
    
    # Drop colors table
    op.drop_index(op.f("ix_colors_name"), table_name="colors")
    op.drop_table("colors")
    
    # Drop fabrics table
    op.drop_index(op.f("ix_fabrics_name"), table_name="fabrics")
    op.drop_table("fabrics")
