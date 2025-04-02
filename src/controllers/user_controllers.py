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

    async def create_user(self, user: UserCreate, hash_password: str) -> User:
        user = User(
            **user.model_dump(exclude_unset=True, exclude={"password"}),
            hash_password=hash_password
        )
        return await self.create(user)
