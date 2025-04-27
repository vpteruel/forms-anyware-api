from typing import Optional
from pydantic import BaseModel

class Site(BaseModel):
    id: int
    name: str
    mnemonic: str
    location: str
    created_at: Optional[str]
    updated_at: Optional[str]
    deleted_at: Optional[str]
