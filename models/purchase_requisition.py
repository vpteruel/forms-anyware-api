from typing import Literal
from pydantic import BaseModel

class PurchaseRequisition(BaseModel):
    id: int
    date: str
    supplier: str
    qtyItems: int
    totalAmount: float
    status: Literal['pending', 'approved', 'rejected']
