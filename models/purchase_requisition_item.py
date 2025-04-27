from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PurchaseRequisitionItem(BaseModel):
    id: int
    purchase_requisition_detail_id: int
    quantity: int
    unit_measure: str
    unit_price: float
    vendor_catalogue_number: str
    eoc_cip: str
    description: str
    total: float
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
