from typing import Optional
from pydantic import BaseModel

class PurchaseRequisitionType(BaseModel):
    id: int
    name: str
    created_at: Optional[str]
    updated_at: Optional[str]
    deleted_at: Optional[str]
