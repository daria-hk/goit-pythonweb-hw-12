from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from datetime import date, timedelta

from src.database.models import Contact, User
from src.schemas import ContactBase, ContactUpdate


class ContactRepository:
    """A repository class for managing contact-related database operations.

    This class provides asynchronous methods for CRUD operations on contacts,
    with support for filtering, searching, and user-specific access.

    Attributes:
        db (AsyncSession): An asynchronous SQLAlchemy database session.
    """
    def __init__(self, session: AsyncSession):
        """Initialize the ContactRepository with an async database session.

        Args:
            session (AsyncSession): The asynchronous database session to be used for operations.
        """
        self.db = session

    async def get_contacts(self, skip: int, limit: int, user: User, query: str | None = None) -> List[Contact]:
        """Retrieve a list of contacts for a specific user with optional filtering.

        Args:
            skip (int): Number of contacts to skip for pagination.
            limit (int): Maximum number of contacts to return.
            user (User): The user whose contacts are being retrieved.
            query (str, optional): A search query to filter contacts by first name, last name, or email.

        Returns:
            List[Contact]: A list of contacts matching the search criteria.
        """
        stmt = (
            select(Contact)
            .filter_by(user=user)
            .offset(skip)
            .limit(limit)
        )

        if query:
            stmt = stmt.where(
                (Contact.first_name.ilike(f"%{query}%"))
                | (Contact.last_name.ilike(f"%{query}%"))
                | (Contact.email.ilike(f"%{query}%"))
            )

        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int, user: User) -> Contact | None:
        """Retrieve a specific contact by its ID for a given user.

        Args:
            contact_id (int): The unique identifier of the contact.
            user (User): The user who owns the contact.

        Returns:
            Contact | None: The contact if found, otherwise None.
        """
        stmt = select(Contact).filter_by(id=contact_id, user=user)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactBase, user: User) -> Contact:
        """Create a new contact for a specific user.

        Args:
            body (ContactBase): The contact details to be created.
            user (User): The user creating the contact.

        Returns:
            Contact: The newly created contact, retrieved to ensure all fields are populated.
        """
        contact = Contact(**body.dict(exclude_unset=True), user=user)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return await self.get_contact_by_id(contact.id, user)

    async def remove_contact(self, contact_id: int, user: User) -> Contact | None:
        """Remove a contact by its ID for a specific user.

        Args:
            contact_id (int): The unique identifier of the contact to be removed.
            user (User): The user who owns the contact.

        Returns:
            Contact | None: The removed contact if it existed, otherwise None.
        """
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def update_contact(self, contact_id: int, body: ContactUpdate, user: User) -> Contact | None:
        """Update an existing contact for a specific user.

        Args:
            contact_id (int): The unique identifier of the contact to be updated.
            body (ContactUpdate): The updated contact details.
            user (User): The user who owns the contact.

        Returns:
            Contact | None: The updated contact if it existed, otherwise None.
        """
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            for key, value in body.dict(exclude_unset=True).items():
                setattr(contact, key, value)

            await self.db.commit()
            await self.db.refresh(contact)

        return contact

    async def get_birthdays(self, user: User) -> List[Contact]:
        """Retrieve contacts with birthdays within the next 7 days for a specific user.

        Args:
            user (User): The user whose contacts' birthdays are being retrieved.

        Returns:
            List[Contact]: A list of contacts with birthdays in the next 7 days.
        """
        today = date.today()
        next_seven_days = today + timedelta(days=7)
        stmt = (
            select(Contact)
            .filter_by(user=user)
            .where(Contact.birthday >= today, Contact.birthday <= next_seven_days)
        )
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()