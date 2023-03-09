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
    num_face = 128

    # TODO(yuxioz): start_pos(in single value or in list) and face_count(num_face)

    # get face data (binary)
    face_data: bytes
    with open(face_file, 'rb') as f:
        face_data = ls11_decode(f.read())

    # get face images
    face_images = load_images(face_data, face_w, face_h, palette, one_face_data_size, num_face)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # index image
    out_filename = '{}/{}00-INDEX.png'.format(out_dir, prefix)
    save_index_image(face_images, face_w, face_h, 16, out_filename)
    print('...save {}'.format(out_filename))

    # single images
    for idx, img in track(enumerate(face_images)):
        out_filename = '{}/{}{:04d}.png'.format(out_dir, prefix, idx)
        img.save(out_filename)


koukai2.add_command(koukai2_face, 'face')

##############################################################################


@click.group()
def koukai3():
    """大航海時代III"""
    pass


@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('-p', '--palette', 'palette_file', default='cds95FaceHeader.bmp', help="色盤檔案")
@click.option('--out_dir', 'out_dir', default='output')
@click.option('--prefix', 'prefix', default='')
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

    # get face data (binary)
    face_data: bytes
    with open(face_file, 'rb') as f:
        face_data = ls11_decode(f.read())
    num_face = len(face_data) // one_face_data_size
    # print("num_face: {}, len(face_data): {}".format(num_face, len(face_data)))

    # get face images
    face_images = load_images(face_data, face_w, face_h, palette, one_face_data_size, num_face)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # index image
    out_filename = '{}/{}00-INDEX.png'.format(out_dir, prefix)
    save_index_image(face_images, face_w, face_h, 16, out_filename)
    print('...save {}'.format(out_filename))

    # single images
    for idx, img in track(enumerate(face_images), description='Saving...       '):
        out_filename = '{}/{}{:04d}.png'.format(out_dir, prefix, idx)
        img.save(out_filename)


koukai3.add_command(koukai3_face, 'face')
