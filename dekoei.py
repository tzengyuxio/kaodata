#!/usr/bin/env python3
import click
from PIL import Image
import os
import os.path
import math


@click.group()
def dekoei():
    """dekoei command"""
    pass


@click.group()
def san9():
    """三國志IX

    \b
    File List:
        G_FaceL.s9
        G_FaceS.s9
        G_FaceT.s9
        P_Face.s9
    """
    pass


@click.command()
def san10():
    """三國志X"""
    pass


def san9_load_palette(filename, start_pos):
    with open(filename, 'rb') as f:
        _ = f.read(start_pos)
        data = f.read(1024)
        color_bytes = [data[i:i+4] for i in range(0, 1024, 4)]
        colors = [tuple([x[i] for i in range(4)]) for x in color_bytes]
        return colors


def san9_load_face(filename, palette, prefix, face_w=64, face_h=80, count=3, out_dir='.'):
    data_size = face_w * face_h
    file_size = os.stat(filename).st_size
    count = min(count, file_size // data_size)

    is_save_index = False if face_w > 128 else True

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    face_images = []
    with open(filename, 'rb') as f:
        f.read(4)
        for _ in range(count):
            f.read(16)
            face_data = f.read(data_size)
            image = Image.new('RGB', (face_w, face_h), color=(55, 55, 55))
            for px_idx in range(data_size):
                x, y = px_idx % face_w, px_idx // face_w
                color_index = face_data[px_idx]
                image.putpixel((x, y), palette[color_index])
            face_images.append(image)

    # save single
    print('saving single files, count={}, {}'.format(count, len(face_images)))
    for idx, img in enumerate(face_images):
        out_filename = '{}/{}{:04d}.png'.format(out_dir, prefix, idx + 1)
        img.save(out_filename)
        print("... save {}".format(out_filename))

    # save index
    if is_save_index:
        print('saving index file')
        img_w = face_w * 16
        img_h = face_h * math.ceil(count / 16)
        index_image = Image.new('RGB', (img_w, img_h), color=(55,55,55))
        out_filename = '{}/{}00-INDEX.png'.format(out_dir, prefix)
        for idx, img in enumerate(face_images):
            pos_x = (idx % 16) * face_w
            pos_y = (idx // 16) * face_h
            index_image.paste(img, (pos_x, pos_y))
        index_image.save(out_filename)



@click.command(help="顏CG解析")
@click.option('-p', '--palette', 'palette_file', help="色盤", required=True)
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('-t', '--tag', 'tag', default='SAN9', help='')
@click.option('--prefix', 'prefix', help='')
@click.option('--image-size',
              type=click.Choice(['L', 'S', 'T'], case_sensitive=False),
              help='頭像尺寸 L 240x240,\n S:  64x 80,\n T: 32x40')
# @click.argument('output', type=click.File('wb'))
def san9_face(palette_file, face_file, tag, image_size, prefix):
    """三國志 IX 頭像解析"""
    palette = san9_load_palette(palette_file, start_pos=44)
    image_size_spec = {"L": (240, 240), "S": (64, 80), "T": (32, 40)}
    face_w, face_h = image_size_spec[image_size]
    san9_load_face(face_file, palette, prefix, face_h=face_h, face_w=face_w, count=786, out_dir=tag)


@click.command()
def san9_person():
    pass


san9.add_command(san9_face, "face")
san9.add_command(san9_person, "person")
dekoei.add_command(san9)
dekoei.add_command(san10)


if __name__ == '__main__':
    dekoei()
