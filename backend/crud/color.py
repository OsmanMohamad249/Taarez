"""
CRUD operations for Color model.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from models.color import Color
from schemas.color import ColorCreate, ColorUpdate


def get_color(db: Session, color_id: UUID) -> Optional[Color]:
    """Get a color by ID."""
    return db.query(Color).filter(Color.id == color_id).first()


def get_color_by_name(db: Session, name: str) -> Optional[Color]:
    """Get a color by name."""
    return db.query(Color).filter(Color.name == name).first()


def get_colors(db: Session, skip: int = 0, limit: int = 100) -> List[Color]:
    """Get all colors with pagination."""
    return db.query(Color).offset(skip).limit(limit).all()


def create_color(db: Session, color: ColorCreate) -> Color:
    """Create a new color."""
    db_color = Color(**color.dict())
    db.add(db_color)
    db.commit()
    db.refresh(db_color)
    return db_color


def update_color(db: Session, color_id: UUID, color: ColorUpdate) -> Optional[Color]:
    """Update a color."""
    db_color = get_color(db, color_id)
    if db_color is None:
        return None

    update_data = color.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_color, field, value)

    db.commit()
    db.refresh(db_color)
    return db_color


def delete_color(db: Session, color_id: UUID) -> bool:
    """Delete a color."""
    db_color = get_color(db, color_id)
    if db_color is None:
        return False

    db.delete(db_color)
    db.commit()
    return True
