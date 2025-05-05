import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO
from src.services.upload_file import UploadFileService


@pytest.mark.asyncio
@patch("cloudinary.uploader.upload")
@patch("cloudinary.CloudinaryImage.build_url")
async def test_upload_file(mock_build_url, mock_upload):
    """Test for uploading a file to Cloudinary and generating a URL."""

    # Arrange: Mock responses for cloudinary methods
    mock_upload.return_value = {
        "version": "sample_version",
        "public_id": "RestApp/testuser"
    }
    
    mock_build_url.return_value = "http://res.cloudinary.com/demo/image/upload/v1234567/sample_version.jpg"

    # Create a mock file object
    mock_file = MagicMock()
    mock_file.file = BytesIO(b"fakefilecontent")  # Mock the file content

    # Initialize the UploadFileService
    upload_service = UploadFileService(
        cloud_name="demo_cloud", 
        api_key="demo_api_key", 
        api_secret="demo_api_secret"
    )

    # Act: Call the upload_file method
    result_url = upload_service.upload_file(mock_file, "testuser")

    # Assert: Verify the correct upload URL is returned
    assert result_url == "http://res.cloudinary.com/demo/image/upload/v1234567/sample_version.jpg"
    
    # Assert: Ensure upload was called with the correct arguments
    mock_upload.assert_called_once_with(mock_file.file, public_id="RestApp/testuser", overwrite=True)

    # Assert: Ensure build_url was called with the correct parameters
    mock_build_url.assert_called_once_with(width=250, height=250, crop="fill", version="sample_version")


@pytest.mark.asyncio
@patch("cloudinary.uploader.upload")
@patch("cloudinary.CloudinaryImage.build_url")
async def test_upload_file_failure(mock_build_url, mock_upload):
    """Test for upload failure (e.g., Cloudinary upload error)."""

    # Arrange: Simulate a failure by having upload raise an exception
    mock_upload.side_effect = Exception("Upload failed")

    # Create a mock file object
    mock_file = MagicMock()
    mock_file.file = BytesIO(b"fakefilecontent")  # Mock the file content

    # Initialize the UploadFileService
    upload_service = UploadFileService(
        cloud_name="demo_cloud", 
        api_key="demo_api_key", 
        api_secret="demo_api_secret"
    )

    # Act & Assert: Ensure that an exception is raised when upload fails
    with pytest.raises(Exception, match="Upload failed"):
        upload_service.upload_file(mock_file, "testuser")
