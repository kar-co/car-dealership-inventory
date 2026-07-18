from app.core.config import settings
from sqlalchemy import create_engine

engine = create_engine(settings.sqlalchemy_database_url, pool_pre_ping=True)
