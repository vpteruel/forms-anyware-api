from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext

from core.config import settings
from models.auth.token import TokenPayload
from models.user import User

# OAuth2 scheme that will get the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)

class UserInDB(User):
    password: str

# Create a password context that explicitly configures the bcrypt handler
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Explicitly set rounds
)

# This is a mock user database for demonstration
fake_users_db = {
    "user@example.com": {
        "id": 1,
        "first_name": "First",
        "last_name": "Last",
        "username": "first.last",
        "email": "user@example.com",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
        "is_sys_admin": True,
        "last_login": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "deleted_at": None,
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, email: str):
    if email in db:
        user_dict = db[email]
        return UserInDB(**user_dict)

def authenticate_user(email: str, password: str):
    user = get_user(fake_users_db, email)

    if not user:
        return False
    if not verify_password(password, user.password):
        return False

    return user

def create_id_token(user_data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create an ID token containing user identity information
    """
    to_encode = {
        "sub": user_data.get("email"),
        "iss": "forms-anyware-api",  # issuer
        "aud": "forms-anyware-client",  # audience
        "iat": datetime.utcnow(),  # issued at time
    }

    profile_data = {
        "id": user_data.get("id"),
        "email": user_data.get("email"),
        "first_name": user_data.get("first_name"),
        "last_name": user_data.get("last_name"),
        "username": user_data.get("username"),
        "is_sys_admin": user_data.get("is_sys_admin"),
        "last_login": user_data.get("last_login"),
    }
    to_encode.update({"profile": profile_data})

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)  # ID tokens can live longer

    to_encode.update({"exp": expire})

    id_token = jwt.encode(to_encode, settings.get_jwt_key, algorithm=settings.ALGORITHM)
    return id_token

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token with an expiration time"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.get_jwt_key, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """Get the current user from the JWT token"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(
            token, 
            settings.get_jwt_key,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": True}  # Explicitly verify expiration
        )

        token_data = TokenPayload(**payload)
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return payload

def get_current_user_optional(token: str = Depends(oauth2_scheme)) -> Optional[Dict[str, Any]]:
    """Get the current user from JWT token if available, otherwise return None"""
    if not token:
        return None
    
    try:
        payload = jwt.decode(
            token, 
            settings.get_jwt_key,  # Use the property
            algorithms=[settings.ALGORITHM]
        )

        token_data = TokenPayload(**payload)
            
    except (JWTError, ValidationError):
        return None
        
    return payload

def get_current_active_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Ensure the user is active"""
    if not current_user.get("is_active", True):  # Default to True if not specified
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user

def get_current_admin_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Ensure the user is an admin"""
    if not current_user.get("is_sys_admin", False):  # Default to False if not specified
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user

def get_user_from_request(request: Request) -> Optional[Dict[str, Any]]:
    """Extract user from request state if available (set by middleware)"""
    return getattr(request.state, "user", None)

# Optional helper to decode ID tokens (for clients)
def decode_id_token(token: str):
    """
    Decode and validate an ID token
    """
    try:
        payload = jwt.decode(token, settings.get_jwt_key, algorithms=[settings.ALGORITHM])
        # Check if it's an ID token
        if "profile" not in payload:
            raise ValueError("Not a valid ID token")
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")
