"""
Color model.
"""

import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from core.database import Base


class Color(Base):
    """Color model for design customization options."""

    __tablename__ = "colors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True, index=True)
    hex_code = Column(String, nullable=False)

    def __repr__(self):
        return f"<Color(id={self.id}, name={self.name})>"
