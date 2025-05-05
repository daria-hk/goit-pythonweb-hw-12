from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import date, datetime

class ContactBase(BaseModel):
    """Base model representing the core information for a contact.

    Attributes:
        first_name (str): First name of the contact, limited to 50 characters.
        last_name (str): Last name of the contact, limited to 50 characters.
        email (EmailStr): Email address of the contact, validated as a valid email format.
        phone (str): Phone number of the contact, limited to 50 characters.
        birthday (date): Date of birth of the contact.
    """
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone: str = Field(max_length=50)
    birthday: date


class ContactUpdate(ContactBase):
    """Model for updating contact information with optional fields.

    Allows partial updates to contact details, with all fields being optional.
    Inherits validation rules from ContactBase.

    Attributes:
        first_name (Optional[str]): Optional updated first name, limited to 50 characters.
        last_name (Optional[str]): Optional updated last name, limited to 50 characters.
        email (Optional[EmailStr]): Optional updated email address.
        phone (Optional[str]): Optional updated phone number, limited to 50 characters.
        birthday (Optional[date]): Optional updated date of birth.
    """
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    birthday: Optional[date] = None

class ContactResponse(ContactBase):
    """Response model for returning contact details, including database-generated fields.

    Extends ContactBase with additional metadata about the contact record.

    Attributes:
        id (int): Unique identifier for the contact.
        first_name (str): First name of the contact.
        last_name (str): Last name of the contact.
        email (str): Email address of the contact.
        phone (str): Phone number of the contact.
        birthday (Optional[date]): Date of birth of the contact.
        created_at (datetime | None): Timestamp of when the contact was created.
        updated_at (Optional[datetime]): Timestamp of the last update to the contact.
    """
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: Optional[date] = None
    created_at: datetime | None
    updated_at: Optional[datetime] | None

    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    """Model representing a user in the system.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): User's chosen username.
        email (str): User's email address.
        avatar (str): URL or path to the user's avatar image.
    """
    id: int
    username: str
    email: str
    avatar: str

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    """Model for creating a new user account.

    Attributes:
        username (str): Desired username for the new user.
        email (str): Email address for the new user.
        password (str): Password for the new user account.
    """
    username: str
    email: str
    password: str

class Token(BaseModel):
    """Model representing an authentication token.

    Attributes:
        access_token (str): The JWT access token for authentication.
        token_type (str): The type of token (typically 'bearer').
    """
    access_token: str
    token_type: str

class RequestEmail(BaseModel):
    """Model for requesting actions related to a specific email address.

    Attributes:
        email (EmailStr): A validated email address.
    """
    email: EmailStr