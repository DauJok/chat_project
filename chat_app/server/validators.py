import os

from django.core.exceptions import ValidationError
from PIL import Image

MAX_ICON_HEIGHT, MAX_ICON_WIDTH = 70, 70
ALLOWED_IMAGE_EXTENTIONS = [".jpeg", ".jpg", ".png", ".svg", ".gif", ".tiff", ".tif"]


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > MAX_ICON_WIDTH or img.height > MAX_ICON_HEIGHT:
                raise ValidationError(
                    f"The maximum allowed dimmensions for the image are {MAX_WIDTH}x{MAX_HEIGHT} - size of your image is: {img.size}"
                )


def validate_image_file_extension(image):
    extension = os.path.splitext(image.name)[1]
    if not extension in ALLOWED_IMAGE_EXTENTIONS:
        raise ValidationError(f"Unsupported image file extension")
