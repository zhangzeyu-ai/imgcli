import os
import re


def rename_images(images, pattern, start=1, dry_run=False):
    results = []
    for i, src in enumerate(images):
        ext = os.path.splitext(src)[1].lower()
        new_name = pattern.replace("{n}", str(start + i)).replace("{ext}", ext)
        dirname = os.path.dirname(src)
        dst = os.path.join(dirname, new_name)

        if not dry_run:
            os.rename(src, dst)

        results.append((src, dst))
    return results


def rename_images_with_counter(images, prefix="image", start=1, padding=3, dry_run=False):
    results = []
    for i, src in enumerate(images):
        ext = os.path.splitext(src)[1].lower()
        num = str(start + i).zfill(padding)
        new_name = f"{prefix}{num}{ext}"
        dirname = os.path.dirname(src)
        dst = os.path.join(dirname, new_name)

        if not dry_run:
            os.rename(src, dst)

        results.append((src, dst))
    return results


def sanitize_filenames(images, dry_run=False):
    results = []
    for src in images:
        dirname = os.path.dirname(src)
        name, ext = os.path.splitext(os.path.basename(src))
        clean = re.sub(r"[^\w\-_]", "_", name)
        clean = re.sub(r"_+", "_", clean).strip("_")
        dst = os.path.join(dirname, f"{clean}{ext}")

        if src == dst:
            results.append((src, src))
            continue

        if not dry_run:
            os.rename(src, dst)
        results.append((src, dst))
    return results
