from typing import Generator, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import TokenPayload
from app.services.user_service import user_service

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token"
)

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = user_service.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

class PermissionChecker:
    def __init__(self, required_permissions: List[str]):
        self.required_permissions = required_permissions

    def __call__(self, current_user: User = Depends(get_current_active_user)):
        # Se for superuser, tem acesso total
        if current_user.is_superuser:
            return True
            
        # Coletar todas as permissões dos perfis do usuário
        user_permissions = []
        for role in current_user.roles:
            if role.permissions:
                user_permissions.extend([p.strip() for p in role.permissions.split(",")])
        
        # Verificar se tem as permissões necessárias
        for perm in self.required_permissions:
            if perm not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing required permission: {perm}"
                )
        return True
