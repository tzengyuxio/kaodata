import itertools
import os.path
from functools import reduce

from PIL import Image


#
SAN2_MSG16P = "/Users/tzengyuxio/DOSBox/SAN2/MSG.16P"
SAN2_NAME16P = "/Users/tzengyuxio/DOSBox/SAN2/NAME.16P"

# 307張
SAN3_HAN16P = "/Users/tzengyuxio/DOSBox/SAN3/HAN.16P"  # 1335 字
SAN3_NAME16P = "/Users/tzengyuxio/DOSBox/SAN3/NAME.16P"

# 古事記外傳 KAMI/FACEGRP.DAT: 23,040 = 12 * 1920 (不成相)
KAMI_KAODATA = "/Users/tzengyuxio/DOSBox/KAMI/FACEGRP.DAT"
KAMI_PALETTE = ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251',
                '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白

# 成吉思汗
KHAN_KAODATA = "/Users/tzengyuxio/DOSBox/KHAN/KAODATA.DAT"
KHAN_PALETTE = ['#302000', '#417120', '#D33030', '#D3B282', '#204182', '#418292', '#C38251',
                '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白

# 魔法皇冠
GEMFIRE_KAODATA = "/Users/tzengyuxio/DOSBox/GEMFIRE/KAODATA.DAT"
GEMFIRE_PALETTE = ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251',
                   '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白

GAME_INFOS = {
    "EUROPE": {
        "name": "歐陸戰線",
        "face_file": "FACE.DAT",
        "face_size": (64, 80),
        "palette": ['#000000', '#419241', '#B24120', '#F3C361', '#104192', '#6FAEAE', '#D371B2', '#F3F3F3']
    },
    "TK2": {
        "name": "提督之決斷II",
        "face_file": "KAO.TK2",
        "face_size": (48, 64),
        "palette": ['#000000', '#417100', '#D32000', '#E3A261', '#0030A2', '#7192B2', '#C36161', '#F3F3F3']
    },
    "KOHRYUKI": {
        "name": "項劉記",
        "face_file": "KAO.KR1",
        "face_size": (64, 80),
        "palette": ['#000000', '#418200', '#C34100', '#E3A251', '#0030A2', '#71A2B2', '#B27171', '#F3E3D3']
    },
    "SAN1": {
        "name": "三國志",
        "face_file": "SAN_B/PICDATA.DAT",
        "face_size": (48, 80),
        "face_count": 114,
        "double_height": True,
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55']
    },
    "SAN2": {
        "name": "三國志II",
        "face_file": "KAODATA.DAT",
        "face_size": (64, 80),
        "double_height": True,
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55', '#5555FF', '#55FFFF', '#FF55FF', '#FFFFFF']
    },
    "SAN3": {
        "name": "三國志III",
        "face_file": "KAODATA.DAT",
        "face_size": (64, 80),
        "palette": ['#000000', '#10B251', '#F35100', '#F3E300', '#0041F3', '#00C3F3', '#F351D3', '#F3F3F3']
    },
    "SAN4": {
        "name": "三國志IV",
        "face_file": "KAODATAP.S4", # KAODATA.S4 作用尚不明, File Size: 530,413 byte (340 人需要 652,800)
        "face_size": (64, 80),
        "palette": ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251', '#D3D3B2']
    },
    "SAN4P": {
        "name": "三國志IV 威力加強版",
        "face_file": "KAODATA2.S4",
        "face_size": (64, 80),
        "palette": ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251', '#D3D3B2']
        # color pallete (威力加強版編輯器)
        #   | 黑[0] | 深藍[4] | 朱紅[2] | 深皮[6] |
        #   | 綠[1] | 淺藍[5] | 淺皮[3] | 雪白[7] |
    },
    "SAN5": {
        "name": "三國志V",
        "face_file": "KAODATA.S5", # KAODATA.S5, KAODATAP.S5: 1,503,360 = 783 * 1920, 兩檔案相同
        "face_size": (64, 80),
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    },
    "SAN5P": {
        "name": "三國志V 威力加強版",
        "face_file": "KAOEX.S5",
        "face_size": (64, 80),
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    },
    "AIR2": {
        "name": "航空霸業II",
        "face_file": "MAN.GDT", # CITYFACE.GDT, MAKFACE.GDT, MAKER.GDT, MAN.GDT, STAFF1.GDT 均非 KAO
        "face_size": (64, 80),
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    },
    "LIBERTY": {
        "name": "獨立戰爭",
        "face_file": "FACE.IDX",
        "face_size": (64, 80),
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    }
}


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


def export_faces(tag, path, all_in_one=False):
    game_info = GAME_INFOS[tag]

    color_table = []
    for c in game_info['palette']:
        rr, gg, bb = c[1:3], c[3:5], c[5:7]
        color_table.append((int(rr, base=16), int(gg, base=16), int(bb, base=16)))

    filename = path + '/' + game_info['face_file']
    face_w, face_h = game_info['face_size']
    dh = True if 'double_height' in game_info and game_info['double_height'] else False
    face_count = -1 if 'face_count' not in game_info else game_info['face_count']
    num_bits_per_color = 2 if len(color_table) == 4 else 3
    data_size = int((face_w * face_h) * num_bits_per_color / 8)
    if dh:
        data_size = int(data_size / 2)
    images = []
    with open(filename, 'rb') as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        num_face = face_count if face_count > 0 else file_size // data_size
        print('  file size   : {}'.format(file_size))
        print('  face size   : {}x{}, ({} bytes)'.format(face_w, face_h, data_size))
        print('  num of faces: {}'.format(num_face))
        f.seek(0)

        i = 0
        while data_bytes := f.read(data_size):
            if len(data_bytes) < data_size or i >= num_face:
                break
            images.append(bytes_to_image(data_bytes, face_w, face_h, color_table, dh))
            i += 1

    if not os.path.exists(tag):
        os.makedirs(tag)

    if all_in_one:
        img_w = face_w * 16
        img_h = face_h * ((num_face // 16) + 1)
        back_image = Image.new('RGB', (img_w, img_h), color='black')
        for idx, img in enumerate(images):
            pos_x = (idx % 16) * face_w
            pos_y = (idx // 16) * face_h
            back_image.paste(img, (pos_x, pos_y))
        out_filename = '{}/00_{}_FACES.png'.format(tag, tag)
        back_image.save(out_filename)
        print('...save {}'.format(out_filename))
    else:
        for idx, img in enumerate(images):
            out_filename = '{}/{}_{:04d}.png'.format(tag, tag, idx + 1)
            img.save(out_filename)
            print('...save {}'.format(out_filename))
        print('{} images of face saved in [{}]'.format(num_face, tag))


def export_kaodata(tag, filename, palette, stretch=False):
    color_table = []
    for c in palette:
        rr, gg, bb = c[1:3], c[3:5], c[5:7]
        color_table.append((int(rr, base=16), int(gg, base=16), int(bb, base=16)))

    if not os.path.exists(tag):
        os.makedirs(tag)

    with open(filename, 'rb') as f:
        i = 0
        read_size = 1920 if not stretch else 960
        while data_bytes := f.read(read_size):
            i += 1
            img = Image.new('RGB', (64, 80))
            color_codes = convert_to_array_8color(data_bytes)
            for idx, color_code in enumerate(color_codes):
                x, y = idx % 64, idx // 64
                if not stretch:
                    img.putpixel((x, y), color_table[color_code])
                else:
                    img.putpixel((x, 2 * y), color_table[color_code])
                    img.putpixel((x, 2 * y + 1), color_table[color_code])
            img_filename = '{}/{}_{:04d}.png'.format(tag, tag, i)
            img.save(img_filename)
            print('...save {}'.format(img_filename))
    print('{} images of face saved in [{}]'.format(i, tag))


def export_font(tag, filename, font_h=14, pre=False):
    font_size = font_h * 2
    block_w = 20
    block_h = 28
    with open(filename, 'rb') as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        # num_font = (file_size-4) // font_size if head else file_size // font_size
        num_font = file_size // font_size
        img_w = block_w * 40
        img_h = block_h * ((num_font // 40) + 1)
        # print('head        : {}'.format(head))
        print('file size   : {}'.format(file_size))
        print('num of fonts: {}'.format(num_font))
        print('image size  : {}x{} ({}x{})'.format(img_w, img_h, 40, ((num_font // 40) + 1)))

        i = 0
        img = Image.new('RGB', (img_w, img_h), color='white')
        f.seek(0)
        if pre:
            f.read(2)
        while data_bytes := f.read(font_size):
            for idx, byte in enumerate(data_bytes):
                for k in range(7, -1, -1):
                    x = 7 - k + 8 * (idx % 2)
                    y = idx // 2
                    bit = (byte >> k) & 1
                    abs_x = (i % 40) * block_w + x
                    abs_y = (i // 40) * block_h + y
                    if bit:
                        img.putpixel((abs_x, abs_y), (0, 0, 0))
                    else:
                        img.putpixel((abs_x, abs_y), (255, 255, 255))
            i += 1
            if pre:
                f.read(2)
    img_filename = '{}_{}.png'.format(tag, os.path.basename(filename).replace('.', ''))
    img.save(img_filename)
    print('...save {}'.format(img_filename))
    print()


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

# 三國志2
# export_font('SAN2', SAN2_MSG16P, pre=True)
# export_font('SAN2', SAN2_NAME16P)

# 三國志3
# export_font('SAN3', SAN3_HAN16P, font_h=14)
# export_font('SAN3', SAN3_NAME16P, font_h=14)

# 古事記外傳 (色盤未確定)
# export_kaodata('KAMI', KAMI_KAODATA, KAMI_PALETTE)

# 成吉思涵 (色盤未確定)
# export_kaodata('KHAN', KHAN_KAODATA, KHAN_PALETTE)

# 魔法皇冠
# export_kaodata('GEMFIRE', GEMFIRE_KAODATA, GEMFIRE_PALETTE, stretch=True)

# ----------------------------------------------------------------------

# 歐陸戰線
# export_faces('EUROPE', '/Users/tzengyuxio/DOSBox/OLZX')
# export_faces('EUROPE', '/Users/tzengyuxio/DOSBox/OLZX', all_in_one=True)

# 提督的決斷2
# export_faces('TK2', '/Users/tzengyuxio/DOSBox/TK2')
# export_faces('TK2', '/Users/tzengyuxio/DOSBox/TK2', all_in_one=True)

# 項劉記
# export_faces('KOHRYUKI', '/Users/tzengyuxio/DOSBox/KANSO')
# export_faces('KOHRYUKI', '/Users/tzengyuxio/DOSBox/KANSO', all_in_one=True)

# 三國志 1~5
# export_faces('SAN1', '/Users/tzengyuxio/DOSBox/SAN1')
# export_faces('SAN1', '/Users/tzengyuxio/DOSBox/SAN1', all_in_one=True)
# export_faces('SAN2', '/Users/tzengyuxio/DOSBox/SAN2')
# export_faces('SAN2', '/Users/tzengyuxio/DOSBox/SAN2', all_in_one=True)
# export_faces('SAN3', '/Users/tzengyuxio/DOSBox/SAN3')
# export_faces('SAN3', '/Users/tzengyuxio/DOSBox/SAN3', all_in_one=True)
# export_faces('SAN4', '/Users/tzengyuxio/DOSBox/SAN4')
# export_faces('SAN4', '/Users/tzengyuxio/DOSBox/SAN4', all_in_one=True)
# export_faces('SAN4P', '/Users/tzengyuxio/DOSBox/SAN4')
# export_faces('SAN4P', '/Users/tzengyuxio/DOSBox/SAN4', all_in_one=True)
# export_faces('SAN5', '/Users/tzengyuxio/DOSBox/SAN5')
# export_faces('SAN5', '/Users/tzengyuxio/DOSBox/SAN5', all_in_one=True)
# export_faces('SAN5P', '/Users/tzengyuxio/DOSBox/SAN5')
# export_faces('SAN5P', '/Users/tzengyuxio/DOSBox/SAN5', all_in_one=True)

# 航空霸業II (尚未找到)
# export_faces('AIR2', '/Users/tzengyuxio/DOSBox/AIR2', all_in_one=True)

# 獨立戰爭 (尚未找到)
# export_faces('LIBERTY', '/Users/tzengyuxio/DOSBox/LIBERTY')
export_faces('LIBERTY', '/Users/tzengyuxio/DOSBox/LIBERTY', all_in_one=True)
