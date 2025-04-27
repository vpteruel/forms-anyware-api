from typing import Optional
from pydantic import BaseModel

class PurchaseRequisitionItem(BaseModel):
    id: int
    purchase_requisition_id: int
    quantity: int
    unit_measure: str
    unit_price: float
    vendor_catalogue_number: str
    eoc_cip: str
    description: str
    total: float
    created_at: Optional[str]
    updated_at: Optional[str]
    deleted_at: Optional[str]
