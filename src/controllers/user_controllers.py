import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.controllers.base import BaseController
from src.models.models import User
from src.schemas.user_schemas import UserCreate

logger = logging.getLogger("uvicorn.error")


class UsersController(BaseController):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(self.model).filter_by(username=username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(self.model).filter_by(email=email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(
        self, user: UserCreate, hash_password: str, avatar: str
    ) -> User:
        user = User(
            **user.model_dump(exclude_unset=True, exclude={"password"}),
            hash_password=hash_password,
            avatar=avatar,
        )
        return await self.create(user)

    async def confirmed_email(self, email: str) -> User | None:
        user = await self.get_user_by_email(email)
        user.confirmed = True
        await self.db.commit()

    async def update_avatar_url(self, email: str, url: str) -> User:
        user = await self.get_user_by_email(email)
        user.avatar = url
        await self.db.commit()
        await self.db.refresh(user)
        return user
