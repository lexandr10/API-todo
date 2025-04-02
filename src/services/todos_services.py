from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from src.controllers.todos_controllers import TodosController
from src.schemas.todo_schemas import (
    TodoSchemaUpdate,
    TodoUpdateStatusSchema,
    TodoSchema,
    TodoResponse,
)


class TodosServices:
    def __init__(self, db: AsyncSession):
        self.todos_controller = TodosController(db)

    async def create_todo(self, todo: TodoSchema):
        todo = await self.todos_controller.create_todo(todo)
        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return todo

    async def get_todos(self, limit: int, offset: int):
        todos = await self.todos_controller.get_todos(limit, offset)
        if todos is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return todos

    async def get_todo_by_id(self, todo_id: int):
        todo = await self.todos_controller.get_todo_by_id(todo_id)
        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return todo

    async def update_todo(self, todo_id: int, todo: TodoSchemaUpdate):
        update_todo = await self.todos_controller.update_todo(todo_id, todo)
        if update_todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return update_todo

    async def update_todo_status(self, todo_id: int, todo: TodoUpdateStatusSchema):
        update_status = await self.todos_controller.update_todo(todo_id, todo)
        if update_status is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
            )
        return update_status

    async def remove_todo(self, todo_id: int):
        return await self.todos_controller.remove_todo(todo_id)
