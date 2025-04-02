from sqlalchemy.ext.asyncio import AsyncSession

from src.controllers.user_controllers import UsersController
from src.schemas.user_schemas import UserCreate
from src.models.models import User
from src.services.auth_service import AuthService


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_controller = UsersController(self.db)
        self.auth_service = AuthService(self.db)

    async def create_user(self, user_data: UserCreate) -> User:
        user = await self.auth_service.register_user(user_data)
        return user

    async def get_by_username(self, username: str) -> User | None:
        return await self.user_controller.get_by_username(username)
