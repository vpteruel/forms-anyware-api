from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PurchaseRequisitionType(BaseModel):
    id: int
    name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
