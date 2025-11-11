"""
Fabric model.
"""

import uuid

from sqlalchemy import Column, Float, String
from sqlalchemy.dialects.postgresql import UUID

from core.database import Base


class Fabric(Base):
    """Fabric model for design customization options."""

    __tablename__ = "fabrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    base_price = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Fabric(id={self.id}, name={self.name})>"
