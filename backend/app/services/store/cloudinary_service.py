import cloudinary
import cloudinary.uploader
from app.core.config import settings

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)

class CloudinaryService:
    @staticmethod
    async def upload_image(file_bytes: bytes, filename: str, folder: str = "products") -> dict:
        """
        Upload an image to Cloudinary.
        Returns: dict with 'url', 'public_id', 'secure_url'
        """
        try:
            result = cloudinary.uploader.upload(
                file_bytes,
                folder=folder,
                public_id=filename.split('.')[0],
                use_filename=True,
                unique_filename=True,
                overwrite=False,
            )
            return {
                "url": result["secure_url"],
                "secure_url": result["secure_url"],
                "public_id": result["public_id"],
                "format": result["format"],
            }
        except Exception as e:
            raise ValueError(f"Failed to upload image: {str(e)}")
