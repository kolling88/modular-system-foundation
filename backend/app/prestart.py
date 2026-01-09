import logging
from sqlalchemy import text
from app.db.session import SessionLocal
from app.db.init_db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main() -> None:
    logger.info("Initializing service")
    db = SessionLocal()
    try:
        # Verificar conexão
        db.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        
        # Executar seed
        logger.info("Creating initial data")
        init_db(db)
        logger.info("Initial data created")
    except Exception as e:
        logger.error(f"Error initializing service: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    main()
