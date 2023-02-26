#!/usr/bin/env python3
import click
from PIL import Image
import os
import os.path
import math
from bitstream import BitStream


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
        G_FacLPK.s9
        G_FacSPK.s9
        G_FacTPK.s9
        P_Face.s9
    """
    pass


@click.group()
def san10():
    """三國志X

    \b
    File List:
        Grp\GpkFace1.s10
        Grp\GpkFace2.s10
        Grp\GpkFaceL.s10
        Grp\GpkFaceS.s10
        Grp\GpkFaceT.s10
        Grp\GrpFaceL.s10 832
        Grp\GrpFaceS.s10 1451, 分左右面向
        Grp\GrpFaceT.s10 832
        P_Face.s9
    """
    pass


def get_codes(data):
    codes = []
    stream = BitStream(data, bytes)
    c1, c2 = 0, 0
    cursor = 0
    pos_end = len(data)*8
    l = 0
    while True:
        bit = stream.read(bool)
        cursor += 1
        c1 = (c1 << 1) | bit
        l += 1
        if not bit:
            for i in range(l):
                c2 = (c2 << 1) | stream.read(bool)
                cursor += 1
            codes.append(c1+c2)
            c1, c2 = 0, 0
            l = 0
        if cursor >= pos_end:
            break
    return codes


def ls11_decode_data(data, dictionary, orig_size):
    original_bytes = bytearray(orig_size)
    pos = 0

    codes = get_codes(data)
    # print('[{}] {}'.format(i, codes))
    # print('{:03d}: [{}]: ({}, {}, {}) ({}, {})'.format(i, pos, *encode_infos[i], len(data), size_of_codes(codes)))
    offset = 0
    count_in_block = 0
    for code in codes:
        # if pos >= original_size:
        #     break
        if count_in_block >= orig_size:
            continue
        if offset > 0:
            length = 3 + code
            for _ in range(length):
                original_bytes[pos] = original_bytes[pos-offset]
                pos += 1
                count_in_block += 1
                if count_in_block >= orig_size:
                    break
            offset = 0
        elif code < 256:
            original_bytes[pos] = dictionary[code]
            pos += 1
            count_in_block += 1
        else:
            offset = code - 256
    return bytes(original_bytes)


def load_palette(filename, start_pos):
    with open(filename, 'rb') as f:
        _ = f.read(start_pos)
        data = f.read(1024)
        color_bytes = [data[i:i+4] for i in range(0, 1024, 4)]
        colors = [tuple([x[i] for i in range(4)]) for x in color_bytes]
        return colors


def load_palette_data(data: bytes):
    color_bytes = [data[i:i+4] for i in range(0, 1024, 4)]
    colors = [tuple(x[2::-1]+x[3:]) for x in color_bytes]  # [b, g, r, a] -> [r, g, b, a]
    return colors


def san9_load_face(filename, palette, face_w=64, face_h=80, count=9999, out_dir='.', start_pos=0):
    data_size = face_w * face_h
    file_size = os.stat(filename).st_size
    count = min(count, file_size // data_size)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    face_images = []
    with open(filename, 'rb') as f:
        f.seek(start_pos)
        for _ in range(count):
            f.read(16)
            face_data = f.read(data_size)
            image = Image.new('RGB', (face_w, face_h), color=(55, 55, 55))
            for px_idx in range(data_size):
                x, y = px_idx % face_w, px_idx // face_w
                color_index = face_data[px_idx]
                image.putpixel((x, y), palette[color_index])
            face_images.append(image)
    return face_images


def san10_load_face(filename, count):
    # data_size = face_w * face_h
    face_images = []
    with open(filename, 'rb') as f:
        f.seek(12)
        group_count = int.from_bytes(f.read(2), 'little')
        print(group_count)
        f.read(6)
        dictionary = f.read(256)
        group_infos = []
        for _ in range(group_count):
            face_w = int.from_bytes(f.read(4), 'little')  # (S) 40000000; (T) 20000000
            face_h = int.from_bytes(f.read(4), 'little')  # (S) 50000000; (T) 28000000
            orig_size = int.from_bytes(f.read(4), 'little')  # 00090000
            pack_size = int.from_bytes(f.read(4), 'little')  # 00090000
            start_pos = int.from_bytes(f.read(4), 'little')  #
            f.read(4)  # 01030000 (?)
            group_infos.append((face_w, face_h, orig_size, pack_size, start_pos))

        count = min(group_count, count)
        for i in range(count):
            face_w, face_h, orig_size, pack_size, start_pos = group_infos[i]
            data_size = face_w * face_h
            f.seek(start_pos)
            pack_data = f.read(pack_size)
            face_data, palette_data = bytes(), bytes()
            if pack_size != orig_size:
                pack_data = ls11_decode_data(pack_data, dictionary, orig_size)
                print('[{}] RLE Decode: ({}, {}, {})'.format(i, orig_size, pack_size, len(face_data)))
            face_data = pack_data[:57600]
            palette_data = pack_data[57600:]
            palette = load_palette_data(palette_data)
            image = Image.new('RGB', (face_w, face_h), color=(55, 55, 55))
            for px_idx in range(data_size):
                x, y = px_idx % face_w, px_idx // face_w
                color_index = face_data[px_idx]
                image.putpixel((x, y), palette[color_index])
            face_images.append(image)
    return face_images


def save_faces(face_images, face_w, face_h, prefix, out_dir):
    is_save_index = False if face_w > 128 else True
    count = len(face_images)

    # save single
    print('saving single files, count={}'.format(count))
    for idx, img in enumerate(face_images):
        out_filename = '{}/{}{:04d}.png'.format(out_dir, prefix, idx + 1)
        img.save(out_filename)
        print("... save {}".format(out_filename))

    # save index
    if is_save_index:
        print('saving index file')
        img_w = face_w * 16
        img_h = face_h * math.ceil(count / 16)
        index_image = Image.new('RGB', (img_w, img_h), color=(55, 55, 55))
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
def san9_face(palette_file, face_file, tag, image_size, prefix):
    """三國志 IX 頭像解析"""
    image_size_spec = {"L": (240, 240), "S": (64, 80), "T": (32, 40)}
    face_w, face_h = image_size_spec[image_size]
    palette = load_palette(palette_file, start_pos=44)
    face_images = san9_load_face(face_file, palette, face_h=face_h, face_w=face_w, out_dir=tag, start_pos=4)
    save_faces(face_images, face_w, face_h, prefix, tag)


@click.command()
def san9_person():
    pass


@click.command(help="顏CG解析")
@click.option('-p', '--palette', 'palette_file', help="色盤", required=True)
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('-t', '--tag', 'tag', default='SAN9', help='')
@click.option('--prefix', 'prefix', help='')
@click.option('--image-size',
              type=click.Choice(['L', 'S', 'T'], case_sensitive=False),
              help='頭像尺寸 L 240x240,\n S:  64x 80,\n T: 32x40')
def san10_face(palette_file, face_file, tag, image_size, prefix):
    """三國志 X 頭像解析"""
    image_size_spec = {"L": (240, 240), "S": (64, 80), "T": (32, 40)}
    face_w, face_h = image_size_spec[image_size]
    face_images = san10_load_face(face_file, 80)
    save_faces(face_images, face_w, face_h, prefix, tag)


san9.add_command(san9_face, "face")
san9.add_command(san9_person, "person")
san10.add_command(san10_face, "face")
dekoei.add_command(san9)
dekoei.add_command(san10)


if __name__ == '__main__':
    dekoei()
