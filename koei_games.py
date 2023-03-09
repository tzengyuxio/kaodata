import os
import click
from utils import *
from ls11 import *
from rich.progress import track
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


@click.group()
def koukai():
    """大航海時代"""
    pass


@click.command(help='顏 CG 解析')
def koukai_face():
    pass


koukai.add_command(koukai_face, 'face')

##############################################################################


@click.group()
def koukai2():
    """大航海時代II"""
    pass


@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='output')
@click.option('--prefix', 'prefix', default='')
@click.command(help='顏 CG 解析')
def koukai2_face(face_file, out_dir, prefix):
    """KAO2.LZW

    /dekoei.py koukai2 face -f kao/KOUKAI2_KAO.LZW
    """
    palette = color_codes_to_palette(
        ['#000000', '#00A261', '#D34100', '#F3A261', '#0041D3', '#00A2F3', '#D361A2', '#F3E3D3']
    )
    face_w, face_h, bpp = 64, 80, 3
    one_face_data_size = int(face_w*face_h*bpp/8)

    # TODO(yuxioz): start_pos(in single value or in list) and face_count(num_face)

    extract_images(face_file, face_w, face_h, palette, out_dir, prefix, one_face_data_size, num_part=128)


koukai2.add_command(koukai2_face, 'face')

##############################################################################


@click.group()
def koukai3():
    """大航海時代III"""
    pass


@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('-p', '--palette', 'palette_file', default='cds95FaceHeader.bmp', help="色盤檔案")
@click.option('--out_dir', 'out_dir', default='output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
@click.command(help='顏 CG 解析')
def koukai3_face(face_file, palette_file, out_dir, prefix):
    """
    ./dekoei.py koukai3 face --face kao/KOUKAI3_FEMALE.CDS --palette kao/cds95FaceHeader.bmp
    ./dekoei.py koukai3 face --face kao/KOUKAI3_MALE.CDS --palette kao/cds95FaceHeader.bmp
    """
    # load palette
    palette_img = Image.open(palette_file)
    # palette_img.mode: "P"
    # palette_img.palette.getdata()[0]: "BGRX"
    #   "P" means using a color palette
    #   "BGRX" means the color order in palette with padding('X')
    #   see https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes

    # get palette with "RGB" mode, return list like [R0, G0, B0, R1, G1, B1, R2...]
    palette = list(grouper(palette_img.getpalette(rawmode='RGB'), 3))

    face_w, face_h = 80, 96
    one_face_data_size = int(face_w*face_h)

    extract_images(face_file, face_w, face_h, palette, out_dir, prefix, one_face_data_size)


koukai3.add_command(koukai3_face, 'face')

##############################################################################


@click.group()
def winning():
    """光榮賽馬, 賽馬大亨"""
    pass


@click.option('-d', '--dir', 'game_dir', help="遊戲目錄", required=True)
@click.option('--out_dir', 'out_dir', default='output')
@click.option('--prefix', 'prefix', default='')
@click.command(help='顏 CG 解析')
def winning_face(game_dir, out_dir, prefix):
    """

    /dekoei.py winning face --dir ~/DOSBox/winning
    """
    palette = color_codes_to_palette(
        ['#000000', '#20D320', '#F30000', '#F3D300', '#0061C3', '#00B2F3', '#F351F3', '#F3F3F3']
    )
    face_w, face_h, bpp = 64, 80, 3
    one_face_data_size = int(face_w*face_h*bpp/8)

    def loader() -> bytes:
        raw_data = bytearray()
        with open(game_dir+'/KAO.DAT', 'rb') as f:
            raw_data.extend(f.read())
        with open(game_dir+'/TEXTGRP.DAT', 'rb') as f:
            raw_data.extend(f.read(one_face_data_size))
        return bytes(raw_data)

    extract_images('', face_w, face_h, palette, out_dir, prefix, one_face_data_size, data_loader=loader)


winning.add_command(winning_face, 'face')
