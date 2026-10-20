"""Configuração compartilhada de conexão com o PostgreSQL."""
import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

DB_NAME = os.getenv("POSTGRES_DB", "iot_db")
DB_USER = os.getenv("POSTGRES_USER", "iot_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "iot_senha_local")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def get_engine():
    """Cria um engine SQLAlchemy para acessar o banco."""
    return create_engine(DATABASE_URL, pool_pre_ping=True)
