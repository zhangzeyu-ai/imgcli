from PIL import Image


FORMAT_MAP = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
    "bmp": "BMP",
    "tiff": "TIFF",
    "tif": "TIFF",
    "avif": "AVIF",
}


def convert_image(image_path, output_path, target_format, quality=85):
    img = Image.open(image_path)
    if img.mode == "RGBA" and target_format == "JPEG":
        img = img.convert("RGB")
    save_kwargs = {}
    if target_format in ("JPEG", "WEBP", "AVIF"):
        save_kwargs["quality"] = quality
    if target_format == "AVIF":
        save_kwargs["quality"] = quality
    img.save(output_path, format=target_format, optimize=True, **save_kwargs)
