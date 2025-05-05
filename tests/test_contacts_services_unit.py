import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.contacts import ContactService
from src.schemas import ContactBase, ContactUpdate
from src.database.models import User


@pytest.fixture
def mock_db():
    """Mock the AsyncSession database."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.commit.return_value = None  # Mock commit behavior
    mock_session.add.return_value = None  # Mock add behavior
    return mock_session



@pytest.fixture
def user():
    """Fixture to create a mock user."""
    return User(id=1, username="testuser", email="testuser@example.com")


@pytest.fixture
def contact_service(mock_db):
    """Fixture to create a ContactService instance."""
    return ContactService(mock_db)


@pytest.mark.asyncio
async def test_create_contact(contact_service, user):
    """Test creating a new contact."""
    # Arrange
    contact_data = ContactBase(
        first_name="John",
        last_name="Doe",
        email="johndoe@example.com",
        phone="123-456-7890"  # Add the missing phone field
    )
    
    # Mock the repository method
    contact_service.contact_repository.create_contact = AsyncMock(return_value={
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "phone": "123-456-7890"
    })
    
    # Act
    result = await contact_service.create_contact(contact_data, user)

    # Assert
    contact_service.contact_repository.create_contact.assert_called_once_with(contact_data, user)
    assert result["first_name"] == "John"
    assert result["last_name"] == "Doe"
    assert result["email"] == "johndoe@example.com"
    assert result["phone"] == "123-456-7890"

@pytest.mark.asyncio
async def test_get_contacts(contact_service, mock_db, user):
    """Test retrieving a list of contacts."""
    # Arrange
    contact_service.contact_repository.get_contacts = AsyncMock(return_value=[{"name": "John Doe", "email": "johndoe@example.com"}])
    
    # Act
    result = await contact_service.get_contacts(skip=0, limit=10, user=user)

    # Assert
    contact_service.contact_repository.get_contacts.assert_called_once_with(0, 10, user)
    assert len(result) == 1
    assert result[0]["name"] == "John Doe"
    assert result[0]["email"] == "johndoe@example.com"


@pytest.mark.asyncio
async def test_get_contact(contact_service, mock_db, user):
    """Test retrieving a specific contact."""
    # Arrange
    contact_service.contact_repository.get_contact_by_id = AsyncMock(return_value={"name": "John Doe", "email": "johndoe@example.com"})
    
    # Act
    result = await contact_service.get_contact(contact_id=1, user=user)

    # Assert
    contact_service.contact_repository.get_contact_by_id.assert_called_once_with(1, user)
    assert result["name"] == "John Doe"
    assert result["email"] == "johndoe@example.com"


@pytest.mark.asyncio
async def test_update_contact(contact_service, mock_db, user):
    """Test updating a contact."""
    # Arrange
    updated_contact_data = ContactUpdate(name="Jane Doe", email="janedoe@example.com")
    contact_service.contact_repository.update_contact = AsyncMock(return_value={"name": "Jane Doe", "email": "janedoe@example.com"})
    
    # Act
    result = await contact_service.update_contact(contact_id=1, body=updated_contact_data, user=user)

    # Assert
    contact_service.contact_repository.update_contact.assert_called_once_with(1, updated_contact_data, user)
    assert result["name"] == "Jane Doe"
    assert result["email"] == "janedoe@example.com"


@pytest.mark.asyncio
async def test_remove_contact(contact_service, mock_db, user):
    """Test removing a contact."""
    # Arrange
    contact_service.contact_repository.remove_contact = AsyncMock(return_value={"message": "Contact removed successfully"})
    
    # Act
    result = await contact_service.remove_contact(contact_id=1, user=user)

    # Assert
    contact_service.contact_repository.remove_contact.assert_called_once_with(1, user)
    assert result["message"] == "Contact removed successfully"


@pytest.mark.asyncio
async def test_get_birthdays(contact_service, mock_db, user):
    """Test retrieving contacts with upcoming birthdays."""
    # Arrange
    contact_service.contact_repository.get_birthdays = AsyncMock(return_value=[{"name": "John Doe", "birthday": "2025-05-05"}])
    
    # Act
    result = await contact_service.get_birthdays(user=user)

    # Assert
    contact_service.contact_repository.get_birthdays.assert_called_once_with(user)
    assert len(result) == 1
    assert result[0]["name"] == "John Doe"
    assert result[0]["birthday"] == "2025-05-05"
