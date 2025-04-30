from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, not_
from typing import List, Optional, Dict, Any
from datetime import datetime

from models.orm_models import User, Department, Role, DepartmentUserRole
from models.user import UserCreate, UserUpdate

class UserService:
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).filter(User.deleted_at.is_(None)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(
            and_(User.id == user_id, User.deleted_at.is_(None))
        ).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(
            and_(User.email == email, User.deleted_at.is_(None))
        ).first()
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            password=user.password,  # This should be hashed
            is_sys_admin=user.is_sys_admin
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None
            
        # Update fields if provided
        if user.first_name is not None:
            db_user.first_name = user.first_name
        if user.last_name is not None:
            db_user.last_name = user.last_name
        if user.username is not None:
            db_user.username = user.username
        if user.email is not None:
            db_user.email = user.email
        if user.password is not None:
            db_user.password = user.password  # This should be hashed
        if user.is_sys_admin is not None:
            db_user.is_sys_admin = user.is_sys_admin
            
        db_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return False
            
        # Soft delete
        db_user.deleted_at = datetime.utcnow()
        db.commit()
        return True
    
    @staticmethod
    def get_user_departments_roles(db: Session, user_id: int) -> List[Dict[str, Any]]:
        result = db.query(DepartmentUserRole, Department, Role)\
            .join(Department, DepartmentUserRole.department_id == Department.id)\
            .join(Role, DepartmentUserRole.role_id == Role.id)\
            .filter(
                and_(
                    DepartmentUserRole.user_id == user_id,
                    Department.deleted_at.is_(None)
                )
            ).all()
        
        return [
            {
                "department_id": dept.id,
                "department_name": dept.name,
                "department_code": dept.code,
                "role_id": role.id,
                "role_name": role.name
            }
            for dur, dept, role in result
        ]