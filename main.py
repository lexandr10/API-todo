from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.routes.v1 import todos_routes, auth_route

app = FastAPI()

app.include_router(todos_routes.router, prefix="/api/v1")
app.include_router(auth_route.router, prefix="/api/v1")


@app.get("/")
async def read_root():
    return {"message": "Todo app v1.0.0"}


@app.get("/api/healthChecker")
async def health_checker(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not available",
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )
