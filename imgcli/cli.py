import os
import click
from . import __version__
from .utils import find_images, ensure_output_dir, output_path
from .compress import compress_quality, compress_max_size, compress_max_dimensions
from .convert import convert_image, FORMAT_MAP
from .watermark import add_text_watermark, add_image_watermark
from .rename import rename_images, rename_images_with_counter, sanitize_filenames


@click.group()
@click.version_option(version=__version__, prog_name="imgcli")
def cli():
    """imgcli - 批处理图片工具"""


def _common_options(fn):
    fn = click.option("--output", "-o", default=None, help="输出目录（默认同目录 _output）")(fn)
    fn = click.option("--recursive", "-r", is_flag=True, help="递归处理子目录")(fn)
    fn = click.option("--dry-run", is_flag=True, help="仅预览，不实际执行")(fn)
    fn = click.argument("input", required=True)(fn)
    return fn


@cli.command()
@click.option("--quality", "-q", default=85, type=int, help="压缩质量 1-100（默认 85）")
@click.option("--max-size", "-s", default=None, type=int, help="目标文件大小（字节），如 500000 = 500KB")
@click.option("--max-width", "-W", default=None, type=int, help="最大宽度（像素）")
@click.option("--max-height", "-H", default=None, type=int, help="最大高度（像素）")
@click.option("--suffix", default="_compressed", help="输出文件名后缀（默认 _compressed）")
@_common_options
def compress(input, output, recursive, dry_run, quality, max_size, max_width, max_height, suffix):
    """压缩图片"""
    files = find_images(input, recursive)
    if not files:
        click.echo("未找到图片文件")
        return

    out_dir = output or os.path.join(
        os.path.dirname(os.path.abspath(input)) if os.path.isfile(input) else os.path.abspath(input),
        "_output"
    )
    ensure_output_dir(out_dir)

    for f in files:
        out = output_path(f, out_dir, suffix=suffix)
        rel = os.path.relpath(f)
        if dry_run:
            click.echo(f"[DRY-RUN] {rel} -> {out}")
            continue

        try:
            size_before = os.path.getsize(f)
            if max_size:
                compress_max_size(f, out, max_size, quality)
            elif max_width or max_height:
                compress_max_dimensions(f, out, max_width or 99999, max_height or 99999, quality)
            else:
                compress_quality(f, out, quality)
            size_after = os.path.getsize(out)
            saved = size_before - size_after
            pct = (saved / size_before) * 100 if size_before > 0 else 0
            click.echo(f"  [OK] {rel}  {_fmt_size(size_before)} -> {_fmt_size(size_after)} (-{pct:.0f}%)")
        except Exception as e:
            click.echo(f"  [FAIL] {rel} 失败: {e}")


@cli.command()
@click.option("--format", "-f", "target_format", required=True,
              type=click.Choice(list(FORMAT_MAP.keys())), help="目标格式")
@click.option("--quality", "-q", default=85, type=int, help="输出质量 1-100")
@click.option("--suffix", default=None, help="输出文件名后缀（默认自动改扩展名）")
@_common_options
def convert(input, output, recursive, dry_run, target_format, quality, suffix):
    """转换图片格式"""
    files = find_images(input, recursive)
    if not files:
        click.echo("未找到图片文件")
        return

    out_dir = output or os.path.join(
        os.path.dirname(os.path.abspath(input)) if os.path.isfile(input) else os.path.abspath(input),
        "_output"
    )
    ensure_output_dir(out_dir)

    for f in files:
        new_ext = f".{target_format}"
        out = output_path(f, out_dir, new_ext=new_ext, suffix=suffix)
        rel = os.path.relpath(f)
        if dry_run:
            click.echo(f"[DRY-RUN] {rel} -> {out}")
            continue

        try:
            convert_image(f, out, FORMAT_MAP[target_format], quality)
            click.echo(f"  [OK] {rel} -> {os.path.basename(out)}")
        except Exception as e:
            click.echo(f"  [FAIL] {rel} 失败: {e}")


@cli.group()
def watermark():
    """添加水印"""


@watermark.command("text")
@click.option("--text", "-t", required=True, help="水印文字")
@click.option("--position", "-p", default="bottom-right",
              type=click.Choice(["top-left", "top-right", "bottom-left", "bottom-right", "center"]),
              help="水印位置")
@click.option("--font-size", "-s", default=36, type=int, help="字号")
@click.option("--opacity", "-a", default=128, type=int, help="透明度 0-255")
@click.option("--color", "-c", default="255,255,255", help="文字颜色 R,G,B")
@click.option("--suffix", default="_watermarked", help="输出文件名后缀")
@_common_options
def watermark_text(input, output, recursive, dry_run, text, position, font_size, opacity, color, suffix):
    """添加文字水印"""
    files = find_images(input, recursive)
    if not files:
        click.echo("未找到图片文件")
        return

    out_dir = output or os.path.join(
        os.path.dirname(os.path.abspath(input)) if os.path.isfile(input) else os.path.abspath(input),
        "_output"
    )
    ensure_output_dir(out_dir)
    color_tuple = tuple(int(c.strip()) for c in color.split(","))

    for f in files:
        out = output_path(f, out_dir, suffix=suffix)
        rel = os.path.relpath(f)
        if dry_run:
            click.echo(f"[DRY-RUN] {rel} -> {out}")
            continue
        try:
            add_text_watermark(f, out, text, position, font_size, opacity, color_tuple)
            click.echo(f"  [OK] {rel}")
        except Exception as e:
            click.echo(f"  [FAIL] {rel} 失败: {e}")


@watermark.command("image")
@click.option("--watermark", "-w", "wm_path", required=True, help="水印图片路径")
@click.option("--position", "-p", default="bottom-right",
              type=click.Choice(["top-left", "top-right", "bottom-left", "bottom-right", "center", "tile"]),
              help="水印位置（tile = 平铺）")
@click.option("--scale", "-s", default=0.2, type=float, help="水印缩放比例 0-1")
@click.option("--opacity", "-a", default=128, type=int, help="透明度 0-255")
@click.option("--suffix", default="_watermarked", help="输出文件名后缀")
@_common_options
def watermark_image(input, output, recursive, dry_run, wm_path, position, scale, opacity, suffix):
    """添加图片水印"""
    files = find_images(input, recursive)
    if not files:
        click.echo("未找到图片文件")
        return

    out_dir = output or os.path.join(
        os.path.dirname(os.path.abspath(input)) if os.path.isfile(input) else os.path.abspath(input),
        "_output"
    )
    ensure_output_dir(out_dir)

    for f in files:
        out = output_path(f, out_dir, suffix=suffix)
        rel = os.path.relpath(f)
        if dry_run:
            click.echo(f"[DRY-RUN] {rel} -> {out}")
            continue
        try:
            add_image_watermark(f, out, wm_path, position, scale, opacity)
            click.echo(f"  [OK] {rel}")
        except Exception as e:
            click.echo(f"  [FAIL] {rel} 失败: {e}")


@cli.group()
def rename():
    """重命名图片"""


@rename.command("pattern")
@click.option("--pattern", "-p", default="image_{n}{ext}",
              help="命名模板，{n}=序号，{ext}=扩展名（默认 image_{n}{ext}）")
@click.option("--start", "-s", default=1, type=int, help="起始序号（默认 1）")
@_common_options
def rename_pattern(input, output, recursive, dry_run, pattern, start):
    """按模板重命名"""
    click.echo("提示: rename 是原地操作，--output 参数无效")
    files = find_images(input, recursive)
    if not files:
        click.echo("未找到图片文件")
        return
    results = rename_images(files, pattern, start, dry_run)
    for src, dst in results:
        click.echo(f"  {'[DRY-RUN]' if dry_run else '[OK]'} {os.path.basename(src)} -> {os.path.basename(dst)}")


@rename.command("counter")
@click.option("--prefix", "-p", default="image", help="文件名前缀（默认 image）")
@click.option("--start", "-s", default=1, type=int, help="起始序号")
@click.option("--padding", "-d", default=3, type=int, help="数字位数（默认 3 => 001）")
@_common_options
def rename_counter(input, output, recursive, dry_run, prefix, start, padding):
    """按计数器重命名（image001.jpg, image002.jpg...）"""
    click.echo("提示: rename 是原地操作，--output 参数无效")
    files = find_images(input, recursive)
    if not files:
        click.echo("未找到图片文件")
        return
    results = rename_images_with_counter(files, prefix, start, padding, dry_run)
    for src, dst in results:
        click.echo(f"  {'[DRY-RUN]' if dry_run else '[OK]'} {os.path.basename(src)} -> {os.path.basename(dst)}")


@rename.command("sanitize")
@_common_options
def rename_sanitize(input, output, recursive, dry_run):
    """清理文件名（特殊字符替换为下划线）"""
    click.echo("提示: rename 是原地操作，--output 参数无效")
    files = find_images(input, recursive)
    if not files:
        click.echo("未找到图片文件")
        return
    results = sanitize_filenames(files, dry_run)
    for src, dst in results:
        if src == dst:
            continue
        click.echo(f"  {'[DRY-RUN]' if dry_run else '[OK]'} {os.path.basename(src)} -> {os.path.basename(dst)}")


@cli.command("info")
@_common_options
def info(input, output, recursive, dry_run):
    """查看图片信息"""
    dry_run = True


def _fmt_size(b):
    if b < 1024:
        return f"{b}B"
    elif b < 1024 * 1024:
        return f"{b / 1024:.1f}KB"
    else:
        return f"{b / 1024 / 1024:.1f}MB"


if __name__ == "__main__":
    cli()
