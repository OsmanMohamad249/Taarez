"""
Category endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.deps import get_current_admin_user
from models.category import Category
from models.user import User
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
def list_categories(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db),
):
    """
    List all categories.
    
    - **skip**: Number of categories to skip (for pagination)
    - **limit**: Maximum number of categories to return
    - **active_only**: If True, only return active categories
    """
    query = db.query(Category)
    
    if active_only:
        query = query.filter(Category.is_active == True)
    
    categories = query.offset(skip).limit(limit).all()
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: str, db: Session = Depends(get_db)):
    """
    Get a specific category by ID.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    
    return category


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Create a new category (admin only).
    
    Requires admin privileges.
    """
    # Check if category with same name already exists
    existing_category = (
        db.query(Category).filter(Category.name == category_data.name).first()
    )
    
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists",
        )
    
    # Create new category
    new_category = Category(
        name=category_data.name,
        description=category_data.description,
        image_url=category_data.image_url,
        is_active=category_data.is_active,
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: str,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Update a category (admin only).
    
    Requires admin privileges.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    
    # Update fields if provided
    update_data = category_data.dict(exclude_unset=True)
    
    # Check for name uniqueness if name is being updated
    if "name" in update_data and update_data["name"] != category.name:
        existing_category = (
            db.query(Category).filter(Category.name == update_data["name"]).first()
        )
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists",
            )
    
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Delete a category (admin only).
    
    Requires admin privileges.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    
    db.delete(category)
    db.commit()
    
    return None
