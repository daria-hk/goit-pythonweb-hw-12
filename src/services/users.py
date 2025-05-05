from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.repository.users import UserRepository
from src.schemas import UserCreate


class UserService:
    def __init__(self, db: AsyncSession):
        """Initialize UserService with a database session.

        Args:
            db (AsyncSession): Asynchronous database session for user operations.
        """
        self.repository = UserRepository(db)

    async def create_user(self, body: UserCreate):
        """Create a new user with an optional Gravatar avatar.

        Args:
            body (UserCreate): User creation details including email.

        Returns:
            User: The newly created user with avatar.

        Notes:
            Attempts to generate a Gravatar avatar for the user's email.
            If avatar generation fails, continues with a None avatar.
        """
        avatar = None
        try:
            g = Gravatar(body.email)
            avatar = g.get_image()
        except Exception as e:
            print(e)

        return await self.repository.create_user(body, avatar)

    async def get_user_by_id(self, user_id: int):
        """Retrieve a user by their unique identifier.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            User: The user with the specified ID, or None if not found.
        """
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str):
        """Retrieve a user by their username.

        Args:
            username (str): The username of the user.

        Returns:
            User: The user with the specified username, or None if not found.
        """
        return await self.repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str):
        """Retrieve a user by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            User: The user with the specified email, or None if not found.
        """
        return await self.repository.get_user_by_email(email)
    
    async def confirmed_email(self, email: str):
        """Mark a user's email as confirmed.

        Args:
            email (str): The email address to be confirmed.

        Returns:
            User: The updated user with confirmed email status.
        """
        return await self.repository.confirmed_email(email)

    async def update_avatar_url(self, email: str, url: str):
        """Update the avatar URL for a user.

        Args:
            email (str): The email address of the user.
            url (str): The new avatar URL to be set.

        Returns:
            User: The user with the updated avatar URL.
        """
        return await self.repository.update_avatar_url(email, url)