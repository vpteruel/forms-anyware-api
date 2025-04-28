from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

from models.user import User

# Move these to config.py in production
SECRET_KEY = "your-secret-key-here-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class UserInDB(User):
    password: str

# Create a password context that explicitly configures the bcrypt handler
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Explicitly set rounds
)

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

    # Add user profile data
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

    # Set expiration
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)  # ID tokens can live longer
    to_encode.update({"exp": expire})

    # Create the ID token
    id_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return id_token

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create an access token containing authorization information
    """
    to_encode = data.copy()
    to_encode.update({
        "iss": "forms-anyware-api",  # issuer
        "aud": "forms-anyware-api",  # audience (API)
        "iat": datetime.utcnow(),  # issued at time
    })

    # Add permissions/scopes if needed
    to_encode.update({"scope": "read:forms write:forms"})  # Example scopes

    # Set expiration (access tokens typically have shorter lifespans)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Create the access token
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Validate the token and extract user information
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Verify the token
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM],
            options={"verify_aud": False}
        )

        # Get the subject (email)
        email: str = payload.get("sub")
        if email is None:
            logger.error("Token missing 'sub' claim")
            raise credentials_exception

        # Try to get user from DB
        user = get_user(fake_users_db, email=email)
        if user is None:
            raise credentials_exception

        return user

    except JWTError as e:
        raise credentials_exception

# Optional helper to decode ID tokens (for clients)
def decode_id_token(token: str):
    """
    Decode and validate an ID token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Check if it's an ID token
        if "profile" not in payload:
            raise ValueError("Not a valid ID token")
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")