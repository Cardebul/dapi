import os
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from dotenv import load_dotenv

load_dotenv()




DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('POSTGRES_DB')}"

aurl = DATABASE_URL
async_engine = create_async_engine(aurl, echo=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
