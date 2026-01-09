from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user_service import user_service
from app.core import security
from app.core.config import settings
from app.schemas.token import Token
from app.schemas.msg import Msg

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = user_service.get_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/password-recovery/{email}", response_model=Msg)
def recover_password(email: str, db: Session = Depends(get_db)) -> Any:
    """
    Password Recovery
    """
    user = user_service.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    # Aqui em um sistema real enviaríamos um e-mail com um token JWT
    # Para este MVP, vamos apenas simular o sucesso
    return {"msg": "Password recovery email sent"}

@router.post("/reset-password/", response_model=Msg)
def reset_password(
    token: str, new_password: str, db: Session = Depends(get_db)
) -> Any:
    """
    Reset password
    """
    # Em um sistema real, validaríamos o token JWT aqui
    # Para o MVP, vamos apenas buscar o usuário pelo ID (simulando que o token continha o ID 1)
    user = user_service.get(db, id=1) 
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    user_service.update(db, db_obj=user, obj_in={"password": new_password})
    return {"msg": "Password updated successfully"}
