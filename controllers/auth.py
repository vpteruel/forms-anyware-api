from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from jose import JWTError, jwt

from core.config import settings
from core.security import (
    authenticate_user,
    create_access_token,
    create_id_token,
    get_current_admin_user,
    oauth2_scheme
)

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={
        401: {"description": "Unauthorized"}
    },
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

    # Set expiration times
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    id_token_expires = timedelta(days=7)  # ID tokens can live longer

    # Convert the user object to a dict for token creation
    user_data = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "is_sys_admin": user.is_sys_admin,
    }

    # Include permissions in access token
    access_token_data = {
        "sub": user.email,
        "is_sys_admin": user.is_sys_admin  # Include this directly in access token
    }
    
    # Create Access token - contains authorization information
    access_token = create_access_token(
        data=access_token_data,
        expires_delta=access_token_expires
    )
    
    # Create ID token - contains user identity information
    id_token = create_id_token(
        user_data=user_data,
        expires_delta=id_token_expires
    )

    # Return both tokens and user profile for convenience
    return {
        "access_token": access_token, 
        "id_token": id_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Seconds
    }

@router.post("/refresh-token")
async def refresh_token(refresh_token: str):
    """
    Refresh token endpoint
    - **refresh_token**: str
    - **return**: new access token
    - **status**: 200 OK
    """

    try:
        payload = jwt.decode(
            refresh_token, 
            settings.get_jwt_key, 
            algorithms=[settings.ALGORITHM]
        )
        user_email = payload.get("sub")
        
        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create a new access token
        access_token = create_access_token(
            data={"sub": user_email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/debug-token", dependencies=[Depends(get_current_admin_user)])
async def debug_token(token: str = Depends(oauth2_scheme)):
    """Debug endpoint to check token details (admin only)"""
    try:
        # Decode without verification for debugging
        payload = jwt.decode(
            token, 
            settings.get_jwt_key, 
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": False}  # Skip expiration check for debugging
        )
        
        # Calculate expiration info
        if "exp" in payload:
            exp_dt = datetime.fromtimestamp(payload["exp"])
            now = datetime.utcnow()
            is_expired = exp_dt < now
            time_left = (exp_dt - now).total_seconds() if not is_expired else 0
            
            return {
                "payload": payload,
                "expiration": exp_dt.isoformat(),
                "current_time": now.isoformat(),
                "is_expired": is_expired,
                "seconds_remaining": time_left
            }
        
        return {"payload": payload, "expiration": "No expiration found"}
        
    except Exception as e:
        return {"error": str(e)}
