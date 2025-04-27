from typing import Optional
from pydantic import BaseModel

class Department(BaseModel):
    id: int
    name: str
    code: str
    created_at: Optional[str]
    updated_at: Optional[str]
    deleted_at: Optional[str]
