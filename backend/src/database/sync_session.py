from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import get_settings

settings = get_settings()

sync_postgresql_engine = create_engine(settings.sync_database_url, echo=False)
SyncSessionLocal = sessionmaker(
    bind=sync_postgresql_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
