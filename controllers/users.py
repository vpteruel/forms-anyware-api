from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import get_current_user
from models.user import User

# OAuth2 scheme that will get the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"},
    },
)

@router.get("/")
def get_users() -> dict[str, str]:
    """
    Get all users
    - **return**: list of users
    - **status**: 200 OK
    """
    return {"message": "Get all users"}

@router.get("/{user_id}")
def get_user(user_id: int) -> dict[str, str]:
    """
    Get user by ID
    - **user_id**: int
    - **return**: user
    - **status**: 200 OK
    """
    return {"message": f"Get user {user_id}"}

@router.post("/")
def create_user() -> dict[str, str]:
    """
    Create user
    - **return**: user
    - **status**: 201 Created
    """
    return {"message": "Create user"}

@router.put("/{user_id}")
def update_user(user_id: int) -> dict[str, str]:
    """
    Update user by ID
    - **user_id**: int
    - **return**: user
    - **status**: 200 OK
    """
    return {"message": f"Update user {user_id}"}

@router.delete("/{user_id}")
def delete_user(user_id: int) -> dict[str, str]:
    """
    Delete user by ID
    - **user_id**: int
    - **return**: user
    - **status**: 200 OK
    """
    return {"message": f"Delete user {user_id}"}