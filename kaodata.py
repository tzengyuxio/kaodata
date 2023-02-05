import itertools
import os.path
from functools import reduce

from PIL import Image

#
SAN1_KAODATA = "/Users/tzengyuxio/DOSBox/SAN1/SAN_B/PICDATA.DAT"
SAN1_PALETTE = ['#000000', '#10B251', '#F35100', '#F3E300', '#0041F3', '#00C3F3', '#F351D3',
                '#F3F3F3']  # 黑 綠 朱 黃 藍 青 洋紅 白

#
SAN2_KAODATA = "/Users/tzengyuxio/DOSBox/SAN2/KAODATA.DAT"
SAN2_MSG16P = "/Users/tzengyuxio/DOSBox/SAN2/MSG.16P"
SAN2_NAME16P = "/Users/tzengyuxio/DOSBox/SAN2/NAME.16P"
SAN2_PALETTE = ['#000000', '#10B251', '#F35100', '#F3E300', '#0041F3', '#00C3F3', '#F351D3',
                '#F3F3F3']  # 黑 綠 朱 黃 藍 青 洋紅 白

# 307張
SAN3_KAODATA = "/Users/tzengyuxio/DOSBox/SAN3/KAODATA.DAT"
SAN3_HAN16P = "/Users/tzengyuxio/DOSBox/SAN3/HAN.16P"  # 1335 字
SAN3_NAME16P = "/Users/tzengyuxio/DOSBox/SAN3/NAME.16P"
SAN3_PALETTE = ['#000000', '#10B251', '#F35100', '#F3E300', '#0041F3', '#00C3F3', '#F351D3',
                '#F3F3F3']  # 黑 綠 朱 黃 藍 青 洋紅 白

# 530,413 byte (340 人需要 652,800)
SAN4_KAODATA = "/Users/tzengyuxio/DOSBox/SAN4/KAODATA.S4"
SAN4_PALETTE = ['#302000', '#204182', '#B24120', '#C38251', '#417120', '#418292', '#D3B282',
                '#D3D3B2']  # 黑 綠 朱 黃 藍 青 洋紅 白

# KAODATA2.S4: 320張, 水滸傳
SAN4_KAODATA2 = "/Users/tzengyuxio/DOSBox/SAN4/KAODATA2.S4"
SAN4_PALETTE2 = ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251',
                 '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白

# KAODATAP.S4: 701張, 1,346,621 byte
SAN4_KAODATAP = "/Users/tzengyuxio/DOSBox/SAN4/KAODATAP.S4"
SAN4_PALETTEP = ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251',
                 '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白

# KAODATA.S5, KAODATAP.S5: 1,503,360 = 783 * 1920, 兩檔案相同
SAN5_KAODATA = "/Users/tzengyuxio/DOSBox/SAN5/KAODATA.S5"
SAN5_PALETTE = ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251',
                '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白

# KAOEX.S5: 733,440 = 382 * 1920
SAN5_KAODATAEX = "/Users/tzengyuxio/DOSBox/SAN5/KAOEX.S5"
SAN5_PALETTEEX = ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251',
                  '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白

# 項劉紀 KANSO/KAO.KR1: 186,240 = 97 * 1920
KANSO_KAODATA = "/Users/tzengyuxio/DOSBox/KANSO/KAO.KR1"
KANSO_PALETTE = ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251',
                 '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白

# 古事記外傳 KAMI/FACEGRP.DAT: 23,040 = 12 * 1920 (不成相)
KAMI_KAODATA = "/Users/tzengyuxio/DOSBox/KAMI/FACEGRP.DAT"
KAMI_PALETTE = ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251',
                '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白

# 成吉思汗
KHAN_KAODATA = "/Users/tzengyuxio/DOSBox/KHAN/KAODATA.DAT"
KHAN_PALETTE = ['#302000', '#417120', '#D33030', '#D3B282', '#204182', '#418292', '#C38251',
                '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白

# 歐陸戰線
EUROPA_KAODATA = "/Users/tzengyuxio/DOSBox/OLZX/FACE.DAT"
EUROPA_PALETTE = ['#000000', '#419241', '#B24120', '#F3C361', '#104192', '#6FAEAE', '#D371B2',
                  '#F3F3F3']  # 黑 綠 紅 粉 藍 青 橙 白

# 提督的決斷2
TK2_KAODATA = "/Users/tzengyuxio/DOSBox/TK2/KAO.TK2"
TK2_PALETTE = ['#000000', '#419241', '#B24120', '#F3C361', '#104192', '#6FAEAE', '#D371B2',
                  '#F3F3F3']  # 黑 綠 紅 粉 藍 青 橙 白

# 魔法皇冠
GEMFIRE_KAODATA = "/Users/tzengyuxio/DOSBox/GEMFIRE/KAODATA.DAT"
GEMFIRE_PALETTE = ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251',
                   '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白


def convert_to_array1(data_bytes):
    array = []
    it = iter(data_bytes)
    for b1 in it:
        b2 = next(it)
        for i in range(7, -1, -1):
            n = ((b1 >> i) & 1) * 2 + ((b2 >> i) & 1)
            array.append(n)
    return array


def convert_to_array(data_bytes):
    array = []
    it = iter(data_bytes)
    for b1 in it:
        b2, b3 = next(it), next(it)
        for i in range(7, -1, -1):
            n = ((b1 >> i) & 1) * 4 + ((b2 >> i) & 1) * 2 + ((b3 >> i) & 1)
            array.append(n)
    return array


def export_kaodata1(tag, filename, palette, stretch=False):
    color_table = []
    for c in palette:
        rr, gg, bb = c[1:3], c[3:5], c[5:7]
        color_table.append((int(rr, base=16), int(gg, base=16), int(bb, base=16)))

    if not os.path.exists(tag):
        os.makedirs(tag)

    with open(filename, 'rb') as f:
        i = 0
        read_size = 480
        while data_bytes := f.read(read_size):
            i += 1
            img = Image.new('RGB', (48, 80))
            color_codes = convert_to_array1(data_bytes)
            for idx, color_code in enumerate(color_codes):
                x, y = idx % 48, idx // 48
                # img.putpixel((x, y), color_table[color_code])
                img.putpixel((x, 2 * y), color_table[color_code])
                img.putpixel((x, 2 * y + 1), color_table[color_code])
            img_filename = '{}/{}_{:04d}.png'.format(tag, tag, i)
            img.save(img_filename)
            print('...save {}'.format(img_filename))
    print('{} images of face saved in [{}]'.format(i, tag))


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
            color_codes = convert_to_array(data_bytes)
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


def export_single_kaodata(tag, filename, palette, stretch=False):
    color_table = []
    for c in palette:
        rr, gg, bb = c[1:3], c[3:5], c[5:7]
        color_table.append((int(rr, base=16), int(gg, base=16), int(bb, base=16)))

    if not os.path.exists(tag):
        os.makedirs(tag)

    face_size = 1920 if not stretch else 960
    face_w = 64
    face_h = 80
    with open(filename, 'rb') as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        num_face = file_size // face_size
        img_w = face_w * 16
        img_h = face_h * ((num_face // 16) + 1)
        print('file size   : {}'.format(file_size))
        print('num of fonts: {}'.format(num_face))
        print('image size  : {}x{} ({}x{})'.format(img_w, img_h, 40, ((num_face // 40) + 1)))

        i = 0
        img = Image.new('RGB', (img_w, img_h), color='black')
        f.seek(0)
        while data_bytes := f.read(face_size):
            color_codes = convert_to_array(data_bytes)
            for idx, color_code in enumerate(color_codes):
                x, y = idx % 64, idx // 64
                abs_x, abs_y = (i % 16) * face_w + x, (i // 16) * face_h + y
                if not stretch:
                    img.putpixel((abs_x, abs_y), color_table[color_code])
                else:
                    abs_y = (i // 16) * img_h + 2 * y
                    img.putpixel((abs_x, abs_y), color_table[color_code])
                    img.putpixel((abs_x, abs_y + 1), color_table[color_code])
            i += 1
        img_filename = '{}/{}_kaodata.png'.format(tag, tag)
        img.save(img_filename)
        print('...save {}'.format(img_filename))
    print('{} images of face saved in [{}]'.format(num_face, tag))


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

# 三國志1
# export_kaodata1('SAN1', SAN1_KAODATA, SAN1_PALETTE)

# 三國志2
# export_kaodata('SAN2', SAN2_KAODATA, SAN2_PALETTE, stretch=True)
# export_font('SAN2', SAN2_MSG16P, pre=True)
# export_font('SAN2', SAN2_NAME16P)

# 三國志3
# export_kaodata('SAN3', SAN3_KAODATA, SAN3_PALETTE)
# export_font('SAN3', SAN3_HAN16P, font_h=14)
# export_font('SAN3', SAN3_NAME16P, font_h=14)

# 三國志4
# export_kaodata('SAN4', SAN4_KAODATA, SAN4_PALETTE)
# export_kaodata('SAN4_2', SAN4_KAODATA2, SAN4_PALETTE2)
# export_kaodata('SAN4_P', SAN4_KAODATAP, SAN4_PALETTEP)

# 三國志5
# export_kaodata('SAN5', SAN5_KAODATA, SAN5_PALETTE)
# export_kaodata('SAN5_EX', SAN5_KAODATAEX, SAN5_PALETTEEX)

# 項劉記 (色盤未確定)
# export_kaodata('KANSO', KANSO_KAODATA, KANSO_PALETTE)

# 古事記外傳 (色盤未確定)
# export_kaodata('KAMI', KAMI_KAODATA, KAMI_PALETTE)

# 成吉思涵 (色盤未確定)
# export_kaodata('KHAN', KHAN_KAODATA, KHAN_PALETTE)

# 歐陸戰線
export_kaodata('EUROPE', EUROPA_KAODATA, EUROPA_PALETTE)
export_single_kaodata('EUROPE', EUROPA_KAODATA, EUROPA_PALETTE)

# 提督的決斷2
export_kaodata('TK2', TK2_KAODATA, TK2_PALETTE)
export_single_kaodata('TK2', TK2_KAODATA, TK2_PALETTE)

# 魔法皇冠
# export_kaodata('GEMFIRE', GEMFIRE_KAODATA, GEMFIRE_PALETTE, stretch=True)
