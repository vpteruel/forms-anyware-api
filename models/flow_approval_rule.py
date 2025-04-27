from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class FlowApprovalRules(BaseModel):
    id: int
    flow_version_id: int
    role_id: int
    approval_level: int
    min_amount: float
    max_amount: float
    can_skip: bool
    skip_reason_required: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
