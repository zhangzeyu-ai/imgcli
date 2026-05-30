import os
import glob

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif", ".avif"}


def find_images(input_path, recursive=False):
    if os.path.isfile(input_path):
        ext = os.path.splitext(input_path)[1].lower()
        if ext in SUPPORTED_EXTENSIONS:
            return [input_path]
        return []

    if recursive:
        pattern = os.path.join(input_path, "**", "*")
    else:
        pattern = os.path.join(input_path, "*")

    result = []
    for f in glob.glob(pattern, recursive=recursive):
        if os.path.isfile(f) and os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS:
            result.append(f)
    return sorted(result)


def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)


def output_path(source, output_dir, new_ext=None, suffix=None):
    basename = os.path.basename(source)
    name, ext = os.path.splitext(basename)
    if suffix:
        name = f"{name}{suffix}"
    ext = new_ext if new_ext else ext
    return os.path.join(output_dir, f"{name}{ext}")
