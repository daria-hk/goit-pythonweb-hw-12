import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.repository.users import UserRepository
from src.schemas import UserCreate


@pytest.fixture
def mock_session():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    return mock_session


@pytest.fixture
def user_repository(mock_session):
    return UserRepository(mock_session)


@pytest.fixture
def user_create_data():
    return UserCreate(username="testuser", email="testuser@example.com", password="testpassword")


@pytest.fixture
def user():
    return User(id=1, username="testuser", email="testuser@example.com", avatar="avatar_url", hashed_password="hashedpassword", confirmed=False)


@pytest.mark.asyncio
async def test_get_user_by_id(user_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await user_repository.get_user_by_id(user_id=1)

    assert result is not None
    assert result.id == 1
    assert result.username == "testuser"
    assert result.email == "testuser@example.com"


@pytest.mark.asyncio
async def test_get_user_by_username(user_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await user_repository.get_user_by_username(username="testuser")

    assert result is not None
    assert result.username == "testuser"
    assert result.email == "testuser@example.com"


@pytest.mark.asyncio
async def test_get_user_by_email(user_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute = AsyncMock(return_value=mock_result)

    result = await user_repository.get_user_by_email(email="testuser@example.com")

    assert result is not None
    assert result.email == "testuser@example.com"
    assert result.username == "testuser"


@pytest.mark.asyncio
async def test_create_user(user_repository, mock_session, user_create_data):
    # Create a fake user to be returned after refresh
    fake_user = User(
        id=1,
        username=user_create_data.username,
        email=user_create_data.email,
        avatar="avatar_url",
        hashed_password="hashed_password",
        confirmed=False
    )

    # Mock session behavior
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock(side_effect=lambda u: u.__dict__.update(fake_user.__dict__))

    # Call method
    result = await user_repository.create_user(body=user_create_data, avatar="avatar_url")

    # Assertions
    assert result is not None
    assert result.username == "testuser"
    assert result.email == "testuser@example.com"
    assert result.avatar == "avatar_url"
    assert result.confirmed is False

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(result)


@pytest.mark.asyncio
async def test_confirmed_email(user_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute = AsyncMock(return_value=mock_result)

    await user_repository.confirmed_email(email="testuser@example.com")

    assert user.confirmed is True
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_avatar_url(user_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute = AsyncMock(return_value=mock_result)

    updated_user = await user_repository.update_avatar_url(email="testuser@example.com", url="new_avatar_url")

    assert updated_user.avatar == "new_avatar_url"
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(updated_user)
