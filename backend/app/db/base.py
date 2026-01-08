# Importar todos os modelos para que o Base.metadata os conheça
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.role import Role  # noqa
from app.models.user_role import UserRole  # noqa
