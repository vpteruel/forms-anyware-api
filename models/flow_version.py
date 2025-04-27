from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class FlowVersion(BaseModel):
    id: int
    flow_id: int
    version: int
    is_active: bool
    effective_from: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
