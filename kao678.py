import sys
from PIL import Image
import os.path
import math

endian = 'little'


def load_pallete(filename, start_pos=0, reverse_rgb=False):
    with open(filename, 'rb') as f:
        if start_pos == 0:
            _ = f.read(4)
        else:
            _ = f.read(start_pos)
        data = f.read(1024)
        bytes_list = [data[i:i+4] for i in range(0, 1024, 4)]
        if reverse_rgb:
            return [tuple([x[i] for i in range(3, -1, -1)]) for x in bytes_list]
        return [tuple([x[i] for i in range(4)]) for x in bytes_list]


def load_san8_pallete(filename, start_pos=0, reverse_rgb=False):
    with open(filename, 'rb') as f:
        if start_pos == 0:
            _ = f.read(4)
        else:
            _ = f.read(start_pos)
        data = f.read(1024)
        bytes_list = [data[i:i+4] for i in range(0, 1024, 4)]
        if reverse_rgb:
            return [tuple([x[i] for i in range(3, -1, -1)]) for x in bytes_list]
        return [tuple([x[i] for i in range(4)]) for x in bytes_list]


def load_pallete_test(filename):
    palettes = []
    with open(filename, 'rb') as f:
        for _ in range(3):
            _ = f.read(4)
            data = f.read(1024)
            bytes_list = [data[i:i+4] for i in range(0, 1024, 4)]
            palette = [tuple([x[i] for i in range(4)]) for x in bytes_list]
            palettes.append(palette)
    print('p0 vs p1: {}'.format(palettes[0] == palettes[1]))
    print('p0 vs p2: {}'.format(palettes[0] == palettes[2]))
    return palettes[0]


def export_all_face(filename, palette_file, tag):
    pallete = load_pallete(palette_file)

    if not os.path.exists(tag):
        os.makedirs(tag)

    with open(filename, 'rb') as f:
        count = int.from_bytes(f.read(4), endian)
        print('count: {}'.format(count))
        offset = 4 + 16 * count
        img_props = []
        for _ in range(count):
            pos = int.from_bytes(f.read(4), endian)
            size = int.from_bytes(f.read(4), endian)
            w = int.from_bytes(f.read(4), endian)
            h = int.from_bytes(f.read(4), endian)
            print('pos: {}; size: {}; dimension: ({}, {})'.format(pos, size, w, h))
            img_props.append((pos, size, w, h))

        images = []
        for prop in img_props:
            pos, size, w, h = prop
            f.seek(offset + pos)
            img_data = f.read(size)

            image = Image.new('RGB', (w, h), color='magenta')
            for i in range(size):
                x, y = i % w, i // w
                color_index = img_data[i]
                image .putpixel((x, y), pallete[color_index])
            images.append(image)

        # save single
        print('saving single files, count={}, {}'.format(count, len(images)))
        for idx, img in enumerate(images):
            out_filename = '{}/{}_{:04d}.png'.format(tag, tag, idx+1)
            img.save(out_filename)
            print('...save {}'.format(out_filename))

        # save all
        print('saving all-in-one files')
        face_w = img_props[0][2]
        face_h = img_props[0][3]
        img_w = face_w * 16
        img_h = face_h * math.ceil(count / 16)
        back_image = Image.new('RGB', (img_w, img_h), color='magenta')
        out_filename = '{}/00_{}_FACES.png'.format(tag, tag)
        for idx, img in enumerate(images):
            pos_x = (idx % 16) * face_w
            pos_y = (idx // 16) * face_h
            back_image.paste(img, (pos_x, pos_y))
        back_image.save(out_filename)


def export_face(filename, idx):
    img_data = None
    with open(filename, 'rb') as f:
        count = int.from_bytes(f.read(4), endian)
        print('count: {}'.format(count))
        offset = 4 + 16 * count
        f.seek(4 + idx * 16)
        pos = int.from_bytes(f.read(4), endian)
        size = int.from_bytes(f.read(4), endian)
        w = int.from_bytes(f.read(4), endian)
        h = int.from_bytes(f.read(4), endian)
        print('pos: {}; size: {}; dimension: ({}, {})'.format(pos, size, w, h))
        f.seek(offset + pos)
        img_data = f.read(size)

    pallete = load_pallete("KAO/SAN6_PALETTE.S6")

    print('img_data len: {}, type: {}'.format(len(img_data), type(img_data)))
    image = Image.new('RGB', (w, h), color='magenta')
    for i in range(size):
        x, y = i % w, i // w
        color_index = img_data[i]
        image.putpixel((x, y), pallete[color_index])
    out_filename = 'KAO_{:04d}.png'.format(idx+1)
    image.save(out_filename)


def export_san8_face(filename, p_filename, tag):
    pallete = load_san8_pallete(p_filename, 5720)  # 5701 from van's text

    if not os.path.exists(tag):
        os.makedirs(tag)

    with open(filename, 'rb') as f:
        count = 846

        f.seek(9392)  # 大頭像 160x180 # 9393 from van's text
        face_w, face_h = 160, 180
        # f.seek(24374192)  # 小頭像 64x80 # 24374193 from van's text
        # face_w, face_h = 64, 80

        img_size = face_w * face_h
        img_w = face_w * 16
        img_h = face_h * math.ceil(count / 16)
        back_image = Image.new('RGB', (img_w, img_h), color='magenta')
        out_filename = '00_{}_FACES.png'.format(tag)
        for idx in range(count):
            # generate one image
            bytes_data = f.read(img_size)
            image = Image.new('RGB', (face_w, face_h), color='magenta')
            for i in range(img_size):
                x, y = i % face_w, i // face_w
                color_index = bytes_data[i]
                image .putpixel((x, y), pallete[color_index])
            print("process {:04d} image...".format(idx))
            single_filename = '{}/{}_{:04d}.png'.format(tag, tag, idx+1)
            image.save(single_filename)

            # paste to back image
            pos_x = (idx % 16) * face_w
            pos_y = (idx // 16) * face_h
            back_image.paste(image, (pos_x, pos_y))
        back_image.save(out_filename)


def main():
    args = sys.argv[1:]

    # SAN6 輸出單一張圖
    # export_face("KAO/SAN6_KAODATA.S6", int(args[0], 10))

    # SAN6 輸出全部單圖與全圖
    # export_all_face("KAO/SAN6_KAODATA.S6", "KAO/SAN6_PALETTE.S6", args[0])

    # SAN7 輸出全部單圖與全圖
    # export_all_face('KAO/SAN7_Kaodata.s7', 'KAO/SAN7_P_Kao.s7', args[0])

    # SAN8
    export_san8_face("KAO/SAN8_g_maindy.s8", 'KAO/SAN8_P_MAIN.S8', args[0])
    # export_san8_face("KAO/SAN8_g_maindy.s8", 'KAO/SAN7_P_KAO.S7', args[0])


if __name__ == '__main__':
    main()
