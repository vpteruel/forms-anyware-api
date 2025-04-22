from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    full_name: str
    username: Optional[str]
    email: str
    password: Optional[str]
