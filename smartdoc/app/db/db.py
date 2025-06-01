from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from fastapi import HTTPException

engine = create_async_engine(settings.DATABASE_URL, pool_size=20, max_overflow=0)
async_session = sessionmaker(engine, autoCommit=False, autoFlush=False, expire_on_commit=False, bind=engine)
Base = declarative_base()

from typing import AsyncGenerator

async def get_database() -> AsyncGenerator[AsyncSession, None]:
    try:
        async with async_session() as session:
            yield session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")