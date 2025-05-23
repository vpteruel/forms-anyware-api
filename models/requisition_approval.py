from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class RequisitionApproval(BaseModel):
    id: int
    requisition_id: int
    approval_level: int
    role_id: int
    approver_id: Optional[int]
    status_id: int
    comments: Optional[str]
    decision_date: Optional[datetime]
    skipped: bool
    skip_reason: Optional[str]
    skipped_by_user_id: Optional[int]
    skipped_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
