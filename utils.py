from itertools import zip_longest
from PIL import Image
BGCOLOR = (55, 55, 55)

BIG_ENDIAN = 'big'
LITTLE_ENDIAN = 'little'
DEFAULT_ENDIAN = LITTLE_ENDIAN


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
    elif num_colors == 8:
        return to_3bpp_indexes(data)
    elif num_colors == 16:
        return to_4bpp_indexes(data)
    else:
        raise ValueError('Expected 4, 8, or 16 colors')


def data_to_image(data: bytes, w: int, h: int, colors: list, hh=False) -> Image.Image:
    """
    Convert binary bytes to image.

    :param data:    binary bytes
    :param w:       width
    :param h:       height
    :param colors:  color table
    :param hh:      data contains only half height of size
    :return:        PIL.Image
    """
    img = Image.new('RGB', (w, h), BGCOLOR)
    color_indexes = to_color_indexes(data, len(colors))
    for px_index, color_index in enumerate(color_indexes):
        x, y = px_index % w, px_index // w
        c = colors[color_index]
        if hh:
            img.putpixel((x, 2*y), c)
            img.putpixel((x, 2*y+1), c)
        else:
            img.putpixel((x, y), c)
    return img
