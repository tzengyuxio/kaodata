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


def to_2bpp_indexes(data: bytes) -> list[int]:
    indexes = []
    for g in grouper(data, 2, incomplete='ignore'):
        indexes.extend([
            (((g[0] >> i) & 1) << 1) |
            ((g[1] >> i) & 1)
            for i in range(7, -1, -1)
        ])
    return indexes


def to_3bpp_indexes(data: bytes) -> list[int]:
    indexes = []
    for g in grouper(data, 3, incomplete='ignore'):
        indexes.extend([
            (((g[0] >> i) & 1) << 2) |
            (((g[1] >> i) & 1) << 1) |
            ((g[2] >> i) & 1)
            for i in range(7, -1, -1)
        ])
    return indexes


def to_4bpp_indexes(data: bytes) -> list[int]:
    indexes = []
    for g in grouper(data, 4, incomplete='ignore'):
        indexes.extend([
            (((g[0] >> i) & 1) << 3) |
            (((g[1] >> i) & 1) << 2) |
            (((g[2] >> i) & 1) << 1) |
            ((g[3] >> i) & 1)
            for i in range(7, -1, -1)
        ])
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

    # output image info
    console.log(':white_check_mark: {} images saved to {}.'.format(len(images), out_dir), style='green')


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


def create_floppy_image_loader(filename: str, offset_infos: list[tuple[int, int]]) -> typing.Callable[[], bytes]:
    """
    Create a data loader for floppy image.
    """
    def loader():
        raw_data = bytearray()
        with open(filename, 'rb') as f:
            for offset, size in offset_infos:
                f.seek(offset)
                raw_data.extend(f.read(size))
        return bytes(raw_data)
    return loader


def order_of_big5(c: typing.Union[bytes, int]) -> int:
    """
    Return the order of a big5 character.

    0-base, start from '一' (0xA440)
    """
    if isinstance(c, int):
        c = c.to_bytes(2, 'big')

    if len(c) != 2:
        return -1

    hi, lo = c[0], c[1]
    offset: int
    hi_base: int
    if 0xa4 <= hi and hi <= 0xc6:
        offset, hi_base = 0, 0xa4
    elif 0xc9 <= hi and hi <= 0xf9:
        offset, hi_base = 5401, 0xc9
    else:
        return -1

    if 0x40 <= lo and lo <= 0x7e:
        return offset + (hi - hi_base) * 157 + lo - 0x40
    elif 0xa1 <= lo and lo <= 0xfe:
        return offset + (hi - hi_base) * 157 + lo - 0xa1 + 63
    else:
        return -1


def big5_from_order(n: int) -> int:
    """
    Return the big5 character from order.

    0-base, start from '一' (0xA440)
    """
    if n < 0:
        return -1
    return 0


def count_in_big5(data: bytes) -> int:
    """
    Count the number of characters in big5 encoding.
    """
    count = 0
    for i in range(0, len(data), 2):
        if data[i] >= 0xa1 and data[i+1] >= 0x40:
            count += 1
    return count


def count_in_big5_v2(s) -> int:
    """
    1-base, start from '一乙丁七', A440, A441, A442, A443
    """
    up = s[:2]
    dw = s[2:]
    a = int('0x'+up, 16) - int('0xa4', 16)
    bb = int('0x'+dw, 16)
    if bb >= int('0xa1', 16):
        bb = bb - int('0xa1', 16) + 63
    else:
        bb = bb - int('0x40', 16)
    return (a * 157 + bb) + 1


def count_in_big5_v3(s: bytes) -> int:
    a = s[0] - 0xA4
    bb = s[1]
    if bb > 0xA0:  # for lager than 0xa0
        bb = bb - 0x7E
    else:
        bb = bb - 0x40
    return (a * 157 + bb) + 1
