import cloudinary
import cloudinary
import cloudinary.uploader

from app.core.config import settings


cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)


class CloudinaryService:

    @staticmethod
    async def upload_image(
        file_bytes: bytes,
        filename: str,
        folder: str = "products",
    ) -> dict:
        """
        Upload an image to Cloudinary.
        """

        try:
            result = cloudinary.uploader.upload(
                file_bytes,
                folder=folder,
                public_id=filename.rsplit(".", 1)[0],
                use_filename=True,
                unique_filename=True,
                overwrite=False,
                resource_type="image",
            )

            return {
                "url": result["secure_url"],
                "secure_url": result["secure_url"],
                "public_id": result["public_id"],
                "format": result.get("format"),
            }

        except Exception as exc:
            raise ValueError(
                f"Failed to upload image: {str(exc)}"
            ) from exc

    @staticmethod
    async def delete_image(
        public_id: str,
    ) -> None:
        """
        Delete an image from Cloudinary.
        """

        try:
            result = cloudinary.uploader.destroy(
                public_id,
                resource_type="image",
                invalidate=True,
            )

            if result.get("result") not in {
                "ok",
                "not found",
            }:
                raise ValueError(
                    "Cloudinary image deletion failed."
                )

        except Exception as exc:
            raise ValueError(
                f"Failed to delete image: {str(exc)}"
            ) from exc
