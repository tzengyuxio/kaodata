import os
import click
from PIL import Image
from utils import (
    BGCOLOR,
    LITTLE_ENDIAN,
    color_codes_to_palette,
    save_single_images,
    unpack_npk,
    unpack_npk_3bits,
)


@click.group()
def liberty():
    """獨立戰爭

    FACE.IDX
    """
    pass


@click.command(help="顏 CG 解析")
@click.option("-f", "--face", "face_file", help="頭像檔案", required=True)
@click.option("--out_dir", "out_dir", default="_output", help="output directory")
@click.option("--prefix", "prefix", default="", help="filename prefix of output files")
def liberty_face(face_file, out_dir, prefix):
    """
    ./dekoei.py liberty face -f ~/DOSBox/LIBERTY/FACE.IDX --out_dir LIBERTY --prefix "FACE"
    ./dekoei.py liberty face -f ~/DOSBox/LIBERTY/GRAPHICS.IDX --out_dir LIBERTY --prefix "GRAPHICS"
    """
    palette = color_codes_to_palette(
        [
            "#000000",
            "#104192",
            "#B25110",
            "#A27171",
            "#417100",
            "#82A2B2",
            "#E3B292",
            "#F3E3D3",
        ]
    )

    os.makedirs(out_dir, exist_ok=True)

    file_size = os.stat(face_file).st_size
    images = []
    with open(face_file, "rb") as f:
        f.read(3)  # 'IDX'
        f.read(1)  # 0x2B (43), 應該是 0x12B (299), 高位元被截斷
        n = 299  # 1196 / 4
        offsets = []
        for _ in range(n):
            offset = int.from_bytes(f.read(4), LITTLE_ENDIAN)
            offsets.append(offset)
        offsets.append(file_size)
        for idx, (offset, next_offset) in enumerate(zip(offsets, offsets[1:])):
            size = next_offset - offset
            f.seek(offset)
            data = f.read(size)
            width = int.from_bytes(data[0:2], LITTLE_ENDIAN)
            height = int.from_bytes(data[2:4], LITTLE_ENDIAN)
            color_indexes = unpack_npk_3bits(data[4:], width)
            # print(f'#{idx:03d} {width}x{height} {len(color_indexes)}')
            image = Image.new("RGB", (width, height), BGCOLOR)
            for px_index, color_index in enumerate(color_indexes):
                y, x = divmod(px_index, width)
                c = palette[color_index]
                image.putpixel((x, y), c)
            images.append(image)
    # save face index: all, special, mob
    save_index_image(images, 64, 80, 16, f"{out_dir}/{prefix}00-INDEX.png")
    # save single faces
    images = (
        {str(i): img for i, img in enumerate(images)}
        if isinstance(images, list)
        else images
    )
    save_single_images(images, out_dir, prefix)


@click.command(help="CG 解析")
@click.option("-f", "--file", "graphic_file", help="圖像檔案", required=True)
@click.option("--out_dir", "out_dir", default="_output", help="output directory")
@click.option("--prefix", "prefix", default="", help="filename prefix of output files")
def liberty_graphic(graphic_file, out_dir, prefix):
    palette = color_codes_to_palette(
        [
            "#000000",
            "#104192",
            "#B25110",
            "#A27171",
            "#417100",
            "#82A2B2",
            "#E3B292",
            "#F3E3D3",
            "#000000",
            "#001082",
            "#105110",
            "#A28241",
            "#208230",
            "#4161D3",
            "#B29271",
            "#F3F3F3",
        ]
    )
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    with open(graphic_file, "rb") as f:
        file_size = os.stat(graphic_file).st_size
        header = f.read(3)
        if header != b"IDX":
            print("not IDX file")
        count = int.from_bytes(f.read(1), LITTLE_ENDIAN)
        offsets = []
        for _ in range(count):
            offset = int.from_bytes(f.read(4), LITTLE_ENDIAN)
            offsets.append(offset)
        offsets.append(file_size)
        for idx, (offset, next_offset) in enumerate(zip(offsets, offsets[1:])):
            f.seek(offset)
            npk_data = f.read(next_offset - offset)
            width = int.from_bytes(npk_data[0x0C:0x0E], LITTLE_ENDIAN)
            height = int.from_bytes(npk_data[0x0E:0x10], LITTLE_ENDIAN)
            # 0x10 ~ 0x30 is palette
            color_indexed_data = unpack_npk(npk_data[0x30:], width)
            image = Image.new("RGB", (width, height), BGCOLOR)
            for px_index, color_index in enumerate(color_indexed_data):
                y, x = divmod(px_index, width)
                c = palette[color_index]
                image.putpixel((x, y), c)
            image.save(f"{out_dir}/{prefix}{idx:03d}.png")
        print(f"save {count} images")


liberty.add_command(liberty_face, "face")
liberty.add_command(liberty_graphic, "graphic")
