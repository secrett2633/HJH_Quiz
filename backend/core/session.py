from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from backend.core.config import settings

echo = True

if settings.ENV_STATE == "test":
    uri = f"{settings.DATABASE_URI}?prepared_statement_cache_size=0"
elif settings.ENV_STATE == "prod":
    echo = False
    uri = settings.DATABASE_URI
else:
    uri = settings.DATABASE_URI

engine = create_async_engine(uri, echo=echo)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
