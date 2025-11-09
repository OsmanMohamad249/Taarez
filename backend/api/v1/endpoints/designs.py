"""
Design endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from core.database import get_db
from core.deps import get_current_user, get_current_designer_user
from models.design import Design
from models.category import Category
from models.user import User
from schemas.design import DesignCreate, DesignUpdate, DesignResponse

router = APIRouter()


@router.get("/", response_model=List[DesignResponse])
def list_designs(
    skip: int = 0,
    limit: int = 100,
    style_type: Optional[str] = Query(None, description="Filter by style type"),
    category_id: Optional[str] = Query(None, description="Filter by category ID"),
    active_only: bool = True,
    db: Session = Depends(get_db),
):
    """
    List all designs with optional filtering.
    
    - **skip**: Number of designs to skip (for pagination)
    - **limit**: Maximum number of designs to return
    - **style_type**: Filter designs by style type
    - **category_id**: Filter designs by category ID
    - **active_only**: If True, only return active designs
    """
    query = db.query(Design)
    
    if active_only:
        query = query.filter(Design.is_active == True)
    
    if style_type:
        query = query.filter(Design.style_type == style_type)
    
    if category_id:
        query = query.filter(Design.category_id == category_id)
    
    designs = query.order_by(Design.created_at.desc()).offset(skip).limit(limit).all()
    return designs


@router.get("/{design_id}", response_model=DesignResponse)
def get_design(design_id: str, db: Session = Depends(get_db)):
    """
    Get a specific design by ID.
    """
    design = db.query(Design).filter(Design.id == design_id).first()
    
    if not design:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found",
        )
    
    return design


@router.post("/", response_model=DesignResponse, status_code=status.HTTP_201_CREATED)
def create_design(
    design_data: DesignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_designer_user),
):
    """
    Create a new design (designers only).
    
    Requires designer role.
    """
    # Verify category exists if provided
    if design_data.category_id:
        category = (
            db.query(Category)
            .filter(Category.id == design_data.category_id)
            .first()
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category not found",
            )
    
    # Create new design
    new_design = Design(
        title=design_data.title,
        description=design_data.description,
        style_type=design_data.style_type,
        price=design_data.price,
        image_url=design_data.image_url,
        category_id=design_data.category_id,
        designer_id=current_user.id,
    )
    
    db.add(new_design)
    db.commit()
    db.refresh(new_design)
    
    return new_design


@router.put("/{design_id}", response_model=DesignResponse)
def update_design(
    design_id: str,
    design_data: DesignUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_designer_user),
):
    """
    Update a design (designers can only update their own designs).
    
    Requires designer role and ownership of the design.
    """
    design = db.query(Design).filter(Design.id == design_id).first()
    
    if not design:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found",
        )
    
    # Check if user owns this design (unless superuser)
    if design.designer_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own designs",
        )
    
    # Update fields if provided
    update_data = design_data.dict(exclude_unset=True)
    
    # Verify category exists if being updated
    if "category_id" in update_data and update_data["category_id"]:
        category = (
            db.query(Category)
            .filter(Category.id == update_data["category_id"])
            .first()
        )
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category not found",
            )
    
    for field, value in update_data.items():
        setattr(design, field, value)
    
    db.commit()
    db.refresh(design)
    
    return design


@router.delete("/{design_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_design(
    design_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_designer_user),
):
    """
    Delete a design (designers can only delete their own designs).
    
    Requires designer role and ownership of the design.
    """
    design = db.query(Design).filter(Design.id == design_id).first()
    
    if not design:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found",
        )
    
    # Check if user owns this design (unless superuser)
    if design.designer_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own designs",
        )
    
    db.delete(design)
    db.commit()
    
    return None
