import struct
import click

from utils import (
    calc_part_size,
    color_codes_to_palette,
    create_floppy_image_stream,
    extract_images,
    load_person,
    print_table,
)
from san_person import S1Person, s1_format, s1_headers, s1_table_title


@click.group()
def san1():
    """三國志（初代）

    SAN_B/PICDATA.DAT

    dekoei.py san1 face -f kao/三國志b.fdi
    dekoei.py san1 face -f kao/SAN1_DOS_PICDATA.DAT
    """
    pass


@click.command(help="顏 CG 解析")
@click.option("-f", "--face", "face_file", help="頭像檔案", required=True)
@click.option("--out_dir", "out_dir", default="_output", help="output directory")
@click.option("--prefix", "prefix", default="", help="filename prefix of output files")
def san1_face(face_file, out_dir, prefix):
    palette = color_codes_to_palette(["#000000", "#55FF55", "#FF5555", "#FFFF55"])
    face_w, face_h = 48, 80
    num_part = 114
    loader = None

    # PC98 floppy image as face_file
    if ".fdi" in face_file.lower():
        """PC98_SAN_B.FDI"""
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
        num_part = 113
        part_size = calc_part_size(face_w, face_h, len(palette), hh=True)
        offset_infos = [
            (15360, num_part * part_size)
        ]  # (offset, face_count * part_size)
        loader = create_floppy_image_stream(face_file, offset_infos, part_size)

    extract_images(
        face_file,
        face_w,
        face_h,
        palette,
        out_dir,
        prefix,
        num_part=num_part,
        hh=True,
        data_loader=loader,
    )


@click.command(help="人物資料解析")
@click.option("-f", "--file", "file", help="劇本檔案", required=True)
@click.option("-s", "--scenario", "scenario", help="劇本", default=0)
@click.option(
    "-t",
    "--to",
    "to",
    help="Specify output format",
    default="rich",
    type=click.Choice(["rich", "csv", "json", "markdown", "md"]),
)
def san1_person(file, scenario, to):
    """
    人物資料解析

    SINADATA.DAT

    ./dekoei.py san1 person -s 1 -f ~/dosbox/san1/SINADATA.DAT --to csv > PERSONS_TABLE/san1_persons_s1.csv
    """

    def person_loader(file, scenario=0):
        offsets = [4326, 16816, 29306, 41796, 54286]
        read_count, read_size = 255, struct.calcsize(s1_format)
        person_data = []
        with open(file, "rb") as f:
            f.seek(offsets[scenario])
            for _ in range(read_count):
                person_data.append(f.read(read_size))
        return person_data

    person_data = person_loader(file, scenario)

    persons = load_person(person_data, s1_format, S1Person)
    print_table(s1_table_title, s1_headers, persons, to)


san1.add_command(san1_face, "face")
san1.add_command(san1_person, "person")
