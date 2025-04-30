from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import JWTError, jwt

from core.config import settings
from core.database import get_db
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
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token_expires = settings.access_token_expires
    
    # Create user_data dict from ORM user object
    user_data = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "is_sys_admin": user.is_sys_admin,
        "last_login": user.last_login.isoformat() if user.last_login else None
    }
    
    # Create access token with minimal claims
    access_token_data = {
        "sub": user.email,
        # Include essential permissions directly in access token
        "is_sys_admin": user.is_sys_admin
    }
    
    access_token = create_access_token(
        data=access_token_data,
        expires_delta=access_token_expires
    )
    
    # Create ID token with full profile information
    id_token = create_id_token(
        user_data=user_data,
        expires_delta=timedelta(days=7)  # ID tokens typically last longer
    )
    
    return {
        "access_token": access_token,
        "id_token": id_token,
        "token_type": "bearer",
        "expires_in": int(access_token_expires.total_seconds())
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
