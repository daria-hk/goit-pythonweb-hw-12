from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas import ContactBase, ContactUpdate
from src.database.models import User

class ContactService:
    def __init__(self, db: AsyncSession):
        """
        Initialize the ContactService with a database session.

        Args:
            db (AsyncSession): An asynchronous database session for performing database operations.
        """
        self.contact_repository = ContactRepository(db)

    async def create_contact(self, body: ContactBase, user: User):
        """
        Create a new contact for a specific user.

        Args:
            body (ContactBase): The contact details to be created.
            user (User): The user creating the contact.

        Returns:
            The newly created contact.
        """
        return await self.contact_repository.create_contact(body, user)

    async def get_contacts(self, skip: int, limit: int, user: User):
        """
        Retrieve a paginated list of contacts for a specific user.

        Args:
            skip (int): Number of contacts to skip (for pagination).
            limit (int): Maximum number of contacts to return.
            user (User): The user whose contacts are being retrieved.

        Returns:
            A list of contacts for the user.
        """
        return await self.contact_repository.get_contacts(skip, limit, user)

    async def get_contact(self, contact_id: int, user: User):
        """Retrieve a specific contact by its ID for a given user.

        Args:
            contact_id (int): The unique identifier of the contact.
            user (User): The user who owns the contact.

        Returns:
            The contact with the specified ID.
        """
        return await self.contact_repository.get_contact_by_id(contact_id, user)

    async def update_contact(self, contact_id: int, body: ContactUpdate, user: User):
        """Update an existing contact for a specific user.

        Args:
            contact_id (int): The unique identifier of the contact to update.
            body (ContactUpdate): The updated contact details.
            user (User): The user who owns the contact.

        Returns:
            The updated contact.
        """
        return await self.contact_repository.update_contact(contact_id, body, user)

    async def remove_contact(self, contact_id: int, user: User):
        """Remove a specific contact for a given user.

        Args:
            contact_id (int): The unique identifier of the contact to remove.
            user (User): The user who owns the contact.

        Returns:
            The result of the contact removal operation.
        """
        return await self.contact_repository.remove_contact(contact_id, user)
    
    async def get_birthdays(self, user: User):
        """
        Retrieve contacts with upcoming birthdays for a specific user.

        Args:
            user (User): The user whose contacts' birthdays are being retrieved.

        Returns:
            A list of contacts with upcoming birthdays.
        """
        return await self.contact_repository.get_birthdays(user)