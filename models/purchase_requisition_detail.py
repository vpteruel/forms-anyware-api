from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PurchaseRequisitionDetail(BaseModel):
    id: int
    requisition_id: int
    site_id: int
    purchase_type_id: int
    po_number: Optional[str]
    tel_ext: Optional[str]
    comments: Optional[str]
    suggested_supplier: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
