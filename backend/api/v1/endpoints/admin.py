from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserUpdate, UserOut, UserRegisterWithRole
from core.database import get_db
from api.v1.endpoints.auth import get_current_admin_user
from models.roles import UserRole
from core.security import hash_password

router = APIRouter()

@router.post("/admin-create-user", response_model=dict, status_code=status.HTTP_201_CREATED)
def admin_create_user(user_data: UserRegisterWithRole, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin_user)):
    # Only allow designer or admin roles
    if str(user_data.role).lower() not in ["designer", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only designer or admin roles allowed via this endpoint."
        )
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pwd,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        is_superuser=(user_data.role == UserRole.ADMIN),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"{user_data.role.value.capitalize()} user created successfully", "email": new_user.email}

@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin_user)):
    return db.query(User).all()

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: str, db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}
