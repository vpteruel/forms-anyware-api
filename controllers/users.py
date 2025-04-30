from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from core.database import get_db
from core.security import get_current_user, get_current_admin_user, get_current_user_optional, get_user_from_request
from models.user import User, UserCreate, UserUpdate
from services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"},
    },
)

@router.get("/", dependencies=[Depends(get_current_admin_user)], response_model=List[User])
def get_users(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all users
    """
    users = UserService.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", dependencies=[Depends(get_current_user)], response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user by ID
    """
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Create user (admin only)
    """
    # Check if email already exists
    existing_user = UserService.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    from core.security import get_password_hash
    user_dict = user.model_dump()
    user_dict["password"] = get_password_hash(user.password)
    
    return UserService.create_user(db, UserCreate(**user_dict))

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int, 
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Update user (admin only)
    """
    # Hash the password if it's being updated
    if user.password:
        from core.security import get_password_hash
        user_dict = user.model_dump()
        user_dict["password"] = get_password_hash(user.password)
        user = UserUpdate(**user_dict)
    
    updated_user = UserService.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """
    Delete user (admin only)
    """
    success = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None

@router.get("/me", response_model=User)
def get_my_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user profile 
    """
    # Extract user ID from token
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/admins", dependencies=[Depends(get_current_admin_user)])
def get_admin_users() -> dict[str, str]:
    """
    Get all admin users (requires admin role)
    """
    return {"message": "Get all admin users"}

@router.get("/public-with-user-info")
def public_with_user_info(current_user: dict = Depends(get_current_user_optional)) -> dict:
    """
    Public endpoint that shows different content for logged-in users
    """
    if current_user:
        return {"message": f"Hello, {current_user.get('username', 'User')}!"}
    return {"message": "Hello, Guest!"}

@router.get("/from-middleware")
def from_middleware(request: Request) -> dict:
    """
    Access user from middleware (if using the middleware approach)
    """
    user = get_user_from_request(request)
    if user:
        return {"message": f"Hello, {user.get('username', 'User')}!"}
    return {"message": "Hello, Guest!"}