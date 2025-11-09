"""
Measurement model.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from core.database import Base


class Measurement(Base):
    """Measurement model for storing AI-processed body measurements."""

    __tablename__ = "measurements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    measurements = Column(JSON, nullable=False)
    image_paths = Column(JSON, nullable=False)
    processed_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    confidence_score = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Measurement(id={self.id}, user_id={self.user_id})>"
