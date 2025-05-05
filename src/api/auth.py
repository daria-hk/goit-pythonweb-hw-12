from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas import UserCreate, Token, User, RequestEmail
from src.services.auth import create_access_token, Hash, get_email_from_token
from src.services.users import UserService
from src.services.email import send_email
from src.database.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])
"""
Authentication API Router

This router handles user authentication and email confirmation operations.
It provides endpoints for user registration, login, email confirmation, and
re-requesting email confirmation.

Endpoints:
- POST /register: Register a new user
- POST /login: Authenticate a user and generate an access token
- GET /confirmed_email/{token}: Confirm user's email address
- POST /request_email: Request a new email confirmation

All endpoints are designed to ensure secure user authentication and
verification processes.
"""

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Register a new user in the system.

    Args:
        user_data (UserCreate): User registration data including email, username, and password.
        background_tasks (BackgroundTasks): Background task for sending confirmation email.
        request (Request): The HTTP request object.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If a user with the same email or username already exists.

    Returns:
        User: The newly created user object.
    """
    user_service = UserService(db)

    email_user = await user_service.get_user_by_email(user_data.email)
    if email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    username_user = await user_service.get_user_by_username(user_data.username)
    if username_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this name already exists.",
        )
    user_data.password = Hash().get_password_hash(user_data.password)
    new_user = await user_service.create_user(user_data)
    background_tasks.add_task(
        send_email, new_user.email, new_user.username, request.base_url
    )
    return new_user


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Authenticate a user and generate an access token.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): User login credentials. Defaults to Depends().
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If login credentials are incorrect or email is not confirmed.

    Returns:
        Token: Access token for authenticated user.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_username(form_data.username)
    if not user or not Hash().verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email address not confirmed",
        )
    access_token = await create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/confirmed_email/{token}")
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """Confirm a user's email address using a verification token.

    Args:
        token (str): Email confirmation token.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If verification fails or user is not found.

    Returns:
        dict: Message indicating email confirmation status.
    """
    user_service = UserService(db)
    email = get_email_from_token(token)
    user = await user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error"
        )
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await user_service.confirmed_email(email)
    return {"message": "Email confirmed"}


@router.post("/request_email")
async def request_email(
    body: RequestEmail,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """Request a new email confirmation for a user.

    Args:
        body (RequestEmail): Email address to send confirmation to.
        background_tasks (BackgroundTasks): Background task for sending confirmation email.
        request (Request): The HTTP request object.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        dict: Message instructing user to check their email.
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_email(body.email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user.confirmed:
        return {"message": "Your email has already been confirmed."}
    background_tasks.add_task(
        send_email, user.email, user.username, request.base_url
    )
    return {"message": "Check your email for confirmation."}