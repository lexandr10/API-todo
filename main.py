from datetime import datetime, timezone, timedelta
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status, Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.middleware.cors import CORSMiddleware

from src.database.db import get_db, sessionmanager
from src.routes.v1 import todos_routes, auth_route, users_route

scheduler = AsyncIOScheduler()


async def cleanup_expired_tokens():
    async with sessionmanager.session() as db:
        time_now = datetime.now(timezone.utc)
        cutoff = time_now - timedelta(days=7)
        stmt = text(
            "DELETE FROM refresh_tokens WHERE expired_at < :time_now OR revoked_at IS NOT NULL AND revoked_at < :cutoff"
        )
        await db.execute(stmt, {"time_now": time_now, "cutoff": cutoff})
        await db.commit()
        print(f"Cleaned up expired tokens [{time_now.strftime('%Y-%m-%d %H:%M:%S')}]")


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(cleanup_expired_tokens, "interval", hours=1)
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    lifespan=lifespan,
    title="Todo app v1.0.0",
    description="This is a todo app with FastAPI and SQLAlchemy",
    version="1.0.0",
)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"message": "Rate limit exceeded"},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todos_routes.router, prefix="/api/v1")
app.include_router(auth_route.router, prefix="/api/v1")
app.include_router(users_route.router, prefix="/api/v1")


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
