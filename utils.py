from itertools import zip_longest
import math
import os
import typing
from PIL import Image
from rich.console import Console
from rich.progress import track
from ls11 import ls11_decode, LS11_MAGIC

console = Console()

BGCOLOR = (55, 55, 55)

BIG_ENDIAN = 'big'
LITTLE_ENDIAN = 'little'
DEFAULT_ENDIAN = LITTLE_ENDIAN


def color_codes_to_palette(color_codes):
    # ['#FF0000', '#00FF00', '#0000FF'] --> ((255, 0, 0), (0, 255, 0), (0, 0, 255))
    return [(int(x[1:3], base=16), int(x[3:5], base=16), int(x[5:7], base=16)) for x in color_codes]


def grouper(iterable, n, incomplete='fill', fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == 'fill':
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == 'ignore':
        return zip(*args)
    else:
        raise ValueError('Expected fill, strict, or ignore')


def to_2bpp_indexes(data: bytes):
    indexes = []
    for g in grouper(data, 2, incomplete='ignore'):
        for i in range(7, -1, -1):
            n = (((g[0] >> i) & 1) << 1) | \
                ((g[1] >> i) & 1)
            indexes.append(n)
    return indexes


def to_3bpp_indexes(data: bytes):
    indexes = []
    for g in grouper(data, 3, incomplete='ignore'):
        for i in range(7, -1, -1):
            n = (((g[0] >> i) & 1) << 2) | \
                (((g[1] >> i) & 1) << 1) | \
                ((g[2] >> i) & 1)
            indexes.append(n)
    return indexes


def to_4bpp_indexes(data: bytes):
    indexes = []
    for g in grouper(data, 4, incomplete='ignore'):
        for i in range(7, -1, -1):
            n = (((g[0] >> i) & 1) << 3) | \
                (((g[1] >> i) & 1) << 2) | \
                (((g[2] >> i) & 1) << 1) | \
                ((g[3] >> i) & 1)
            indexes.append(n)
    return indexes


def to_color_indexes(data: bytes, num_colors: int):
    if num_colors == 4:
        return to_2bpp_indexes(data)
    if num_colors == 8:
        return to_3bpp_indexes(data)
    if num_colors == 16:
        return to_4bpp_indexes(data)
    if num_colors == 64 or num_colors == 256:
        # do nothing, origin raw data is just the color indexes
        return data
    raise ValueError('Expected 4, 8, 16, 64 or 256 colors in palette.')


def data_to_image(data: bytes, w: int, h: int, palette: list, hh=False) -> Image.Image:
    """
    Convert binary bytes to image.

    :param data:        binary bytes
    :param w:           width
    :param h:           height
    :param palette:     color table
    :param hh:          data contains only half height of size
    :return:            PIL.Image
    """
    image = Image.new('RGB', (w, h), BGCOLOR)
    color_indexes = to_color_indexes(data, len(palette))
    for px_index, color_index in enumerate(color_indexes):
        x, y = px_index % w, px_index // w
        c = palette[color_index]
        if hh:
            image.putpixel((x, 2*y), c)
            image.putpixel((x, 2*y+1), c)
        else:
            image.putpixel((x, y), c)
    return image


def load_images(data: bytes, w: int, h: int, palette: list, hh: bool, part_size: int, num_part: int) -> list[Image.Image]:
    images = []
    for i in track(range(num_part), description="Loding...   "):
        pos = i*part_size
        img = data_to_image(data[pos:pos+part_size], w, h, palette, hh)
        images.append(img)
    return images


def save_index_image(images: list[Image.Image], w: int, h: int, num_col: int, filename: str) -> None:
    # index image
    if w > 96:
        console.log(':exclamation: Single image too large to generate index image.', style='yellow')
        return
    img_w = w * num_col
    img_h = h * math.ceil(len(images) / num_col)
    index_image = Image.new('RGB', (img_w, img_h), color=BGCOLOR)
    for idx, img in track(enumerate(images), description="Saving index", total=len(images)):
        pos_x = (idx % num_col) * w
        pos_y = (idx // num_col) * h
        index_image.paste(img, (pos_x, pos_y))
    index_image.save(filename)


def save_single_images(images: dict[str, Image.Image], out_dir: str, prefix: str) -> None:
    for key in track(images, description='Saving...   ', total=len(images)):
        out_filename = '{}/{}{:0>4}.png'.format(out_dir, prefix, key)
        images[key].save(out_filename)


def calc_part_size(w: int, h: int, num_colors: int, hh=False) -> int:
    """
    計算單一張頭像所佔用的 raw data 大小
    """
    bpp: int  # bits per pixel
    if num_colors == 4:
        bpp = 2
    elif num_colors == 8:
        bpp = 3
    elif num_colors == 16:
        bpp = 4
    else:
        # default 1 byte per color in palette mode (indexed-color)
        # when color-used more than 256, true-color mode instead (3 or 4 bytes per pixel)
        bpp = 8

    return int(w * h * bpp / 8 / 2) if hh else int(w * h * bpp / 8)


# output_images take a map or a list of Image.Image, save them to out_dir with prefix
def output_images(images: typing.Union[list[Image.Image], dict[str, Image.Image]],
                  out_dir: str, prefix: str,
                  w: typing.Optional[int] = None, h: typing.Optional[int] = None) -> None:
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # zip images with index if it's a list
    images = {str(i): img for i, img in enumerate(images)} if isinstance(images, list) else images
    image_list = list(images.values())

    if w is None or h is None:
        w, h = image_list[0].width, image_list[0].height

    # index image
    out_filename = '{}/{}00-INDEX.png'.format(out_dir, prefix)
    save_index_image(image_list, w, h, 16, out_filename)

    # single images
    save_single_images(images, out_dir, prefix)


def extract_images(filename: str, w: int, h: int, palette: list, out_dir: str, prefix: str, part_size=-1, num_part=-1, hh=False, data_loader=None) -> None:
    """
    A basic scaffold of loading file, save index and save single images.
    """

    # get raw data (binary) of images
    raw_data: bytes
    if data_loader:
        raw_data = data_loader()
    else:
        with open(filename, 'rb') as f:
            header = f.read(4)
            f.seek(0)
            if header in LS11_MAGIC:
                raw_data = ls11_decode(f.read())
            else:
                raw_data = f.read()

    if part_size == -1:
        part_size = calc_part_size(w, h, len(palette), hh)

    if num_part == -1:
        num_part = len(raw_data) // part_size

    # load each single images from raw data
    images = load_images(raw_data, w, h, palette, hh, part_size, num_part)

    output_images(images, out_dir, prefix)
