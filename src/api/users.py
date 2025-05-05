from fastapi import APIRouter, Depends, Request, UploadFile, File

from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import User
from src.conf.config import config
from src.services.auth import get_current_user
from src.services.users import UserService
from src.services.upload_file import UploadFileService


router = APIRouter(prefix="/users", tags=["users"])
"""
Users API Router

This router handles user-related operations such as retrieving user information
and updating user avatars. It provides endpoints for authenticated users to
manage their profile and personal information.

Endpoints:
- GET /me: Retrieve current user's information
- PATCH /avatar: Update user's avatar image

All endpoints require authentication and have rate limiting to prevent abuse.
"""
limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/me", response_model=User, description="No more than 10 requests per minute"
)
@limiter.limit("10/minute")
async def me(request: Request, user: User = Depends(get_current_user)):
    """
    Retrieve the current authenticated user's information.

    This endpoint returns the details of the currently logged-in user.
    It is rate-limited to 10 requests per minute to prevent abuse.

    Args:
        request (Request): The incoming HTTP request.
        user (User, optional): The authenticated user, obtained via dependency injection.

    Returns:
        User: The current user's information.
    """
    return user


@router.patch("/avatar", response_model=User)
async def update_avatar_user(
    file: UploadFile = File(),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update the avatar for the current user.

    This endpoint allows a user to upload a new avatar image. The image is uploaded
    to a cloud storage service (Cloudinary) and the avatar URL is updated in the database.

    Args:
        file (UploadFile): The image file to be uploaded as the new avatar.
        user (User, optional): The authenticated user, obtained via dependency injection.
        db (AsyncSession, optional): The database session, obtained via dependency injection.

    Returns:
        User: The updated user object with the new avatar URL.
    """
    avatar_url = UploadFileService(
        config.CLD_NAME, config.CLD_API_KEY, config.CLD_API_SECRET
    ).upload_file(file, user.username)

    user_service = UserService(db)
    user = await user_service.update_avatar_url(user.email, avatar_url)

    return user