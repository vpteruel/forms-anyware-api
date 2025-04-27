from pydantic import BaseModel

class DepartmentUserRole(BaseModel):
    id: int
    department_id: int
    user_id: int
    role_id: int
