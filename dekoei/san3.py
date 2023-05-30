import struct
import click
from PIL import Image

from utils import (
    color_codes_to_palette,
    extract_images,
    load_person,
    print_table,
    output_images,
)
from san_person import (
    S3Person,
    s3_format,
    s3_headers,
    s3_table_title,
)


@click.group()
def san3():
    """三國志III

    NBDATA.DAT      新武將
    SANGOKU3.SAV    存檔

    dekoei.py san3 face -f kao/SAN3_KAODATA.DAT --out_dir SAN3_DOS --prefix "SAN3_DOS_F"
    dekoei.py san3 face -f kao/SAN3_FACES.BMP --out_dir SAN3_WIN --prefix "SAN3_WIN_F"
    """
    pass


@click.command(help="顏 CG 解析")
@click.option("-f", "--face", "face_file", help="頭像檔案", required=True)
@click.option("--out_dir", "out_dir", default="_output", help="output directory")
@click.option("--prefix", "prefix", default="", help="filename prefix of output files")
def san3_face(face_file, out_dir, prefix):
    """
    KAODATA.DAT (DOS)
    FACES.BMP (WIN, STEAM), 專用顏307, 大眾臉311
    """
    if "faces.bmp" in face_file.lower():
        facebmp = Image.open(face_file)
        skips = [307, 308, 309, 310, 311, 623]
        w, h, num_col = 64, 80, 12
        num_faces = (facebmp.width // 64) * (facebmp.height // 80)
        face_images = dict()
        for i in range(num_faces):
            if i in skips:
                continue
            face = facebmp.crop(
                (
                    i % num_col * w,
                    i // num_col * h,
                    (i % num_col + 1) * w,
                    (i // num_col + 1) * h,
                )
            )
            face_images[str(i)] = face
        output_images(face_images, out_dir, prefix)
        # output_images(list(face_images.values())[:307], out_dir, prefix+'_A')  # 專用顏
        # output_images(list(face_images.values())[307:], out_dir, prefix+'_B')  # 大眾臉
        return

    # for KAODATA.DAT (DOS)
    palette = color_codes_to_palette(
        [
            "#000000",
            "#10B251",
            "#F35100",
            "#F3E300",
            "#0041F3",
            "#00C3F3",
            "#F351D3",
            "#F3F3F3",
        ]
    )
    face_w, face_h = 64, 80

    extract_images(face_file, face_w, face_h, palette, out_dir, prefix)


@click.command(help="人物資料解析")
@click.option("-f", "--file", "file", help="劇本檔案", required=True)
@click.option(
    "--to",
    "to",
    help="Specify output format",
    default="rich",
    type=click.Choice(["rich", "csv", "json", "markdown", "md"]),
)
def san3_person(file, to):
    """
    人物資料解析

    SNDATA1B.CIM

    ./dekoei.py san3 person -f ~/dosbox/SAN3/SNDATA1B.CIM --to csv > PERSONS_TABLE/san3_persons_s1.csv
    ./dekoei.py san3 person -f ~/dosbox/SAN3/SNDATA6B.CIM --to csv > PERSONS_TABLE/san3_persons_s6.csv
    """

    def person_loader(file):
        read_count, read_size = 600, struct.calcsize(s3_format)
        person_data = []
        with open(file, "rb") as f:
            for _ in range(read_count):
                pd = f.read(read_size)
                if pd[43:] == b"\x00\x00\x00\x00\x00\x00":
                    continue
                person_data.append(pd)
        return person_data

    person_data = person_loader(file)

    persons = load_person(person_data, s3_format, S3Person)
    print_table(s3_table_title, s3_headers, persons, to)


san3.add_command(san3_face, "face")
san3.add_command(san3_person, "person")
