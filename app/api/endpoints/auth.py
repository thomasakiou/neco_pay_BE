from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.infrastructure.user_repository import UserRepository
from app.application.auth.dtos import LoginRequest, LoginResponse
from app.application.auth.utils import verify_password, create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint - authenticates user and returns JWT token
    """
    user_repo = UserRepository(db)
    user = user_repo.get_by_username(request.username)
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        username=user.username,
        role=user.role
    )
