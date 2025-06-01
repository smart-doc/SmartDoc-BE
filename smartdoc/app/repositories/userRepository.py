from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from ..models.user import User
from ..models import UserRole
from ..security import get_password_hash, verify_password

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, email: str, password: str, role: UserRole) -> User:
        hashed_password = get_password_hash(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            role=role
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
    
    async def update_password(self, user: User, new_password: str):
        user.hashed_password = get_password_hash(new_password)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_all_users(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()