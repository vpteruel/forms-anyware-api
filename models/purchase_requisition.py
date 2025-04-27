from typing import Optional
from pydantic import BaseModel

class PurchaseRequisition(BaseModel):
    id: int
    site_id: int
    type_id: int
    department_id: int
    user_id: int
    status_id: int
    pr_number: str
    po_number: Optional[str]
    requisition_date: str
    tel_ext: Optional[str]
    comments: Optional[str]
    suggested_supplier: Optional[str]
    skip_delegate_approval: bool
    skip_manager_approval: bool
    skip_director_approval: bool
    skip_vp_department_approval: bool
    skip_vp_cfe_approval: bool
    skip_ceo_approval: bool
    created_at: Optional[str]
    updated_at: Optional[str]
    deleted_at: Optional[str]
