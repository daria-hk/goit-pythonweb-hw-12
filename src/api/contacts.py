from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.schemas import (
    ContactBase,
    ContactUpdate,
    ContactResponse,
)
from src.services.contacts import ContactService
from src.services.auth import get_current_user

router = APIRouter(prefix="/contacts")

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user),
):
    """Retrieve a list of contacts for the current user.

    Args:
        skip (int, optional): Number of contacts to skip for pagination. Defaults to 0.
        limit (int, optional): Maximum number of contacts to return. Defaults to 100.
        db (AsyncSession): Database session dependency.
        user (User): Currently authenticated user.

    Returns:
        List[ContactResponse]: A list of contact responses.
    """
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(skip, limit, user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    """Retrieve a specific contact by its ID.

    Args:
        contact_id (int): The unique identifier of the contact.
        db (AsyncSession): Database session dependency.
        user (User): Currently authenticated user.

    Returns:
        ContactResponse: The contact details.

    Raises:
        HTTPException: If the contact is not found (404 status).
    """
    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactBase, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    """Create a new contact for the current user.

    Args:
        body (ContactBase): The contact details to create.
        db (AsyncSession): Database session dependency.
        user (User): Currently authenticated user.

    Returns:
        ContactResponse: The created contact details.
    """
    contact_service = ContactService(db)
    return await contact_service.create_contact(body, user)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactUpdate, contact_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    """Update an existing contact for the current user.

    Args:
        body (ContactUpdate): The updated contact details.
        contact_id (int): The unique identifier of the contact to update.
        db (AsyncSession): Database session dependency.
        user (User): Currently authenticated user.

    Returns:
        ContactResponse: The updated contact details.

    Raises:
        HTTPException: If the contact is not found (404 status).
    """
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="contact not found"
        )
    return contact

@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    """Remove a contact for the current user.

    Args:
        contact_id (int): The unique identifier of the contact to remove.
        db (AsyncSession): Database session dependency.
        user (User): Currently authenticated user.

    Returns:
        ContactResponse: The details of the removed contact.

    Raises:
        HTTPException: If the contact is not found (404 status).
    """
    contact_service = ContactService(db)
    contact = await contact_service.remove_contact(contact_id, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="contact not found"
        )
    return contact

@router.get("/birthdays", response_model=List[ContactResponse])
async def get_birthdays(db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    """Retrieve contacts with upcoming birthdays for the current user.

    Args:
        db (AsyncSession): Database session dependency.
        user (User): Currently authenticated user.

    Returns:
        List[ContactResponse]: A list of contacts with upcoming birthdays.
    """
    contact_service = ContactService(db)
    return await contact_service.get_birthdays(user)