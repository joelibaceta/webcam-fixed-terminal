from typing import Optional
from PIL import Image
import shutil


def image_to_ascii_art(img: Image.Image, rows: int = 0) -> str:
    """Convert an Image to ASCII Art"""

    width, height = img.size
    aspect_ratio = height / width
    new_width = rows
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))

    pixels = img.getdata()

    chars = ["*", "S", "#", "&", "@", "$", "%", "*", "!", ":", "."]
    new_pixels = [chars[pixel // 25] for pixel in pixels]
    new_pixels = "".join(new_pixels)

    new_pixels_count = len(new_pixels)
    ascii_image = [
        new_pixels[index : index + new_width]
        for index in range(0, new_pixels_count, new_width)
    ]
    ascii_image = "\n".join(ascii_image)

    return ascii_image
