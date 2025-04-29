from pydantic import BaseModel, field_validator
from typing import Optional, Dict, Any
import time

class Token(BaseModel):
    """Model for token response"""
    access_token: str
    id_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int = 3600  # Default to 1 hour

class TokenPayload(BaseModel):
    """Model for JWT token payload validation"""
    # Standard JWT claims
    sub: str  # Subject (typically user email or ID)
    exp: int  # Expiration time (Unix timestamp)
    
    # Optional standard JWT claims
    iss: Optional[str] = None  # Issuer
    aud: Optional[str] = None  # Audience
    iat: Optional[int] = None  # Issued at time
    
    # User profile information
    is_sys_admin: Optional[bool] = False
    profile: Optional[Dict[str, Any]] = None
    
    # Access control flags
    is_sys_admin: Optional[bool] = False

    @field_validator("exp", mode="before")
    def check_expiration(cls, v):
        # Ensure the token is not expired
        if v < time.time():
            raise ValueError("Token has expired")
        return v
    
    class Config:
        arbitrary_types_allowed = True

class RefreshToken(BaseModel):
    """Model for refresh token"""
    refresh_token: str

class TokenRefreshRequest(BaseModel):
    """Model for token refresh request"""
    refresh_token: str
