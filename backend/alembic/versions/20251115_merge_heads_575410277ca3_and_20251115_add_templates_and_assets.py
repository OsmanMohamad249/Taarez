"""Merge head revisions 575410277ca3 and 20251115_add_templates_and_assets

Revision ID: 20251115_merge_575410277ca3_and_20251115_add_templates_and_assets
Revises: 575410277ca3, 20251115_add_templates_and_assets
Create Date: 2025-11-15 17:40:00.000000

This is a merge migration whose purpose is to unify two previously
divergent Alembic heads so CI and test-time `alembic upgrade head`
can run successfully.
"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "20251115_merge_575410277ca3_and_20251115_add_templates_and_assets"
down_revision = ("575410277ca3", "20251115_add_templates_and_assets")
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Merge migration: no schema changes required.

    This migration intentionally does not alter the database schema.
    It only records a merge of two revision heads so that `alembic`
    considers the migration graph linear for `upgrade head`.
    """
    pass


def downgrade() -> None:
    # Downgrade from a merge is non-trivial and not implemented.
    # If you need to revert this merge, handle the branches manually.
    pass
