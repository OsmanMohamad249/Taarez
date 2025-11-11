"""
CRUD operations for Design model.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from models.design import Design
from models.fabric import Fabric
from models.color import Color
from schemas.design import DesignCreate, DesignUpdate


def get_design(db: Session, design_id: UUID) -> Optional[Design]:
    """Get a design by ID."""
    return db.query(Design).filter(Design.id == design_id).first()


def get_designs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    owner_id: Optional[UUID] = None,
    active_only: bool = False,
) -> List[Design]:
    """Get all designs with optional filtering by owner_id."""
    query = db.query(Design)

    if owner_id:
        query = query.filter(Design.owner_id == owner_id)

    if active_only:
        query = query.filter(Design.is_active == True)

    return query.order_by(Design.created_at.desc()).offset(skip).limit(limit).all()


def create_design(db: Session, design: DesignCreate, owner_id: UUID) -> Design:
    """Create a new design."""
    # Extract fabric and color IDs
    fabric_ids = design.available_fabric_ids or []
    color_ids = design.available_color_ids or []

    # Create design without relationships
    design_data = design.dict(exclude={"available_fabric_ids", "available_color_ids"})
    db_design = Design(**design_data, owner_id=owner_id)

    # Add fabrics if provided
    if fabric_ids:
        fabrics = db.query(Fabric).filter(Fabric.id.in_(fabric_ids)).all()
        db_design.available_fabrics = fabrics

    # Add colors if provided
    if color_ids:
        colors = db.query(Color).filter(Color.id.in_(color_ids)).all()
        db_design.available_colors = colors

    db.add(db_design)
    db.commit()
    db.refresh(db_design)
    return db_design


def update_design(
    db: Session, design_id: UUID, design: DesignUpdate
) -> Optional[Design]:
    """Update a design."""
    db_design = get_design(db, design_id)
    if db_design is None:
        return None

    update_data = design.dict(
        exclude_unset=True, exclude={"available_fabric_ids", "available_color_ids"}
    )

    # Update fabric relationships if provided
    if design.available_fabric_ids is not None:
        fabrics = (
            db.query(Fabric).filter(Fabric.id.in_(design.available_fabric_ids)).all()
        )
        db_design.available_fabrics = fabrics

    # Update color relationships if provided
    if design.available_color_ids is not None:
        colors = db.query(Color).filter(Color.id.in_(design.available_color_ids)).all()
        db_design.available_colors = colors

    # Update other fields
    for field, value in update_data.items():
        setattr(db_design, field, value)

    db.commit()
    db.refresh(db_design)
    return db_design


def delete_design(db: Session, design_id: UUID) -> bool:
    """Delete a design."""
    db_design = get_design(db, design_id)
    if db_design is None:
        return False

    db.delete(db_design)
    db.commit()
    return True
