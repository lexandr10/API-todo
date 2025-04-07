from fastapi import (
    APIRouter,
    Depends,
    status,
    Request,
    HTTPException,
    BackgroundTasks,
    UploadFile,
    File,
)
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.conf.config import settings
from src.core.email_token import get_email_from_token
from src.database.db import get_db
from src.schemas.schema_email import RequestEmailSchema
from src.schemas.user_schemas import UserResponse
from src.services.auth_service import AuthService, oauth2_scheme
from src.models.models import User
from src.core.depend_service import (
    get_current_admin,
    get_current_moderator,
    get_user_service,
)
from src.services.service_email import send_email
from src.services.user_sevice import UserService
from src.services.upload_file_service import UploadFileService

router = APIRouter(prefix="/users", tags=["users"])
limiter = Limiter(key_func=get_remote_address)


def get_auth_service(db: AsyncSession = Depends(get_db)):
    return AuthService(db)


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
@limiter.limit("10/minute")
async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.get_current_user(token)


@router.get("/confirmed_email/{token}")
async def confirm_email(
    token: str,
    user_service: UserService = Depends(get_user_service),
):
    email = get_email_from_token(token)
    user = await user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user.confirmed:
        return {"message": "Email already confirmed"}

    await user_service.confirmed_email(email)
    return {"message": "Email confirmed"}


@router.post("/request_email")
async def request_email(
    body: RequestEmailSchema,
    background_tasks: BackgroundTasks,
    request: Request,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user_by_email(str(body.email))

    if user.confirmed:
        return {"message": "Email already confirmed"}
    if user:
        background_tasks.add_task(
            send_email, user.email, user.username, str(request.base_url)
        )

    return {"message": "Email sent"}


@router.patch("/avatar", response_model=UserResponse)
async def update_avatar(
    file: UploadFile = File(),
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    avatar_url = UploadFileService(
        settings.CLD_NAME, settings.CLD_API_KEY, settings.CLD_API_SECRET
    ).upload_file(file, user.username)

    user = await user_service.update_avatar_url(user.email, avatar_url)

    return user


@router.get("/moderator")
def read_moderator(current_user: User = Depends(get_current_moderator)):
    return {"message": f"Hello Moderator {current_user.username}"}


@router.get("/admin")
def read_admin(current_user: User = Depends(get_current_admin)):
    return {"message": f"Hello Admin {current_user.username}"}
