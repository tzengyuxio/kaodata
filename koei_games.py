import os
import click
from utils import *
from ls11 import *


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
    """KAO2.LZW"""
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
    face_images = []
    for i in range(num_face):
        pos = i*one_face_data_size
        img = data_to_image(face_data[pos:pos+one_face_data_size], face_w, face_h, palette)
        face_images.append(img)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # index image
    out_filename = '{}/{}00-INDEX.png'.format(out_dir, prefix)
    save_index_image(face_images, face_w, face_h, 16, out_filename)
    print('...save {}'.format(out_filename))

    # single images
    for idx, img in enumerate(face_images):
        out_filename = '{}/{}{:04d}.png'.format(out_dir, prefix, idx)
        img.save(out_filename)
        print('...save {}'.format(out_filename))


koukai2.add_command(koukai2_face, 'face')
