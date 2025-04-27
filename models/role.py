from enum import Enum

class Role(Enum):
    ADMINISTRADOR = 1
    INITIATOR = 2
    DELEGATE = 3
    SUPERVISOR = 4
    MANAGER = 5
    DIRECTOR = 6
    VP_FOR_DEPARTMENT = 7
    VP_CFE = 8
    CEO = 9
    BOARD_CHAIR = 10

    @classmethod
    def get_role(cls, role_id: int) -> str:
        for role in cls:
            if role.value == role_id:
                return role.name
        return "Unknown Role"
