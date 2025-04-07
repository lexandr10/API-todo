from datetime import datetime
from enum import Enum

from sqlalchemy import (
    String,
    DateTime,
    func,
    ForeignKey,
    Text,
    Enum as SqlaEnum,
    Boolean,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped, mapped_column

from src.conf import containts


class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(containts.TITLE_MAX_LENGTH), nullable=False
    )
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    completed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["User"] = relationship("User", backref="todos", lazy="joined")


class UserRole(str, Enum):
    USER = "USER"
    MODERATOR = "MODERATOR"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SqlaEnum(UserRole), default=UserRole.USER, nullable=False
    )
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        "RefreshToken", back_populates="user"
    )


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    token_hash: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[str] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")
