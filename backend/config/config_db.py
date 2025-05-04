from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from backend.utils.logger import logger

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    DATABASE_URL: str

settings = Settings()
logger.info(f"DATABASE_URI leída: {settings.DATABASE_URL}")

# Crear el engine sin abrir la conexión inmediatamente
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# Configurar sessionmaker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def init_db():
    from backend.db.base import Base
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas de la base de datos creadas o ya existentes.")
    except OperationalError as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        raise


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.info("Conexión a la base de datos cerrada.")
