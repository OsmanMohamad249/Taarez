"""
CRUD operations for Fabric model.
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session

from models.fabric import Fabric
from schemas.fabric import FabricCreate, FabricUpdate


def get_fabric(db: Session, fabric_id: UUID) -> Optional[Fabric]:
    """Get a fabric by ID."""
    return db.query(Fabric).filter(Fabric.id == fabric_id).first()


def get_fabric_by_name(db: Session, name: str) -> Optional[Fabric]:
    """Get a fabric by name."""
    return db.query(Fabric).filter(Fabric.name == name).first()


def get_fabrics(db: Session, skip: int = 0, limit: int = 100) -> List[Fabric]:
    """Get all fabrics with pagination."""
    return db.query(Fabric).offset(skip).limit(limit).all()


def create_fabric(db: Session, fabric: FabricCreate) -> Fabric:
    """Create a new fabric."""
    db_fabric = Fabric(**fabric.dict())
    db.add(db_fabric)
    db.commit()
    db.refresh(db_fabric)
    return db_fabric


def update_fabric(
    db: Session, fabric_id: UUID, fabric: FabricUpdate
) -> Optional[Fabric]:
    """Update a fabric."""
    db_fabric = get_fabric(db, fabric_id)
    if db_fabric is None:
        return None

    update_data = fabric.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_fabric, field, value)

    db.commit()
    db.refresh(db_fabric)
    return db_fabric


def delete_fabric(db: Session, fabric_id: UUID) -> bool:
    """Delete a fabric."""
    db_fabric = get_fabric(db, fabric_id)
    if db_fabric is None:
        return False

    db.delete(db_fabric)
    db.commit()
    return True
