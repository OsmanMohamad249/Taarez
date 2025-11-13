from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from models.roles import UserRole
from core.database import get_db
from core.security import hash_password, verify_password, create_access_token
from models.user import User
from schemas.user import UserRegisterWithRole, Token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_admin_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    from core.security import verify_access_token
    payload = verify_access_token(token)
    email = payload.get("sub")
    role = payload.get("role")
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_superuser or role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required.")
    return user
# Admin-only endpoint to create designer/admin users
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
"""
Authentication endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import hash_password, verify_password, create_access_token
from models.user import User
from schemas.user import UserRegisterWithRole, Token

router = APIRouter()


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def register(user_data: UserRegisterWithRole, db: Session = Depends(get_db)):
    """
    Register a new user with role specification (for admin use).
    """
    # Only allow customer role for public registration
    if str(user_data.role).lower() != "customer":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only customer role is allowed for public registration."
        )

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create new user
    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pwd,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        role=user_data.role,
        is_superuser=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "email": new_user.email}


@router.post("/login", response_model=Token, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Login with email and password. Returns access token.
    Note: username field in OAuth2PasswordRequestForm is used for email.
    """
    # Find user by email (using username field from OAuth2 form)
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

    # Create access token with user role for frontend use
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value}
    )

    return Token(access_token=access_token, token_type="bearer")
