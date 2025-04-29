from fastapi import APIRouter, Depends, HTTPException, status, Request
from core.security import get_current_user, get_current_admin_user, get_current_user_optional, get_user_from_request
from models.user import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        404: {"description": "Not found"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"},
    },
)

@router.get("/", dependencies=[Depends(get_current_user)])
def get_users() -> dict[str, str]:
    """
    Get all users
    - **return**: list of users
    - **status**: 200 OK
    """
    return {"message": "Get all users"}

@router.get("/{user_id}", dependencies=[Depends(get_current_user)])
def get_user(user_id: int) -> dict[str, str]:
    """
    Get user by ID
    - **user_id**: int
    - **return**: user
    - **status**: 200 OK
    """
    return {"message": f"Get user {user_id}"}

@router.post("/", dependencies=[Depends(get_current_user)])
def create_user() -> dict[str, str]:
    """
    Create user
    - **return**: user
    - **status**: 201 Created
    """
    return {"message": "Create user"}

@router.put("/{user_id}", dependencies=[Depends(get_current_user)])
def update_user(user_id: int) -> dict[str, str]:
    """
    Update user by ID
    - **user_id**: int
    - **return**: user
    - **status**: 200 OK
    """
    return {"message": f"Update user {user_id}"}

@router.delete("/{user_id}", dependencies=[Depends(get_current_user)])
def delete_user(user_id: int) -> dict[str, str]:
    """
    Delete user by ID
    - **user_id**: int
    - **return**: user
    - **status**: 200 OK
    """
    return {"message": f"Delete user {user_id}"}

@router.get("/admins", dependencies=[Depends(get_current_admin_user)])
def get_admin_users() -> dict[str, str]:
    """
    Get all admin users (requires admin role)
    """
    return {"message": "Get all admin users"}

@router.get("/me")
def get_my_profile(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Get current user profile 
    """
    return {"message": "User profile", "user": current_user}

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