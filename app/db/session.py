from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import AppConfig as ac

aurl = f"postgresql+asyncpg://{ac.pg_user}:{ac.pg_pass}@{ac.pg_host}:{ac.pg_port}/{ac.pg_db}"

async_engine = create_async_engine(aurl, echo=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
