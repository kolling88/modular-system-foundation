from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user_service import user_service
from app.services.role_service import role_service
from app.schemas.user import User, UserCreate, UserUpdate
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[User], dependencies=[Depends(deps.get_current_active_user)])
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    return user_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=User, dependencies=[Depends(deps.get_current_active_superuser)])
def create_user(user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
    user = user_service.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    return user_service.create(db, obj_in=user_in)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)) -> Any:
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)) -> Any:
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_service.update(db, db_obj=user, obj_in=user_in)

@router.post("/{user_id}/roles/{role_id}", response_model=User)
def assign_role_to_user(user_id: int, role_id: int, db: Session = Depends(get_db)) -> Any:
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    role = role_service.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return user_service.assign_role(db, user=user, role=role)

@router.delete("/{user_id}/roles/{role_id}", response_model=User)
def remove_role_from_user(user_id: int, role_id: int, db: Session = Depends(get_db)) -> Any:
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    role = role_service.get(db, id=role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return user_service.remove_role(db, user=user, role=role)
