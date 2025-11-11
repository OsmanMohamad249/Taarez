"""
Login endpoint for user authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import verify_password, create_access_token
from models.user import User
from schemas.user import Token

router = APIRouter()


@router.post("/access-token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login.
    Authenticate user and return JWT access token.
    Accepts any user role (CUSTOMER, DESIGNER, or ADMIN).
    """
    # Find user by email (username field in OAuth2PasswordRequestForm is used for email)
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is not active"
        )

    # Create access token with user email as subject
    access_token = create_access_token(data={"sub": user.email})

    return Token(access_token=access_token, token_type="bearer")
