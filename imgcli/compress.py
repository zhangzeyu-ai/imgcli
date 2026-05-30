import os
from PIL import Image


def compress_quality(image_path, output_path, quality):
    img = Image.open(image_path)
    img.save(output_path, quality=quality, optimize=True)


def compress_max_size(image_path, output_path, target_bytes, quality_start=85):
    quality = quality_start
    while quality > 10:
        img = Image.open(image_path)
        img.save(output_path, quality=quality, optimize=True)
        if os.path.getsize(output_path) <= target_bytes:
            return quality
        quality -= 5

    q = quality
    while q > 1:
        img = Image.open(image_path)
        img.save(output_path, quality=q, optimize=True)
        if os.path.getsize(output_path) <= target_bytes:
            return q
        q -= 1
    return q


def compress_max_dimensions(image_path, output_path, max_width, max_height, quality=85):
    img = Image.open(image_path)
    img.thumbnail((max_width, max_height), Image.LANCZOS)
    img.save(output_path, quality=quality, optimize=True)
