from typing import List, Sequence
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.models.models import Todo, User
from src.schemas.todo_schemas import (
    TodoSchemaUpdate,
    TodoUpdateStatusSchema,
    TodoSchema,
)

logger = logging.getLogger("uvicorn.error")


class TodosController:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_todos(self, limit: int, offset: int, user: User) -> Sequence[Todo]:
        stmt = select(Todo).filter_by(user_id=user.id).limit(limit).offset(offset)
        todos = await self.db.execute(stmt)
        return todos.scalars().all()

    async def get_todo_by_id(self, todo_id: int, user: User) -> Todo:
        stmt = select(Todo).filter_by(id=todo_id, user_id=user.id)
        todo = await self.db.execute(stmt)
        return todo.scalar_one_or_none()

    async def create_todo(self, todo: TodoSchema, user: User) -> Todo:
        new_todo = Todo(**todo.model_dump(), user=user)
        self.db.add(new_todo)
        await self.db.commit()
        await self.db.refresh(new_todo)
        return new_todo

    async def remove_todo(self, todo_id: int, user: User) -> None:
        todo = await self.get_todo_by_id(todo_id, user)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        await self.db.delete(todo)
        await self.db.commit()

    async def update_todo(
        self, todo_id: int, todo: TodoSchemaUpdate | TodoUpdateStatusSchema, user: User
    ) -> Todo | None:
        todo_to_update = await self.get_todo_by_id(todo_id, user)
        if todo_to_update is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        update_data = todo.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(todo_to_update, key, value)
        await self.db.commit()
        await self.db.refresh(todo_to_update)
        return todo_to_update
