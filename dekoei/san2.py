import io
import os
import struct
import click
from PIL import Image

from utils import (
    BGCOLOR,
    LITTLE_ENDIAN,
    calc_part_size,
    color_codes_to_palette,
    create_floppy_image_stream,
    data_to_image,
    extract_images,
    load_images_with_data,
    load_person,
    output_images,
    print_table,
    save_index_image,
    save_single_images,
    unpack_npk_3bits,
)
from san_person import (
    S2Person,
    s2_format,
    s2_format_taiki,
    s2_headers,
    s2_table_title,
)


@click.group()
def san2():
    """三國志II

    KAODATA.DAT

    dekoei.py san2 face -f kao/SAN2_DOS_KAODATA.DAT
    dekoei.py san2 face -f kao/SAN2_PC98_三國志2_b.fdi
    dekoei.py san2 face -f kao/SAN2_WIN_FACE01.SN2 --out_dir _outdir_san2win --prefix SAN2_WIN_F
    """
    pass


@click.command(help="顏 CG 解析")
@click.option("-f", "--face", "face_file", help="頭像檔案", required=True)
@click.option("--out_dir", "out_dir", default="_output", help="output directory")
@click.option("--prefix", "prefix", default="", help="filename prefix of output files")
def san2_face(face_file, out_dir, prefix):
    palette = color_codes_to_palette(
        [
            "#000000",
            "#55FF55",
            "#FF5555",
            "#FFFF55",
            "#5555FF",
            "#55FFFF",
            "#FF55FF",
            "#FFFFFF",
        ]
    )
    face_w, face_h = 64, 80
    hh = True
    loader = None

    # PC98 floppy image as face_file
    if ".fdi" in face_file.lower():
        """PC98_SAN2_B.FDI"""
        palette = color_codes_to_palette(
            [
                "#000000",
                "#00FF00",
                "#FF0000",
                "#FFFF00",
                "#0000FF",
                "#00FFFF",
                "#FF00FF",
                "#FFFFFF",
            ]
        )
        hh = False
        # NOTE: 在第二組 offset_info 之後還有 52 個 face 大小的 montage 資料
        part_size = calc_part_size(face_w, face_h, len(palette), hh=hh)
        # 371840 = 189440 + 95 * part_size
        offset_infos = [
            (189440, 95 * part_size),
            (371840 + 896, 124 * part_size),
        ]  # (offset, face_count * part_size)
        loader = create_floppy_image_stream(face_file, offset_infos, part_size)
    elif ".hdm" in face_file.lower():
        """X68_SAN2_C.HDM"""
        palette = color_codes_to_palette(
            [
                "#000000",
                "#00E700",
                "#E70000",
                "#E7E700",
                "#0000E7",
                "#00E7E7",
                "#E700E7",
                "#E7E7E7",
            ]
        )
        hh = False
        # 211072 = 28672 + 95 * part_size
        # 396288 = (211072+896) + 95 * part_size
        part_size = calc_part_size(face_w, face_h, len(palette), hh=hh)
        offset_infos = [
            (28672, 95 * part_size),
            (211072 + 896, 96 * part_size),
            (396288 + 896 + 128, 28 * part_size),
        ]  # (offset, face_count * part_size)
        # NOTE: 在第三組 offset_info 之後還有 60 個 face 大小的 montage 資料
        loader = create_floppy_image_stream(face_file, offset_infos, part_size)
    elif ".sn2" in face_file.lower():
        """FACE01.SN2, FACE02.SAN2"""
        bmp_size = 6198
        images = []
        files = [face_file]
        files.append(face_file.replace("FACE01", "FACE02"))
        for f in files:
            with open(f, "rb") as f:
                data = f.read(bmp_size)
                while data:
                    img = Image.open(io.BytesIO(data))
                    images.append(img)
                    data = f.read(bmp_size)
        # save face index: all, special, mob
        save_index_image(images[1:], 64, 80, 16, f"{out_dir}/{prefix}00-INDEX.png")
        save_index_image(
            images[1:220], 64, 80, 16, f"{out_dir}/{prefix}00-INDEX_KAO.png"
        )
        save_index_image(
            images[220:], 64, 80, 16, f"{out_dir}/{prefix}00-INDEX_MOB.png"
        )
        # save single faces
        for idx, img in enumerate(images[1:]):
            filename = f"{out_dir}/{prefix}{idx:04d}.png"
            img.save(filename)
        return

    extract_images(
        face_file, face_w, face_h, palette, out_dir, prefix, hh=hh, data_loader=loader
    )


@click.command(help="人物資料解析")
@click.option("-f", "--file", "file", help="劇本檔案", required=True)
@click.option("-t", "--taiki-file", "taiki_file", help="待機檔案", required=True)
@click.option(
    "--to",
    "to",
    help="Specify output format",
    default="rich",
    type=click.Choice(["rich", "csv", "json", "markdown", "md"]),
)
def san2_person(file, taiki_file, to):
    """
    人物資料解析

    dekoei.py san2 person -f ~/dosbox/SAN2/SCENARIO.DAT -t ~/DOSBox/san2/TAIKI.DAT
    """

    def person_loader(file, taiki_file):
        offsets = [
            0x0,
            0x33AF,
            0x675E,
            0x9B0D,
            0xCEBC,
            0x1026B,
        ]  # size=0x33af per scenario
        read_count, read_size = 215, struct.calcsize(s2_format)  # count=215
        tf_read_count, tf_read_size = 420, struct.calcsize(s2_format_taiki)  # count=420
        person_data = []
        kaos = set()  # 用來過濾重複
        with open(file, "rb") as f, open(taiki_file, "rb") as tf:
            for offset in offsets:
                f.seek(offset + 0x16)
                for _ in range(read_count):
                    pd = f.read(read_size)
                    if pd[26:28] in kaos:  # [26:28]
                        continue
                    if pd[28:32] == b"\x00\x00\x00\x00":
                        break
                    person_data.append(b"".join([b"\xFF\xFF\xFF", pd]))
                    kaos.add(pd[26:28])
            tf.seek(0x6)
            for _ in range(tf_read_count):
                pd = tf.read(tf_read_size)
                if pd[29:31] in kaos:  # [29:31]
                    continue
                if pd[31:35] == b"\x00\x00\x00\x00":
                    break
                person_data.append(pd)
                kaos.add(pd[29:31])
        return person_data

    person_data = person_loader(file, taiki_file)

    persons = load_person(person_data, s2_format_taiki, S2Person)
    print_table(s2_table_title, s2_headers, persons, to)


@click.command(help="地圖資料解析")
@click.option("--game_dir", "game_dir", default="san2", help="game directory")
@click.option("--out_dir", "out_dir", default="_output", help="output directory")
def san2_map(game_dir, out_dir):
    palette = color_codes_to_palette(
        [
            "#000000",
            "#55FF55",
            "#FF5555",
            "#FFFF55",
            "#5555FF",
            "#55FFFF",
            "#FF55FF",
            "#FFFFFF",
        ]
    )
    hex_file = f"{game_dir}/HEXDATA.DAT"
    hex_file = os.path.expanduser(hex_file)
    map_size = 12 * 13
    total_map_size = map_size * 41
    terrain_type_count = 7  # 平原 森林 丘陵 高山 水域 營寨 城池
    terrain_cg_size = int(32 * 16 / 8 * 3)  # 192
    with open(hex_file, "rb") as f:
        f.seek(total_map_size * 2)
        data = f.read(terrain_cg_size * terrain_type_count)
        images = load_images_with_data(
            data, 32, 32, palette, True, terrain_cg_size, terrain_type_count
        )
        output_images(images, out_dir, "")

@click.command(help="其他資料解析")
@click.option("--game_dir", "game_dir", default="san2", help="game directory")
@click.option("--out_dir", "out_dir", default="_output", help="output directory")
def san2_grp(game_dir, out_dir):
    """
    1) 640 x 200 劇本選擇圖
    2) 296 x 200 大地圖
    3) 344 x 200 右半邊框
    4) 336 x   3 分隔線
    5)  80 x  56 圖框
    6) 128 x  64 外交事件
    7) 128 x  64 信件攔截事件
    """
    palette = color_codes_to_palette(
        [
            "#000000",
            "#55FF55",
            "#FF5555",
            "#FFFF55",
            "#5555FF",
            "#55FFFF",
            "#FF55FF",
            "#FFFFFF",
        ]
    )
    grp_file = f"{game_dir}/GRPDATA.DAT"
    grp_file = os.path.expanduser(grp_file)
    images = []
    with open(grp_file, 'rb') as f:
        offset_info = [(0, 14254), (14254, 11012), (25266, 1695), (26961, 25), (26986, 174), (27160, 2311), (29471, 14232)]
        for offset, size in offset_info:
            f.seek(offset)
            data = f.read(size)
            w = int.from_bytes(data[0:2], LITTLE_ENDIAN)
            h = int.from_bytes(data[2:4], LITTLE_ENDIAN)
            print(w, h)
            color_indexes = unpack_npk_3bits(data[4:], w, h)
            image = Image.new("RGB", (w, h), BGCOLOR)
            for px_index, color_index in enumerate(color_indexes):
                y, x = divmod(px_index, w)
                c = palette[color_index]
                image.putpixel((x, y), c)
            images.append(image)
    images = (
        {str(i): img for i, img in enumerate(images)}
        if isinstance(images, list)
        else images
    )
    save_single_images(images, out_dir, "")

@click.command(help="其他資料解析")
@click.option("--game_dir", "game_dir", default="san2", help="game directory")
@click.option("--out_dir", "out_dir", default="_output", help="output directory")
def san2_grpa(game_dir, out_dir):
    palette = color_codes_to_palette(
        [
            "#000000",
            "#55FF55",
            "#FF5555",
            "#FFFF55",
            "#5555FF",
            "#55FFFF",
            "#FF55FF",
            "#FFFFFF",
        ]
    )
    # file size 46715
    # 30 張圖 45851
    # left: 864 bytes, 箭頭, 6 方向 6 張，每張 144, 寬 24, 高可能為 16(hh, 32)
    # 風向箭頭
    # 目前未知: 馬, 戰爭圖
    # grp_file = f"{game_dir}/GRPDATA.DAT"
    grp_file = f"{game_dir}/ENDING.DAT"
    grp_file = os.path.expanduser(grp_file)
    images = []
    offsets = []
    with open(grp_file, 'rb') as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        next_offset = 0
        # i = 0
        # while i < 1:
        while True:
            # i += 1
            offset = next_offset
            f.seek(offset)
            dest = bytearray()
            w = int.from_bytes(f.read(2), LITTLE_ENDIAN)
            h = int.from_bytes(f.read(2), LITTLE_ENDIAN)
            if w == 0 or h == 0:
                print(f'OUT OF RANGE: {w=} {h=} pos:{offset=}')
                break
            dest_len = w * h
            while (f.tell() < file_size and len(dest) < dest_len):
                b = f.read(1)[0]
                if b & 0x80:
                    run_size = ((b & 0x0F) + 1)         # info.len
                    run_offset = ((b & 0x30) >> 4) + 1  # info.range
                    run_offset = run_offset * w if (b & 0x40) else run_offset * 4
                    for _ in range(run_size*4):
                        dest.append(dest[-run_offset])
                    # print(f'{data.tell(): 6d} type: {b:08b}, dir: {b & 0x40}, offset: {run_offset}, run_size: {run_size} pos={len(dest)}')
                else:
                    b1 = b
                    b2 = f.read(1)[0]
                    count = ((b1 & 0xF0) >> 4) + 1
                    buf = []
                    for _ in range(4):
                        d = ((b1 & 0x08) >> 1) | ((b2 & 0x80) >> 6) | ((b2 & 0x08) >> 3)
                        buf.append(d)
                        b1 = b1 << 1
                        b2 = b2 << 1
                    dest.extend(buf * count)
                    # print(f'{data.tell(): 6d} type: {(b1>>4):02x} {(b2>>4):02x}, count: {count}, buf: {buf} pos={len(dest)}')
            # save image
            print(f'{w=}, {h=}')
            image = Image.new("RGB", (w, h*2), BGCOLOR)
            for px_index, color_index in enumerate(bytes(dest)):
                y, x = divmod(px_index, w)
                c = palette[color_index]
                # image.putpixel((x, y), c)
                image.putpixel((x, 2*y), c)
                image.putpixel((x, 2*y+1), c)
            images.append(image)
            # prepare for loop
            next_offset = f.tell()
            offsets.append((offset, next_offset-offset))
            if next_offset >= file_size:
                break
        if next_offset < file_size:
            w = 24
            h = 32
            data_size = int(w * h / 2 / 8 * 3) # 108
            for i in range(6):
                data = f.read(data_size)
                img = data_to_image(data, w, h, palette, True)
                images.append(img)
    total_size = 0
    for offset, size in offsets:
        print(f'{offset=}, {size=}')
        total_size += size
    print(f'{total_size=}')
    images = (
        {str(i): img for i, img in enumerate(images)}
        if isinstance(images, list)
        else images
    )
    save_single_images(images, out_dir, "")


san2.add_command(san2_face, "face")
san2.add_command(san2_grp, "grp")
san2.add_command(san2_grpa, "grpa")
san2.add_command(san2_map, "map")
san2.add_command(san2_person, "person")
