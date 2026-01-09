from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate

class RoleService:
    def get(self, db: Session, id: int) -> Optional[Role]:
        return db.query(Role).filter(Role.id == id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Role]:
        return db.query(Role).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: RoleCreate) -> Role:
        db_obj = Role(
            name=obj_in.name,
            description=obj_in.description,
            permissions=obj_in.permissions
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Role, obj_in: RoleUpdate) -> Role:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> Role:
        obj = db.query(Role).get(id)
        db.delete(obj)
        db.commit()
        return obj

role_service = RoleService()
