from itertools import zip_longest
import math
from PIL import Image
from rich.progress import track

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


def load_images(data: bytes, w: int, h: int, palette: list, part_size: int, num_face: int) -> list[Image.Image]:
    images = []
    for i in track(range(num_face), description="Loding...       "):
        pos = i*part_size
        img = data_to_image(data[pos:pos+part_size], w, h, palette)
        images.append(img)
    return images


def save_index_image(images: list[Image.Image], w: int, h: int, num_col: int, filename: str) -> None:
    # index image
    # TODO(yuxioz): return when too large in width or too many in num_col
    img_w = w * num_col
    img_h = h * math.ceil(len(images) / num_col)
    index_image = Image.new('RGB', (img_w, img_h), color=BGCOLOR)
    for idx, img in enumerate(images):
        pos_x = (idx % num_col) * w
        pos_y = (idx // num_col) * h
        index_image.paste(img, (pos_x, pos_y))
    index_image.save(filename)
