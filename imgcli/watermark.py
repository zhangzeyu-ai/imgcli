from PIL import Image, ImageDraw, ImageFont


def _get_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except (IOError, OSError):
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except (IOError, OSError):
            return ImageFont.load_default()


def add_text_watermark(image_path, output_path, text, position="bottom-right",
                       font_size=36, opacity=128, color=(255, 255, 255)):
    img = Image.open(image_path).convert("RGBA")
    txt_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_layer)
    font = _get_font(font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]

    positions = {
        "top-left": (10, 10),
        "top-right": (img.width - tw - 10, 10),
        "bottom-left": (10, img.height - th - 10),
        "bottom-right": (img.width - tw - 10, img.height - th - 10),
        "center": ((img.width - tw) // 2, (img.height - th) // 2),
    }
    x, y = positions.get(position, positions["bottom-right"])
    draw.text((x, y), text, font=font, fill=(*color, opacity))
    result = Image.alpha_composite(img, txt_layer)
    result.convert("RGB").save(output_path, optimize=True)


def add_image_watermark(image_path, output_path, watermark_path, position="bottom-right",
                        scale=0.2, opacity=128):
    img = Image.open(image_path).convert("RGBA")
    wm = Image.open(watermark_path).convert("RGBA")

    wm_width = int(img.width * scale)
    wm_height = int(wm.height * (wm_width / wm.width))
    wm = wm.resize((wm_width, wm_height), Image.LANCZOS)

    if opacity < 255:
        wm.putalpha(wm.split()[3].point(lambda x: min(x, opacity)))

    positions = {
        "top-left": (10, 10),
        "top-right": (img.width - wm_width - 10, 10),
        "bottom-left": (10, img.height - wm_height - 10),
        "bottom-right": (img.width - wm_width - 10, img.height - wm_height - 10),
        "center": ((img.width - wm_width) // 2, (img.height - wm_height) // 2),
        "tile": (0, 0),
    }

    if position == "tile":
        result = Image.new("RGBA", img.size, (0, 0, 0, 0))
        for y in range(0, img.height, wm_height):
            for x in range(0, img.width, wm_width):
                result.paste(wm, (x, y), wm)
    else:
        x, y = positions.get(position, positions["bottom-right"])
        result = Image.new("RGBA", img.size, (0, 0, 0, 0))
        result.paste(wm, (x, y), wm)

    result = Image.alpha_composite(img, result)
    result.convert("RGB").save(output_path, optimize=True)
