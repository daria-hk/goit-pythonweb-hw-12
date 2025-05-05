import cloudinary
import cloudinary.uploader


class UploadFileService:
    """A service class for handling file uploads to Cloudinary cloud storage.

    This class provides methods to configure and upload files to Cloudinary,
    specifically designed for user avatar uploads in a REST application.

    Attributes:
        cloud_name (str): The name of the Cloudinary cloud.
        api_key (str): The API key for Cloudinary authentication.
        api_secret (str): The API secret for Cloudinary authentication.
    """

    def __init__(self, cloud_name, api_key, api_secret):
        """Initialize the Cloudinary configuration for file uploads.

        Args:
            cloud_name (str): The name of the Cloudinary cloud.
            api_key (str): The API key for Cloudinary authentication.
            api_secret (str): The API secret for Cloudinary authentication.
        """
        self.cloud_name = cloud_name
        self.api_key = api_key
        self.api_secret = api_secret
        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret,
            secure=True,
        )

    @staticmethod
    def upload_file(file, username) -> str:
        """Upload a file to Cloudinary and generate a resized avatar URL.

        This method uploads a file to Cloudinary with a specific public ID based on the username,
        and generates a 250x250 pixel avatar URL with a fill crop.

        Args:
            file (UploadFile): The file to be uploaded, typically from a FastAPI request.
            username (str): The username to be used in the public ID of the uploaded file.

        Returns:
            str: The URL of the uploaded and resized avatar image.
        """
        public_id = f"RestApp/{username}"
        r = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
        src_url = cloudinary.CloudinaryImage(public_id).build_url(
            width=250, height=250, crop="fill", version=r.get("version")
        )
        return src_url