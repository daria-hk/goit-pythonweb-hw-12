import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import User, Contact
from src.repository.contacts import ContactRepository
from src.schemas import ContactBase, ContactUpdate
from src.services.contacts import ContactService  # Assuming it's located here


@pytest.fixture
def mock_session():
    mock_session = AsyncMock(spec=AsyncSession)
    return mock_session


@pytest.fixture
def contact_repository(mock_session):
    return ContactRepository(mock_session)


@pytest.fixture
def contact_service(contact_repository):
    return ContactService(contact_repository)  # Use the contact_repository fixture


@pytest.fixture
def user():
    return User(id=1, username="testuser", email="testuser@example.com", avatar="avatar_url")


@pytest.mark.asyncio
async def test_get_contacts(contact_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        Contact(id=1, first_name="John", last_name="Doe", email="john@example.com", phone="123456789", birthday=None, user=user)
    ]
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    contacts = await contact_repository.get_contacts(skip=0, limit=10, user=user)

    # Assertions
    assert len(contacts) == 1
    assert contacts[0].first_name == "John"
    assert contacts[0].last_name == "Doe"
    assert contacts[0].email == "john@example.com"
    assert contacts[0].phone == "123456789"


@pytest.mark.asyncio
async def test_get_contact_by_id(contact_repository, mock_session, user):
    # Setup
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = Contact(
        id=1, first_name="John", last_name="Doe", email="john@example.com", phone="123456789", birthday=None, user=user
    )
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    contact = await contact_repository.get_contact_by_id(contact_id=1, user=user)

    # Assertions
    assert contact is not None
    assert contact.id == 1
    assert contact.first_name == "John"
    assert contact.last_name == "Doe"
    assert contact.email == "john@example.com"


@pytest.mark.asyncio
async def test_create_contact(contact_service, user):
    """Test creating a new contact."""
    # Arrange
    contact_data = ContactBase(
        first_name="John",
        last_name="Doe",
        email="johndoe@example.com",
        phone="123-456-7890"
    )
    # Mock the repository's method to return the contact data
    contact_service.contact_repository.create_contact = AsyncMock(return_value=Contact(id=1, **contact_data.dict(), user=user))
    
    # Act
    result = await contact_service.create_contact(contact_data, user)

    # Assert
    contact_service.contact_repository.create_contact.assert_called_once_with(contact_data, user)
    assert result.first_name == "John"
    assert result.last_name == "Doe"
    assert result.email == "johndoe@example.com"
    assert result.phone == "123-456-7890"


@pytest.mark.asyncio
async def test_remove_contact(contact_repository, mock_session, user):
    # Setup
    existing_contact = Contact(
        id=1, first_name="John", last_name="Doe", email="john@example.com", phone="123456789", birthday=None, user=user
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_contact
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await contact_repository.remove_contact(contact_id=1, user=user)

    # Assertions
    assert result is not None
    assert result.first_name == "John"
    assert result.last_name == "Doe"
    mock_session.delete.assert_awaited_once_with(existing_contact)
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_contact(contact_repository, mock_session, user):
    # Setup
    contact_data = ContactUpdate(
        first_name="John", last_name="Smith", email="john.smith@example.com", phone="555123456", birthday=None
    )
    existing_contact = Contact(
        id=1, first_name="John", last_name="Doe", email="john@example.com", phone="123456789", birthday=None, user=user
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_contact
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await contact_repository.update_contact(contact_id=1, body=contact_data, user=user)

    # Assertions
    assert result is not None
    assert result.first_name == "John"
    assert result.last_name == "Smith"
    assert result.email == "john.smith@example.com"
    assert result.phone == "555123456"
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(existing_contact)
