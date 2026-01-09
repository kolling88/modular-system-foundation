from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.role_service import role_service
from app.schemas.role import Role, RoleCreate, RoleUpdate

router = APIRouter()

@router.get("/", response_model=List[Role])
def read_roles(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    return role_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=Role)
def create_role(role_in: RoleCreate, db: Session = Depends(get_db)) -> Any:
    role = role_service.get_by_name(db, name=role_in.name)
    if role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return role_service.create(db, obj_in=role_in)

@router.get("/{role_id}", response_model=Role)
def read_role(role_id: int, db: Session = Depends(get_db)) -> Any:
    role = role_service.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.put("/{role_id}", response_model=Role)
def update_role(role_id: int, role_in: RoleUpdate, db: Session = Depends(get_db)) -> Any:
    role = role_service.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role_service.update(db, db_obj=role, obj_in=role_in)
