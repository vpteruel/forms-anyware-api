from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: Optional[str]
    email: str
    password: Optional[str]
    is_admin: bool
    last_login: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
