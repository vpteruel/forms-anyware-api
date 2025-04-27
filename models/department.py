from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Department(BaseModel):
    id: int
    name: str
    code: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
