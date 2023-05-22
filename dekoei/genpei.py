import math
import os
import bitarray
import click
from PIL import Image
from utils import (
    BGCOLOR,
    LITTLE_ENDIAN,
    color_codes_to_palette,
    data_to_image,
    save_single_images,
    unpack_npk,
    unpack_npk_3bits,
)

# map, item
genpei_colors = [
    "#000000",
    "#1041A2",
    "#d34100",
    "#E38251",
    "#009230",
    "#71b2b2",
    "#F3B241",
    "#f3f3d3",
    "#302000",
    "#302051",
    "#925130",
    "#C39241",
    "#718251",
    "#102041",
    "#a2a2b2",
    "#C3C3B2",
]

genpei_item_colors = [
    "#000000",
    "#1041A2",
    "#d34100",
    "#E38251",
    "#009230",
    "#71b2b2",
    "#F3B241",
    "#f3f3d3",
]

genpei_select_colors = [
    "#000000",
    "#009230",
    "#d34100",
    "#f3b241",
    "#1041a2",
    "#71b2b2",
    "#e38251",
    "#f3f3d3",
    "#304100",  # 以下未排序
    "#718251",
    "#102041",
    "#a2b241",
    "#302000",
    "#c39241",
    "#925130",
    "#a2a2b2",
]

genpei_opendat_colors = [
    "#000000",
    "#512030",
    "#B292A2",
    "#C3B2B2",
    "#927182",
    "#106192",
    "#e38251",  # not yet
    "#f3f3d3",  # not yet
    "#304100",  # 以下未排序
    "#718251",
    "#102041",
    "#a2b241",
    "#302000",
    "#c39241",
    "#925130",
    "#a2a2b2",
]

genpei_face_colors = [
    "#000000",
    "#009230",
    "#d34100",
    "#f3b241",
    "#1041a2",
    "#71b2b2",
    "#e38251",
    "#f3f3d3",
]


@click.group()
def genpei():
    """源平合戰

    \b
    Kaodata.gp
    Montage.gp
    ENDDAT.GP
    HGROUND.GP          (8px_in_3bytes 時有 mask 的 pattern), 未解析
    HIKBACK.GP          單挑背景
    HKUMI.GP
    HUNITPAT.GP         單位圖案, 動畫, 8px_in_3bytes, 未解析
    OPENDAT.GP          片頭 (error)
    MAINCMD.GP          有「決定」「中止」等字樣, 8px_in_3bytes, 未解析
    MAINCMD2.GP         外交 (error)
    MAINEVT.GP          事件
    MAINITEM.GP         道具
    MAINMAP.GP          地圖
    MAINSTL.GP          月令圖, 小地圖
    """
    pass


@click.command(help="CG 解析")
@click.option("-f", "--file", "cg_file", help="圖像檔案", required=True)
@click.option("--out_dir", "out_dir", default="_output", help="output directory")
@click.option("--prefix", "prefix", default="", help="filename prefix of output files")
def genpei_cg(cg_file, out_dir, prefix):
    """CG 解析"""
    os.makedirs(out_dir, exist_ok=True)

    palette = color_codes_to_palette(genpei_colors)

    with open(cg_file, "rb") as f:
        offsets = []
        data = bytearray(f.read())
        offset = data.find(b"NPK016")
        while offset != -1:
            offsets.append(offset)
            offset = data.find(b"NPK016", offset + 1)
        offsets.append(len(data))
        for offset in offsets[:-1]:
            print(f"processing {offset=:08X}")

        images = []
        width, height = 0, 0
        for i in range(len(offsets) - 1):
            offset = offsets[i]
            size = offsets[i + 1] - offset
            f.seek(offset)
            npk_data = f.read(size)
            width = int.from_bytes(npk_data[0x0C:0x0E], LITTLE_ENDIAN)
            height = int.from_bytes(npk_data[0x0E:0x10], LITTLE_ENDIAN)
            # palette_data = npk_data[0x10:0x30]
            # s = palette_data.hex()
            # result = ' '.join(s[i:i+4] for i in range(0, len(s), 4))
            # print(f"palette: {result}")
            color_indexes = unpack_npk(npk_data[0x30:], width)
            image = Image.new("RGB", (width, height))
            for px_index, color_index in enumerate(color_indexes):
                y, x = divmod(px_index, width)
                c = palette[color_index]
                image.putpixel((x, y), c)
            image.save(f"{out_dir}/{prefix}{i:03d}.png")
            images.append(image)

        # save 大地圖
        if "mainmap" in cg_file.lower():
            image = Image.new("RGB", (width*len(images)-48, height))
            for i, img in enumerate(images):
                pos_x = width * i - math.floor(i/4) * 16
                image.paste(img, (pos_x, 0))
            image.save(f"{out_dir}/{prefix}all.png")
        print(f"save {len(offsets)-1} images")


@click.command(help="顏 CG 解析")
@click.option("-f", "--face", "face_file", help="頭像檔案", required=True)
@click.option("--out_dir", "out_dir", default="_output", help="output directory")
@click.option("--prefix", "prefix", default="", help="filename prefix of output files")
def genpei_face(face_file, out_dir, prefix):
    """顏 CG 解析"""
    os.makedirs(out_dir, exist_ok=True)
    main_file = face_file.lower().replace("kaodata.gp", "main.exe")

    palette = color_codes_to_palette(genpei_item_colors)
    face_w, face_h = 128, 160

    offset_infos = []
    offset = 0
    with open(main_file, "rb") as f:
        n = 90
        for i in range(n):
            # part 1
            f.seek(0x4d51f + i * 2)
            size = int.from_bytes(f.read(2), LITTLE_ENDIAN)
            offset_infos.append((offset, size))
            print(f"{i=} {offset=} {size=}")
            offset += size
            # part 2
            f.seek(0x4d51f + 180 + i * 2)
            size = int.from_bytes(f.read(2), LITTLE_ENDIAN)
            offset_infos.append((offset, size))
            print(f"{i=} {offset=} {size=}")
            offset += size
            offset += 2  # skip 2 bytes

    images = []
    with open(face_file, "rb") as f:
        for idx, (offset, size) in enumerate(offset_infos):
            f.seek(offset)
            data = f.read(size)
            color_indexes = unpack_npk_3bits(data[4:], face_w)
            image = Image.new("RGB", (face_w, face_h), BGCOLOR)
            for px_index, color_index in enumerate(color_indexes):
                if px_index >= face_w * face_h:
                    break
                y, x = divmod(px_index, face_w)
                c = palette[color_index]
                image.putpixel((x, y), c)
            image.save(f"{out_dir}/{prefix}{idx:04d}.png")
            # print(f'{idx=} {offset=} {size=} {len(data)=} {len(color_indexes)=}')  # len(output): 20480, 20492
            if idx % 2 == 1:
                data = f.read(2)
                print(f"{idx=} {data.hex()} {data[0]=} {data[1]=}")
    return
    images = (
        {str(i): img for i, img in enumerate(images)}
        if isinstance(images, list)
        else images
    )
    save_single_images(images, out_dir, prefix)



@click.command(help="顏 CG 解析")
@click.option("-f", "--face", "face_file", help="頭像檔案", required=True)
@click.option("--out_dir", "out_dir", default="_output", help="output directory")
@click.option("--prefix", "prefix", default="", help="filename prefix of output files")
def genpei_montage(face_file, out_dir, prefix):
    palette = color_codes_to_palette(genpei_face_colors)
    face_w, face_h = 72, 77
    areas = [(72, 77), (128, 99), (72, 88), (128, 103), (120, 78), (128, 99)]
    areas = [x for x in areas for _ in range(8)]

    # extract_images(face_file, face_w, face_h, palette, out_dir, prefix)

    file_size = os.stat(face_file).st_size
    with open(face_file, "rb") as f:
        for idx, (w, h) in enumerate(areas):
            data_size = int(w * h / 8 * 3)
            mask_size = int(w * h / 8)
            data = f.read(data_size)
            mask = f.read(mask_size)
            bits = bitarray.bitarray()
            bits.frombytes(mask)
            alpha = [0 if b else 255 for b in bits]
            img = data_to_image(data, w, h, palette, alpha=alpha)
            save_single_images({f"{idx}": img}, out_dir, prefix)
        print(f"{f.tell()=} / {file_size=}")


genpei.add_command(genpei_cg, "cg")
genpei.add_command(genpei_face, "face")
genpei.add_command(genpei_montage, "montage")
