import os
from PIL import Image
from utils import grouper
from rich.console import Console
from rich.table import Table
#
SAN2_MSG16P = "/Users/tzengyuxio/DOSBox/SAN2/MSG.16P"
SAN2_NAME16P = "/Users/tzengyuxio/DOSBox/SAN2/NAME.16P"

# 307張
SAN3_HAN16P = "/Users/tzengyuxio/DOSBox/SAN3/HAN.16P"  # 1335 字
SAN3_NAME16P = "/Users/tzengyuxio/DOSBox/SAN3/NAME.16P"


def export_font(tag, filename, font_h=14, pre=True):
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
            c = f.read(2)  # 這個是 big5
            print('{}: ({}, {})'.format(c.hex(), i // 40, i % 40))
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
                c = f.read(2)
                print('{}: ({}, {})'.format(c.hex(), i // 40, i % 40))
    img_filename = '{}_{}.png'.format(tag, os.path.basename(filename).replace('.', ''))
    img.save(img_filename)
    print('...save {}'.format(img_filename))
    print()

# 三國志2
# export_font('SAN2', SAN2_MSG16P, pre=True)
# export_font('SAN2', SAN2_NAME16P)

# 三國志3
# export_font('SAN3', SAN3_HAN16P, font_h=14)
# export_font('SAN3', SAN3_NAME16P, font_h=14)


def count_big5(s):
    up = s[:2]
    dw = s[2:]
    a = int('0x'+up, 16) - int('0xa4', 16)
    bb = int('0x'+dw, 16)
    if bb >= int('0xa1', 16):
        bb = bb - int('0xa1', 16) + 63
    else:
        bb = bb - int('0x40', 16)
    return (a * 157 + bb) + 1


def count_koei(s):
    up = s[:2]
    dw = s[2:]
    a = int('0x'+up, 16) - int('0x92', 16)
    bb = int('0x'+dw, 16)
    if bb >= int('0x80', 16):
        bb = bb - int('0x80', 16) + 62
    elif bb >= int('0x61', 16):
        bb = bb - int('0x61', 16) + 36
    elif bb >= int('0x41', 16):
        bb = bb - int('0x41', 16) + 10
    else:
        bb = bb - int('0x30', 16)
    return (a * 188 + bb) + 1 - 94


def count_koei_old(s):
    up = s[:2]
    dw = s[2:]
    a = int('0x'+up, 16) - int('0x92', 16)
    bb = int('0x'+dw, 16)
    if bb > int('0x80', 16):
        bb = bb - int('0x80', 16) + 63
    else:
        bb = bb - int('0x40', 16)
    return (a * 188 + bb) + 1 - 95


def big5_code(c):
    return c.encode('big5').hex().upper()


# hanzi: (big5, koei)
# koei: check in name, and in MSG16P
ctable = {
    "三": ("A454", "92B4"),  # LEMPE
    "卡": ("A564", "93A5"),  # LEMPE
    "世": ("A540", "9381"),  # LEMPE
    "四": ("A57C", "93BD"),  # LEMPE
    "治": ("AA76", "97D8"),  # LEMPE
    "洛": ("ACA5", "99A7"),  # LEMPE
    "娜": ("AE52", "9AF3"),  # LEMPE
    "拿": ("AEB3", "9B71"),  # LEMPE
    "破": ("AF7D", "9C31"),  # LEMPE
    "崙": ("B15B", "9DA0"),  # LEMPE
    "喬": ("B3EC", "9FD1"),  # LEMPE
    "琳": ("B559", "A0DE"),  # LEMPE, SAN3
    "維": ("BAFB", "A5C3"),  # LEMPE
    "多": ("A668", "948A"),  # LEMPE
    "亞": ("A8C8", "968A"),  # LEMPE
    "袁": ("B04B", "9CAF"),  # SAN3
    "紹": ("B2D0", "9ED4"),  # SAN3
    "曹": ("B1E4", "9E39"),  # SAN3
    "操": ("BEDE", "A8E6"),  # SAN3
    "術": ("B34E", "9F4A"),  # SAN3
    "劉": ("BC42", "A6AB"),  # SAN3
    "表": ("AAED", "986C"),  # SAN3
    "備": ("B3C6", "9FAB"),  # SAN3
    "孫": ("AE5D", "9B30"),  # SAN3
    "公": ("A4BD", "92FB"),  # SAN3
    "王": ("A4FD", "937A"),  # SAN3
    "馬": ("B0A8", "9CEA"),  # SAN3
    "孔": ("A4D5", "934C"),  # SAN3
    "華": ("B5D8", "A17A"),  # SAN3
    "太": ("A4D3", "934A"),  # SAN3
    "尚": ("A97C", "96FD"),  # SAN3
    "黃": ("B6C0", "A236"),  # SAN3
    "良": ("A87D", "9656"),  # SAN3
    "陶": ("B3B3", "9F98"),  # SAN3
    "春": ("AC4B", "9999"),  # 
    "夏": ("AE4C", "9999"),  # 
    "秋": ("ACEE", "9999"),  # 
    "冬": ("A556", "9999"),  # 
    "莉": ("B2FA", "9549")  # 漢字部分不確定
}

# export_font('LEMPE', 'FONT/LEMPE_MSG.16P', pre=True)

# print(count_big5('a454'))  # 三 21
# print(count_big5('a540'))  # 世 158
# print(count_big5('a57c'))  # 四 218
# print(count_big5('aca5'))  # 洛 1324
# print(count_big5('aeb3'))  # 拿 1652 // 後面不管(+3)
# print(count_big5('af7d'))  # 破 1789 (+18)
# print(count_big5('b15b'))  # 崙 2069
# print()
# print(count_koei('92b4'))  # 三 21
# print(count_koei('9381'))  # 世 158
# print(count_koei('93bd'))  # 四 218
# print(count_koei('99a7'))  # 洛 1324
# print(count_koei('9b71'))  # 拿 1647
# print(count_koei('9c31'))  # 破 1771
# print(count_koei('9da0'))  # 崙 2069
# print()

s = '黃良陶春夏秋冬'

for c in s:
    print(c, big5_code(c))

# 列出關係與驗證
for k in sorted(ctable.keys(), key=lambda x: count_big5(ctable[x][0])):
    v = ctable[k]
    matched = ' ' if count_big5(v[0]) == count_koei(v[1]) else 'x'
    print("{} [{}] {:04d} {:04d}, {}".format(k, matched, count_big5(v[0]), count_koei(v[1]), v))


def draw_table():
    codes = set()
    with open('/Users/tzengyuxio/DOSBox/lempereur/NPDATA.CIM', 'rb') as f:
        f.seek(8934)
        for i in range(255):
            data = f.read(17)
            name = data[:14]
            for c in grouper(name, 2):
                if c == (b'\x00', b'\x00') or c == (0, 0):
                    continue
                to_add = ''.join([hex(x)[2:].upper() for x in c])
                if to_add == '00':
                    print('(({}))'.format(c))
                codes.add(to_add)
    print('count:', len(codes))

    with open('/Users/tzengyuxio/DOSBox/SAN3/SNDATA1B.CIM', 'rb') as f:
        for i in range(600):
            data = f.read(49)
            name = data[43:]
            for c in grouper(name, 2):
                if c == (b'\x00', b'\x00') or c == (0, 0):
                    continue
                to_add = ''.join([hex(x)[2:].upper() for x in c])
                if to_add == '00':
                    print('(({}))'.format(c))
                codes.add(to_add)

    print('count:', len(codes))
    # for c in codes:
    #     print(c)

    lower_codes = set()
    for c in codes:
        if c[2:] == '':
            print('({})'.format(c))
        lower_codes.add(c[2:])

    tbl = dict()
    for i in range(16):
        key = hex(i).upper().replace('0X', '')
        tbl[key] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # print(key)

    print('====')
    for c in lower_codes:
        # print('[{}]'.format(c))
        # print('[{}]'.format(c))
        # print(c[0], c[1], type(c[0]))
        # print(int(c[1], 16))
        tbl[c[0]][int(c[1], 16)] += 1

    print('count:', len(lower_codes))

    table = Table(title="Star Wars Movies")

    table.add_column('UPPER\\LOWER', justify="right", style="cyan", no_wrap=True)
    for i in range(16):
        table.add_column(hex(i).upper(), justify="right", style="cyan", no_wrap=True)
    for k, v in tbl.items():
        table.add_row(k, *['' if x == 0 else 'Ｏ' for x in v])

    console = Console()
    console.print(table)


draw_table()
