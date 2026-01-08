from sqlalchemy.orm import Session
from app.models.role import Role
from app.models.user import User
from app.core.config import settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db(db: Session) -> None:
    # Criar perfis iniciais
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        admin_role = Role(
            name="admin",
            description="Administrador do Sistema",
            permissions="all"
        )
        db.add(admin_role)

    user_role = db.query(Role).filter(Role.name == "user").first()
    if not user_role:
        user_role = Role(
            name="user",
            description="Usuário Padrão",
            permissions="read,write"
        )
        db.add(user_role)

    # Criar superusuário inicial
    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user = User(
            full_name="Administrator",
            email="admin@example.com",
            hashed_password=pwd_context.hash("admin123"),
            is_superuser=True,
        )
        db.add(user)
        db.flush()  # Para obter o ID do usuário
        
        # Vincular perfil admin ao usuário
        user.roles.append(admin_role)

    db.commit()
