import pytest
from unittest.mock import patch, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession 
from src.services.users import UserService
from src.schemas import UserCreate

# Mock data for User creation
user_data = {
    "email": "testuser@example.com",
    "username": "testuser",
    "password": "securepassword123"
}

@pytest.fixture
def mock_db():
    """Mock the AsyncSession database."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.commit.return_value = None
    mock_session.add.return_value = None
    return mock_session

@pytest.fixture
def user_service(mock_db):
    """Fixture to initialize UserService with mocked DB."""
    return UserService(db=mock_db)

# ---------------- Test Cases ---------------- #

@pytest.mark.asyncio
@patch("src.services.users.Gravatar")
async def test_create_user_without_avatar_gravatar_failure(mock_gravatar_class, user_service):
    """Test creating a user without an avatar if Gravatar fails."""
    # Simulate Gravatar throwing an exception
    mock_gravatar_instance = mock_gravatar_class.return_value
    mock_gravatar_instance.get_image.side_effect = Exception("Gravatar failed")

    # Mock DB repo response
    user_service.repository.create_user = AsyncMock(return_value={
        "email": user_data["email"],
        "avatar": None
    })

    user_create = UserCreate(**user_data)
    created_user = await user_service.create_user(user_create)

    assert created_user["email"] == user_data["email"]
    assert created_user["avatar"] is None

@pytest.mark.asyncio
@patch("src.services.users.Gravatar")
async def test_create_user_with_gravatar_avatar(mock_gravatar_class, user_service):
    """Test creating a user and assigning Gravatar avatar."""
    avatar_url = "https://www.gravatar.com/avatar/12345"
    mock_gravatar_instance = mock_gravatar_class.return_value
    mock_gravatar_instance.get_image.return_value = avatar_url

    user_service.repository.create_user = AsyncMock(return_value={
        "email": user_data["email"],
        "avatar": avatar_url
    })

    user_create = UserCreate(**user_data)
    created_user = await user_service.create_user(user_create)

    assert created_user["email"] == user_data["email"]
    assert created_user["avatar"] == avatar_url

@pytest.mark.asyncio
async def test_get_user_by_id(user_service):
    user_id = 1
    expected_user = {"id": user_id, "email": user_data["email"], "username": user_data["username"]}
    user_service.repository.get_user_by_id = AsyncMock(return_value=expected_user)

    user = await user_service.get_user_by_id(user_id)
    assert user["id"] == user_id
    assert user["email"] == user_data["email"]
    assert user["username"] == user_data["username"]

@pytest.mark.asyncio
async def test_get_user_by_username(user_service):
    expected_user = {"id": 1, "email": user_data["email"], "username": user_data["username"]}
    user_service.repository.get_user_by_username = AsyncMock(return_value=expected_user)

    user = await user_service.get_user_by_username(user_data["username"])
    assert user["username"] == user_data["username"]
    assert user["email"] == user_data["email"]

@pytest.mark.asyncio
async def test_get_user_by_email(user_service):
    expected_user = {"id": 1, "email": user_data["email"], "username": user_data["username"]}
    user_service.repository.get_user_by_email = AsyncMock(return_value=expected_user)

    user = await user_service.get_user_by_email(user_data["email"])
    assert user["email"] == user_data["email"]
    assert user["username"] == user_data["username"]

@pytest.mark.asyncio
async def test_confirm_email(user_service):
    expected_user = {"id": 1, "email": user_data["email"], "username": user_data["username"], "confirmed": True}
    user_service.repository.confirmed_email = AsyncMock(return_value=expected_user)

    user = await user_service.confirmed_email(user_data["email"])
    assert user["email"] == user_data["email"]
    assert user["confirmed"] is True

@pytest.mark.asyncio
async def test_update_avatar_url(user_service):
    new_avatar_url = "https://www.newgravatar.com/avatar/12345"
    expected_user = {"email": user_data["email"], "avatar": new_avatar_url}
    user_service.repository.update_avatar_url = AsyncMock(return_value=expected_user)

    user = await user_service.update_avatar_url(user_data["email"], new_avatar_url)
    assert user["email"] == user_data["email"]
    assert user["avatar"] == new_avatar_url
