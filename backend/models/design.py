"""
Design model.
"""

import uuid

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from core.database import Base


class Design(Base):
    """Design model for marketplace designs."""

    __tablename__ = "designs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    style_type = Column(String, nullable=True, index=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    designer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self):
        return f"<Design(id={self.id}, title={self.title})>"
