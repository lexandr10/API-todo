import logging

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.services.todos_services import TodosServices
from src.schemas.todo_schemas import (
    TodoSchema,
    TodoSchemaUpdate,
    TodoResponse,
    TodoUpdateStatusSchema,
)

router = APIRouter(prefix="/todos", tags=["todos"])
logger = logging.getLogger("uvicorn.error")


@router.get("/", response_model=list[TodoResponse])
async def get_todos(
    limit: int = Query(10, ge=0, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    todo_services = TodosServices(db)
    return await todo_services.get_todos(limit, offset)


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo_services = TodosServices(db)
    return await todo_services.get_todo_by_id(todo_id)


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoSchema, db: AsyncSession = Depends(get_db)):
    todo_services = TodosServices(db)
    return await todo_services.create_todo(todo)


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int, todo: TodoSchemaUpdate, db: AsyncSession = Depends(get_db)
):
    todo_services = TodosServices(db)
    return await todo_services.update_todo(todo_id, todo)


@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo_status(
    todo_id: int, todo: TodoUpdateStatusSchema, db: AsyncSession = Depends(get_db)
):
    todo_services = TodosServices(db)
    return await todo_services.update_todo_status(todo_id, todo)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int, db: AsyncSession = Depends(get_db)):
    todo_services = TodosServices(db)
    return await todo_services.remove_todo(todo_id)
