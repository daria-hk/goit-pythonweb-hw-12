from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas import UserCreate

class UserRepository:
    """
    A repository class for managing user-related database operations.

    This class provides methods for retrieving, creating, and updating user information
    using an asynchronous SQLAlchemy session.

    Attributes:
        db (AsyncSession): An asynchronous database session for executing queries.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the UserRepository with an asynchronous database session.

        Args:
            session (AsyncSession): The database session to be used for queries.
        """
        self.db = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a user by their unique identifier.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            User | None: The user with the specified ID, or None if not found.
        """
        stmt = select(User).filter_by(id=user_id)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Retrieve a user by their username.

        Args:
            username (str): The username of the user.

        Returns:
            User | None: The user with the specified username, or None if not found.
        """
        stmt = select(User).filter_by(username=username)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            User | None: The user with the specified email, or None if not found.
        """
        stmt = select(User).filter_by(email=email)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def create_user(self, body: UserCreate, avatar: str = None) -> User:
        """
        Create a new user in the database.

        Args:
            body (UserCreate): The user creation data model.
            avatar (str, optional): URL or path to the user's avatar image. Defaults to None.

        Returns:
            User: The newly created user object.
        """
        user = User(
            **body.model_dump(exclude_unset=True, exclude={"password"}),
            hashed_password=body.password,
            avatar=avatar
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def confirmed_email(self, email: str) -> None:
        """
        Mark a user's email as confirmed.

        Args:
            email (str): The email address of the user to confirm.
        """
        user = await self.get_user_by_email(email)
        user.confirmed = True
        await self.db.commit()
    
    async def update_avatar_url(self, email: str, url: str) -> User:
        """
        Update the avatar URL for a user.

        Args:
            email (str): The email address of the user.
            url (str): The new avatar URL.

        Returns:
            User: The updated user object.
        """
        user = await self.get_user_by_email(email)
        user.avatar = url
        await self.db.commit()
        await self.db.refresh(user)
        return user