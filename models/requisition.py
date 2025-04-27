from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Requisition(BaseModel):
    id: int
    requisition_number: str
    requisition_type_id: int
    flow_id: int
    flow_version_id: int
    department_id: int
    initiator_id: int
    current_status_id: int
    total_amount: float
    submission_date: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
