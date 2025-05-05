import pytest
from unittest.mock import AsyncMock, patch, ANY
from src.services.email import send_email
from fastapi_mail.errors import ConnectionErrors
from src.services.auth import create_email_token


@pytest.mark.asyncio
@patch("src.services.email.FastMail")
@patch("src.services.email.create_email_token")
async def test_send_email(mock_create_email_token, mock_FastMail):
    """Test for send_email function."""
    # Arrange: Mock the token creation
    mock_create_email_token.return_value = "fake-token"
    
    # Mock FastMail's send_message method
    mock_send_message = AsyncMock()
    mock_FastMail.return_value.send_message = mock_send_message
    
    email = "testuser@example.com"  # Use a plain string for email
    username = "testuser"
    host = "http://example.com"
    
    # Act: Call the send_email function
    await send_email(email=email, username=username, host=host)
    
    # Assert: Ensure the email token is created
    mock_create_email_token.assert_called_once_with({"sub": email})
    
    # Assert: Ensure FastMail's send_message is called
    mock_send_message.assert_called_once_with(
        ANY,  # Use `ANY` from `unittest.mock` to accept any argument
        template_name="verify_email.html",
    )

    # Assert: Check if the email is being sent with correct parameters
    message = mock_send_message.call_args[0][0]
    assert message.subject == "Confirm your email"
    assert message.recipients == [email]
    assert message.template_body["host"] == host
    assert message.template_body["username"] == username
    assert message.template_body["token"] == "fake-token"


@pytest.mark.asyncio
@patch("src.services.email.FastMail")
@patch("src.services.email.create_email_token")
async def test_send_email_connection_error(mock_create_email_token, mock_FastMail):
    """Test send_email function handling connection errors."""
    # Arrange: Mock the token creation
    mock_create_email_token.return_value = "fake-token"
    
    # Simulate a connection error
    mock_FastMail.side_effect = ConnectionErrors("Failed to connect to mail server")
    
    email = "testuser@example.com"  # Use a plain string for email
    username = "testuser"
    host = "http://example.com"
    
    # Act: Call the send_email function and assert that it doesn't raise an exception
    await send_email(email=email, username=username, host=host)
    
    # Assert: Check if the exception was handled and printed
    mock_FastMail.assert_called_once()
    # You can also check if ConnectionErrors was logged (in this case, you'd likely want a logger to capture it)
    # For example, you can mock the `print` function to check if the error was printed.
