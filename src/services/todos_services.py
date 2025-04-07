from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from src.controllers.todos_controllers import TodosController
from src.models.models import User
from src.schemas.todo_schemas import (
    TodoSchemaUpdate,
    TodoUpdateStatusSchema,
    TodoSchema,
)


class TodosServices:
    def __init__(self, db: AsyncSession):
        self.todos_controller = TodosController(db)

    async def create_todo(self, todo: TodoSchema, user: User):
        todo = await self.todos_controller.create_todo(todo, user)
        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return todo

    async def get_todos(self, limit: int, offset: int, user: User):
        todos = await self.todos_controller.get_todos(limit, offset, user)
        if todos is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return todos

    async def get_todo_by_id(self, todo_id: int, user: User):
        todo = await self.todos_controller.get_todo_by_id(todo_id, user)
        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return todo

    async def update_todo(self, todo_id: int, todo: TodoSchemaUpdate, user: User):
        update_todo = await self.todos_controller.update_todo(todo_id, todo, user)
        if update_todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return update_todo

    async def update_todo_status(
        self, todo_id: int, todo: TodoUpdateStatusSchema, user: User
    ):
        update_status = await self.todos_controller.update_todo(todo_id, todo, user)
        if update_status is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return update_status

    async def remove_todo(self, todo_id: int, user: User):
        return await self.todos_controller.remove_todo(todo_id, user)
