import struct
import click
from PIL import Image

from utils import (
    calc_part_size,
    color_codes_to_palette,
    create_floppy_image_stream,
    extract_images,
    load_person,
    print_table,
    save_index_image,
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


san2.add_command(san2_face, "face")
san2.add_command(san2_person, "person")
