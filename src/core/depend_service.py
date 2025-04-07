from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException

from src.database.db import get_db
from src.services.auth_service import AuthService, oauth2_scheme
from src.services.user_sevice import UserService
from src.models.models import User, UserRole


def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService(db)


def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)


async def get_current_user(
    auth_service: AuthService = Depends(get_auth_service),
    token: str = Depends(oauth2_scheme),
):
    return await auth_service.get_current_user(token)


def get_current_moderator(current_user: User = Depends(get_current_user)):
    if current_user.role not in [UserRole.ADMIN, UserRole.MODERATOR]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user


def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Forbidden")

    return current_user
