from datetime import datetime
from typing import List, Sequence
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.controllers.base import BaseController
from src.models.models import RefreshToken
from src.schemas.user_schemas import UserResponse, UserSchema, UserCreate

logger = logging.getLogger("uvicorn.error")


class RefreshTokenController(BaseController):
    def __init__(self, session: AsyncSession):
        super().__init__(
            session,
            RefreshToken,
        )

    async def get_by_token_hash(self, token_hash: str) -> RefreshToken | None:
        stmt = select(self.model).where(RefreshToken.token_hash == token_hash)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_token(
        self, token_hash: str, current_time: datetime
    ) -> RefreshToken | None:
        stmt = select(self.model).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.expires_at > current_time,
            RefreshToken.revoked_at is None,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_token(
        self,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
        ip_address: str,
        user_agent: str,
    ) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        return await self.create(refresh_token)

    async def revoke_token(self, refresh_token: RefreshToken) -> None:
        refresh_token.revoked_at = datetime.now()
        await self.db.commit()
