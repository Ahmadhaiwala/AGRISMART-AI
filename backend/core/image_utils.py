from io import BytesIO
from typing import BinaryIO

import torch
from PIL import Image, UnidentifiedImageError
from torchvision import transforms

from core.config import settings


class ImageProcessor:
    """Image preprocessing and validation for model inference."""

    def __init__(self):
        # IMPORTANT:
        # These transformations must match the validation
        # transformations used during model training.

        self.transform = transforms.Compose([
            transforms.Resize(
                (settings.IMAGE_SIZE, settings.IMAGE_SIZE)
            ),

            transforms.ToTensor(),

            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
        ])

    def preprocess(
        self,
        image_file: BinaryIO
    ) -> torch.Tensor:
        """
        Preprocess an uploaded image for model inference.

        Args:
            image_file: Binary file object containing image data.

        Returns:
            Tensor with shape:
            [1, 3, IMAGE_SIZE, IMAGE_SIZE]
        """

        try:
            # Open image
            image = Image.open(image_file)

            # Convert everything to RGB.
            # This handles grayscale, RGBA, etc.
            image = image.convert("RGB")

            # Apply preprocessing
            image_tensor = self.transform(image)

            # Add batch dimension
            #
            # Before:
            # [3, 224, 224]
            #
            # After:
            # [1, 3, 224, 224]
            image_tensor = image_tensor.unsqueeze(0)

            return image_tensor

        except Exception as e:
            raise ValueError(
                f"Unable to preprocess image: {str(e)}"
            ) from e

    def validate_image(
        self,
        file_data: bytes,
        filename: str
    ) -> tuple[bool, str]:
        """
        Validate an uploaded image.

        Args:
            file_data: Raw image bytes.
            filename: Original filename.

        Returns:
            (is_valid, error_message)
        """

        # --------------------------------
        # 1. Validate file size
        # --------------------------------

        if len(file_data) > settings.MAX_IMAGE_SIZE:

            max_size_mb = (
                settings.MAX_IMAGE_SIZE / (1024 * 1024)
            )

            return (
                False,
                f"File size exceeds maximum of "
                f"{max_size_mb:.1f}MB"
            )

        # --------------------------------
        # 2. Validate file extension
        # --------------------------------

        file_ext = ""

        if "." in filename:
            file_ext = filename.rsplit(
                ".",
                1
            )[1].lower()

        allowed_extensions = {
            ext.lower().lstrip(".")
            for ext in settings.ALLOWED_EXTENSIONS
        }

        if file_ext not in allowed_extensions:

            return (
                False,
                "File type not allowed. "
                f"Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )

        # --------------------------------
        # 3. Validate actual image content
        # --------------------------------

        try:

            image = Image.open(
                BytesIO(file_data)
            )

            # verify() checks that the file is actually
            # a valid image.
            image.verify()

            return True, ""

        except (UnidentifiedImageError, OSError):

            return (
                False,
                "Invalid or corrupted image file."
            )

        except Exception as e:

            return (
                False,
                f"Invalid image file: {str(e)}"
            )


# ----------------------------------------
# Global image processor instance
# ----------------------------------------

image_processor = ImageProcessor()