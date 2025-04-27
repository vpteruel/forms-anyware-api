from enum import Enum

class PurchaseRequisitionStatus(Enum):
    DRAFT = 1
    PENDING = 2
    APPROVED = 3
    REJECTED = 4
    CANCELLED = 5

    @classmethod
    def get_status(cls, status_id: int) -> str:
        for status in cls:
            if status.value == status_id:
                return status.name
        return "Unknown Status"
