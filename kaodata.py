import itertools
import os.path
import math
from functools import reduce
import sys
from PIL import Image
from game_infos import GAME_INFOS
from numpy import *
from bitstream import *


# 成吉思汗
KHAN_KAODATA = "/Users/tzengyuxio/DOSBox/KHAN/KAODATA.DAT"
KHAN_PALETTE = ['#302000', '#417120', '#D33030', '#D3B282', '#204182', '#418292', '#C38251',
                '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白


def convert_to_array_4color(data_bytes):
    array = []
    it = iter(data_bytes)
    for b1 in it:
        b2 = next(it)
        for i in range(7, -1, -1):
            n = ((b1 >> i) & 1) * 2 + ((b2 >> i) & 1)
            array.append(n)
    return array


def convert_to_array_8color(data_bytes):
    array = []
    it = iter(data_bytes)
    for b1 in it:
        b2, b3 = next(it), next(it)
        for i in range(7, -1, -1):
            n = ((b1 >> i) & 1) * 4 + ((b2 >> i) & 1) * 2 + ((b3 >> i) & 1)
            array.append(n)
    return array


def convert_to_array(data_bytes, color_table):
    return convert_to_array_4color(data_bytes) if len(color_table) == 4 else convert_to_array_8color(data_bytes)


def bytes_to_image(data, w, h, color_table, dh=False):
    """
    Convert binary bytes to image.

    :param data:        binary bytes
    :param w:           width
    :param h:           height
    :param color_table: color table
    :param dh:          double height
    :return:            PIL.Image
    """
    img = Image.new('RGB', (w, h))
    color_indexes = convert_to_array(data, color_table)
    for idx, color_index in enumerate(color_indexes):
        x, y = idx % w, idx // w
        c = color_table[color_index]
        if dh:
            img.putpixel((x, 2 * y), c)
            img.putpixel((x, 2 * y + 1), c)
        else:
            img.putpixel((x, y), c)
    return img


def bytes_to_images(data, size_per_image, w, h, color_table, dh=False):
    """
    Convert binary bytes to image list.
    """
    images = []
    num_images = math.floor(len(data) / size_per_image)
    for i in range(num_images):
        data_bytes = data[size_per_image*i: size_per_image * (i+1)]
        images.append(bytes_to_image(data_bytes, w, h, color_table, dh))
    return images


def export_faces(tag, path, all_in_one=False):
    game_info = GAME_INFOS[tag]

    color_table = []
    for c in game_info['palette']:
        rr, gg, bb = c[1:3], c[3:5], c[5:7]
        color_table.append((int(rr, base=16), int(gg, base=16), int(bb, base=16)))

    # filename = path + '/' + game_info['face_file']
    filename = path
    face_w, face_h = game_info['face_size']
    dh = True if 'double_height' in game_info and game_info['double_height'] else False
    face_count = -1 if 'face_count' not in game_info else game_info['face_count']
    start_pos = 0 if 'start_pos' not in game_info else game_info['start_pos']
    num_bits_per_color = 2 if len(color_table) == 4 else 3
    data_size = int((face_w * face_h) * num_bits_per_color / 8)
    if dh:
        data_size = int(data_size / 2)
    num_face = 0

    filename_postfix = ''
    if tag in ('TEST', 'TEST2'):
        all_in_one = True
        filename_postfix = '_' + os.path.basename(filename).split('.')[0]

    ls11_encoded = False if 'ls11_encoded' not in game_info else game_info['ls11_encoded']
    if ls11_encoded:
        out_filename = '{}.DEC'.format(filename)
        ls11_decode(filename, out_filename)
        filename = out_filename
    with open(filename, 'rb') as f:
        all_face_data_bytes = b''
        if type(start_pos) is not list:
            f.seek(start_pos, os.SEEK_END)
            file_size = f.tell()
            face_count_by_size = file_size // data_size
            num_face = min(face_count, face_count_by_size) if face_count > 0 else face_count_by_size
            # print('  file size   : {}'.format(file_size))
            f.seek(start_pos)
            all_face_data_bytes = f.read(data_size * num_face)
        else:
            parts = []
            num_face = 0
            for sp, fc in zip(start_pos, face_count):
                f.seek(sp)
                db = f.read(fc * data_size)
                num_face += fc
                parts.append(db)
            all_face_data_bytes = all_face_data_bytes.join(parts)
        print('  all data size: {}'.format(len(all_face_data_bytes)))
        print('  face size    : {}x{}, ({} bytes)'.format(face_w, face_h, data_size))
        print('  num of faces : {}'.format(num_face))
        images = bytes_to_images(all_face_data_bytes, data_size, face_w, face_h, color_table, dh)

    if not os.path.exists(tag):
        os.makedirs(tag)

    if all_in_one:
        img_w = face_w * 16
        img_h = face_h * math.ceil(num_face / 16)
        back_image = Image.new('RGB', (img_w, img_h), color='magenta')
        for idx, img in enumerate(images):
            pos_x = (idx % 16) * face_w
            pos_y = (idx // 16) * face_h
            back_image.paste(img, (pos_x, pos_y))
        out_filename = '{}/00_{}_FACES{}.png'.format(tag, tag, filename_postfix)
        back_image.save(out_filename)
        print('...save {}'.format(out_filename))
    else:
        for idx, img in enumerate(images):
            out_filename = '{}/{}_{:04d}.png'.format(tag, tag, idx + 1)
            img.save(out_filename)
            print('...save {}'.format(out_filename))
        print('{} images of face saved in [{}]'.format(num_face, tag))


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
        # print('bit: {}'.format(bit))
        c1 = (c1 << 1) | bit
        l += 1
        if not bit:
            # print('l: {}'.format(l))
            for i in range(l):
                c2 = (c2 << 1) | stream.read(bool)
                cursor += 1
            codes.append(c1+c2)
            c1, c2 = 0, 0
            l = 0
        if cursor >= pos_end:
            break
    return codes


def size_of_codes(codes):
    cnt = 0
    do_copy = False
    for c in codes:
        if do_copy:
            cnt += (3 + c)
            do_copy = False
        elif c > 256:
            do_copy = True
        else:
            cnt += 1
    return cnt


def ls11_decode(in_filename, out_filename):
    with open(in_filename, 'rb') as f, open(out_filename, 'wb') as fout:
        header = f.read(16)
        dictionary = f.read(256)
        encode_infos = []
        b1 = f.read(4)
        while b1 != b'\x00\x00\x00\x00':
            b2 = f.read(4)
            b3 = f.read(4)
            compressed_size = int.from_bytes(b1, 'big')
            original_size = int.from_bytes(b2, 'big')
            start_pos = int.from_bytes(b3, 'big')
            encode_infos.append((compressed_size, original_size, start_pos))
            b1 = f.read(4)
        n = len(encode_infos)
        print('N: {}'.format(n))
        for i in range(n):
            print('  {} {} {}'.format(*encode_infos[i]))

        original_size = reduce(lambda x, y: x+y, [x[1] for x in encode_infos])
        print('original size: {}'.format(original_size))

        original_bytes = bytearray(original_size)
        pos = 0
        for i in range(n):
            # encode_info = encode_infos[i]
            compressed_size, original_size, start_pos = encode_infos[i]
            f.seek(start_pos)
            data = f.read(compressed_size)
            codes = get_codes(data)
            # print('[{}] {}'.format(i, codes))
            # print('{:03d}: [{}]: ({}, {}, {}) ({}, {})'.format(i, pos, *encode_infos[i], len(data), size_of_codes(codes)))
            offset = 0
            count_in_block = 0
            for code in codes:
                # if pos >= original_size:
                #     break
                if count_in_block >= original_size:
                    continue
                if offset > 0:
                    length = 3 + code
                    for _ in range(length):
                        original_bytes[pos] = original_bytes[pos-offset]
                        pos += 1
                        count_in_block += 1
                        if count_in_block >= original_size:
                            break
                    offset = 0
                elif code < 256:
                    original_bytes[pos] = dictionary[code]
                    pos += 1
                    count_in_block += 1
                else:
                    offset = code - 256
        print('original bytes len: {}'.format(len(original_bytes)))
        fout.write(bytes(original_bytes))


def grouper(iterable, n):
    return itertools.zip_longest(*[iter(iterable)] * n)


def revert(array):
    groups = grouper(array, 8)
    bytes_array = []
    for group in groups:
        hi = [x // 2 for x in group]
        lo = [x % 2 for x in group]
        hi_byte = reduce(lambda x, y: (x << 1) + y, hi)
        lo_byte = reduce(lambda x, y: (x << 1) + y, lo)
        print('{:02x} {:02x} '.format(hi_byte, lo_byte), end='')


# revert([0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 0, 3, 2, 3, 2, 2])


# 成吉思涵 (色盤未確定)
# export_kaodata('KHAN', KHAN_KAODATA, KHAN_PALETTE)

# ----------------------------------------------------------------------

# 三國志 1~5
# export_faces('SAN4', '/Users/tzengyuxio/DOSBox/SAN4')
# export_faces('SAN4', '/Users/tzengyuxio/DOSBox/SAN4', all_in_one=True)
# export_faces('SAN4P', '/Users/tzengyuxio/DOSBox/SAN4')
# export_faces('SAN4P', '/Users/tzengyuxio/DOSBox/SAN4', all_in_one=True)
# export_faces('SAN5', '/Users/tzengyuxio/DOSBox/SAN5')
# export_faces('SAN5', '/Users/tzengyuxio/DOSBox/SAN5', all_in_one=True)
# export_faces('SAN5P', '/Users/tzengyuxio/DOSBox/SAN5')
# export_faces('SAN5P', '/Users/tzengyuxio/DOSBox/SAN5', all_in_one=True)

# export_faces('SAN1S', '/Users/tzengyuxio/DOSBox/SteamSAN1', all_in_one=True)
# export_faces('SAN1PC98', '/Users/tzengyuxio/DOSBox/SAN')
# export_faces('SAN1PC98', '/Users/tzengyuxio/DOSBox/SAN', all_in_one=True)
# export_faces('SAN2PC98', '/Users/tzengyuxio/DOSBox/SAN2')
# export_faces('SAN2PC98', '/Users/tzengyuxio/DOSBox/SAN2', all_in_one=True)

# 大航海時代
# export_faces('KOUKAI2', '/Users/tzengyuxio/DOSBox/DAIKOH2')
# export_faces('KOUKAI2', '/Users/tzengyuxio/DOSBox/DAIKOH2', all_in_one=True)
# export_faces('KOUKAI2I', '/Users/tzengyuxio/DOSBox/DAIKOH2', all_in_one=True) # items
# export_faces('KOUKAI2M', '/Users/tzengyuxio/DOSBox/DAIKOH2', all_in_one=True) # montage
# ls11_decode('/Users/tzengyuxio/DOSBox/DAIKOH2/KAO.LZW')
# data = b'\x3C\x93\xF8\x17\x13\xF8\x3B\x2F\x13\xF8\x16\xC3'
# print(get_codes(data))

# 水滸傳
# export_faces('SUIKODEN', '/Users/tzengyuxio/DOSBox/SUI')
# export_faces('SUIKODEN', '/Users/tzengyuxio/DOSBox/SUI', all_in_one=True)

# 航空霸業II (尚未找到)
# export_faces('AIR2', '/Users/tzengyuxio/DOSBox/AIR2', all_in_one=True)

# 獨立戰爭 (尚未找到)
# export_faces('LIBERTY', '/Users/tzengyuxio/DOSBox/LIBERTY')
# export_faces('LIBERTY', '/Users/tzengyuxio/DOSBox/LIBERTY', all_in_one=True)

# ls11_decode('KAODATA/ISHIN2_FACE.I2', 'KAODATA/ISHIN2_FACE.DEC')


def main():
    args = sys.argv[1:]
    if len(args) == 2:
        export_faces(args[0], args[1])
    elif len(args) == 3:
        export_faces(args[0], args[1], True)
    else:
        print("Usage: {} KEYWORD FILENAME (all_in_one)".format(sys.argv[0]))


if __name__ == '__main__':
    main()
