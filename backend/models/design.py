"""
Design model.
"""

import uuid

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base

# Association table for Design-Fabric many-to-many relationship
design_fabric_association = Table(
    "design_fabric",
    Base.metadata,
    Column("design_id", UUID(as_uuid=True), ForeignKey("designs.id"), primary_key=True),
    Column("fabric_id", UUID(as_uuid=True), ForeignKey("fabrics.id"), primary_key=True),
)

# Association table for Design-Color many-to-many relationship
design_color_association = Table(
    "design_color",
    Base.metadata,
    Column("design_id", UUID(as_uuid=True), ForeignKey("designs.id"), primary_key=True),
    Column("color_id", UUID(as_uuid=True), ForeignKey("colors.id"), primary_key=True),
)


class Design(Base):
    """Design model for marketplace designs."""

    __tablename__ = "designs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    base_image_url = Column(String, nullable=True)
    base_price = Column(Float, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    customization_rules = Column(JSON, nullable=True, default=dict)

    # Legacy fields for backward compatibility
    style_type = Column(String, nullable=True, index=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Many-to-many relationships
    available_fabrics = relationship(
        "Fabric", secondary=design_fabric_association, backref="designs"
    )
    available_colors = relationship(
        "Color", secondary=design_color_association, backref="designs"
    )

    def __repr__(self):
        return f"<Design(id={self.id}, name={self.name})>"
