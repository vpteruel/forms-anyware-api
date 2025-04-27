from enum import Enum

class RequisitionStatus(Enum):
    DRAFT = 1
    IN_PROGRESS = 2
    PENDING = 3
    APPROVED = 4
    REJECTED = 5
    CANCELLED = 6
    SKIPPED = 7

    @classmethod
    def get_status(cls, status_id: int) -> str:
        for status in cls:
            if status.value == status_id:
                return status.name
        return "Unknown Status"