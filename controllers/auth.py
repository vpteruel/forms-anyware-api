from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from core.security import (
    authenticate_user,
    create_access_token,
    create_id_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={401: {"description": "Unauthorized"}},
)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint
    - **username**: email address
    - **password**: str
    - **return**: ID token and Access token
    - **status**: 200 OK
    """

    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert the user object to a dict for token creation
    user_dict = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": user.full_name,
        "username": user.username
    }

    # Set expiration times
    id_token_expires = timedelta(days=7)  # ID tokens can live longer
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Create ID token - contains user identity information
    id_token = create_id_token(
        user_data=user_dict,
        expires_delta=id_token_expires
    )
    
    # Create Access token - contains authorization information
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    # Return both tokens and user profile for convenience
    return {
        "id_token": id_token,
        "access_token": access_token, 
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Seconds
    }