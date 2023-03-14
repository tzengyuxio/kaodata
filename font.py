import os
from PIL import Image
from utils import grouper
from rich.console import Console
from rich.table import Table
from math import ceil, floor
from rich.progress import track

HOME_DIR = os.path.expanduser('~')

#
SAN2_MSG16P = HOME_DIR + "/DOSBox/SAN2/MSG.16P"
SAN2_NAME16P = HOME_DIR + "/DOSBox/SAN2/NAME.16P"

# 307張
SAN3_HAN16P = HOME_DIR + "/DOSBox/SAN3/HAN.16P"  # 37380 bytes, 1335 字, 每字 28 bytes
SAN3_NAME16P = HOME_DIR + "/DOSBox/SAN3/NAME.16P"

LEMPE_MSG16P = HOME_DIR + "/DOSBox/lempereur/MSG.16P"
NOBU4_MSG16P = HOME_DIR + "/DOSBox/NOBU4/MSG.16P"
SUI_MSG16P = HOME_DIR + "/DOSBox/SUI/MSG.16P"


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
# export_font('SAN2', SAN2_NAME16P)

# 三國志3
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
    "伊": ("A5EC", "9444"),  # nobu4
    "達": ("B946", "A444"),  # nobu4
    "宗": ("A976", "96F7"),  # nobu4
    "中": ("A4A4", "92E2"),  # nobu4
    "野": ("B3A5", "9F8A"),  # nobu4
    "張": ("B169", "9DAE"),  # SAN3
    "飛": ("ADB8", "9A9A"),  # SAN3
    "周": ("A950", "96D1"),  # SAN3
    "倉": ("ADDC", "9ABE"),  # SAN3
    "胡": ("AD4A", "9A43"),  # SAN3, 車兒 966B 96A2
    "宮": ("AE63", "9B36"),  # SAN3, 陳 9F94
    "島": ("AE71", "9B4B"),  # nobu4, 津 999E
    "義": ("B871", "A399"),  # nobu4
    "時": ("AEC9", "9B8C"),  # nobu4
    "泰": ("AEF5", "9BB8"),  # SAN3
    "班": ("AF5A", "9BDC"),  # SAN3, 吳 9562
    "祖": ("AFAA", "9C43"),  # SAN3, 黃 A236
    "純": ("AFC2", "9C61"),  # SAN3
    "蔣": ("BDB1", "A7D9"),  # SAN3, 琬 BEA0
    "蔡": ("BDB2", "A7DA"),  # SAN3, 瑁 A346
    "蒙": ("BB58", "A5DF"),  # SAN3, 呂 9564
    "褚": ("BB75", "A5FC"),  # SAN3, 許褚 9F58
    "遜": ("BBB9", "A657"),  # SAN3, 陸 9F95
    "審": ("BC66", "A6CF"),  # SAN3, 配 9CD8
    "德": ("BC77", "A6E0"),  # SAN3, 龐 ACB1
    "樂": ("BCD6", "A756"),  # SAN3, 進 A1CF
    # "群": ("B873", "9A95"),  # SAN3, 陳 9F94
    "會": ("B77C", "A2C3"),  # SAN3, 鍾 AB95
    "當": ("B7ED", "A34B"),  # SAN3, 韓 ABA6
    "雲": ("B6B3", "A1F7"),  # SAN3
    "賈": ("B8EB", "A3F1"),  # SAN3, 詡 C36A
    "宋": ("A7BA", "959B"),  # SUI
    "江": ("A6BF", "94BF"),  # SUI
    "魯": ("BE7C", "A8A6"),  # SUI
    "智": ("B4BC", "A082"),  # SUI
    "深": ("B260", "9E86"),  # SUI
    "高": ("B0AA", "9CEC"),  # SUI
    "俅": ("CDDE", "B3FD"),  # SUI
    "詡": ("E048", "C36A")  # SAN3
    # "春": ("AC4B", "9999"),  #
    # "夏": ("AE4C", "9999"),  #
    # "秋": ("ACEE", "9999"),  #
    # "冬": ("A556", "9999"),  #
    # "莉": ("B2FA", "9549")  # 漢字部分不確定
    # 徐庶 (KOEI)9B579DAB
    # "徐": ("A8A4", "9650"),  # AI
    # 鄒靖 (KOEI)A44FA478
    # "鄒": ("A8A4", "9650"),  # AI
    # 趙雲 (KOEI)A64DA1F7
}

# export_font('LEMPE', 'FONT/LEMPE_MSG.16P', pre=True)

s = '高俅宋江'  # '即晨晝夜晴雲多雨霧'

for c in s:
    print(c, big5_code(c))

not_matched = []

# 列出關係與驗證
for k in sorted(ctable.keys(), key=lambda x: count_big5(ctable[x][0])):
    v = ctable[k]
    matched = ' ' if count_big5(v[0]) == count_koei(v[1]) else 'x'
    if matched == 'x':
        not_matched.append(v[1])
    print("{} [{}] {:04d} {:04d}, {}".format(k, matched, count_big5(v[0]), count_koei(v[1]), v))


def num_unique(a_list: list) -> int:
    return len(set(a_list))


def collect_koei_font_codes(filename, offset, read_count, read_size, beg, end):
    codes: list[str] = []
    with open(filename, 'rb') as f:
        f.seek(offset)
        for _ in range(read_count):
            data = f.read(read_size)
            text = data[beg:end]
            for c in grouper(text, 2):
                if c == (0, 0):
                    continue
                code = ''.join([hex(x)[2:].upper() for x in c])
                codes.append(code)
    print('  count/distinct: {:4d}/{:4d} ({})'.format(len(codes), num_unique(codes), filename))
    return codes


def draw_table():
    codes = []
    codes.extend(collect_koei_font_codes(HOME_DIR+'/DOSBox/lempereur/NPDATA.CIM', 8934, 255, 17, 0, 14))  # 人名
    codes.extend(collect_koei_font_codes(HOME_DIR+'/DOSBox/lempereur/NPDATA.CIM', 7220, 16, 10, 0, 8))  # 國名
    codes.extend(collect_koei_font_codes(HOME_DIR+'/DOSBox/lempereur/NPDATA.CIM', 7370, 46, 34, 0, 14))  # 城市名
    codes.extend(collect_koei_font_codes(HOME_DIR+'/DOSBox/SAN3/SNDATA1B.CIM', 0, 600, 49, 43, 49))
    codes.extend(collect_koei_font_codes(HOME_DIR+'/DOSBox/SAN3/SNDATA1.CIM', 3733, 21, 25, 0, 6))
    codes.extend(collect_koei_font_codes(HOME_DIR+'/DOSBox/nobu4/SNDATA1.CIM', 4498, 250, 33, 0, 6))  # 風雲錄 劇本1 姓
    codes.extend(collect_koei_font_codes(HOME_DIR+'/DOSBox/nobu4/SNDATA1.CIM', 4505, 250, 33, 0, 6))  # 風雲錄 劇本1 名
    codes.extend(collect_koei_font_codes(HOME_DIR+'/DOSBox/nobu4/SNDATA2.CIM', 4498, 255, 33, 0, 6))  # 風雲錄 劇本2 姓
    codes.extend(collect_koei_font_codes(HOME_DIR+'/DOSBox/nobu4/SNDATA2.CIM', 4505, 255, 33, 0, 6))  # 風雲錄 劇本2 名
    codes.extend(collect_koei_font_codes(HOME_DIR+'/DOSBox/nobu4/SNDATA3.CIM', 4498, 250, 33, 0, 6))  # 風雲錄 劇本3 姓
    codes.extend(collect_koei_font_codes(HOME_DIR+'/DOSBox/nobu4/SNDATA3.CIM', 4505, 250, 33, 0, 6))  # 風雲錄 劇本3 名
    codes.extend(collect_koei_font_codes(HOME_DIR+'/DOSBox/SUI/SUIDATA1.CIM', 7124, 255, 45, 0, 6))  # 水滸傳
    unique_codes = set(codes)
    print('count/distinct: {:4d}/{:4d}'.format(len(codes), len(unique_codes)))

    unique_lower_codes = set()
    for c in unique_codes:
        # if c[:2] >= 'A9': 列出誤差較大範圍
        #     print(c)
        unique_lower_codes.add(c[2:])
    print('unique_lower_codes len: {:4d}'.format(len(unique_lower_codes)))

    tbl = dict()
    for i in range(16):
        key = hex(i).replace('0x', '').upper()
        tbl[key] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    print('not_matched:', len(not_matched))
    for c in unique_codes:
        lo = c[2:]
        try:
            if c in not_matched:  # ('9AF3', '9B30', '9B71', '9C31'):
                tbl[lo[0]][int(lo[1], 16)] += 100
            else:
                tbl[lo[0]][int(lo[1], 16)] += 1
        except IndexError:
            print('+', c, '+')
            raise
        except KeyError:
            print(tbl.keys(), lo[0], lo)

    print('count:', len(unique_lower_codes))

    table = Table(title="")

    table.add_column('HI\\LO', justify="center", style="cyan", no_wrap=True)
    for i in range(16):
        table.add_column(hex(i).upper(), justify="center", style="cyan", no_wrap=True)
    for k, v in tbl.items():
        table.add_row(k+'0', *['[red]⬜️️' if x == 0 else '[red]'+str(x) if x > 100 else '[green]'+str(x) for x in v])

    console = Console()
    console.print(table)


def extract_font(filename: str, glyph_h: int = 14, prefix: str = '', has_big5_code: bool = False) -> None:
    """
    TODO:
        [ ] Custom cell width and height
        [ ] Custom num_col
        [ ] Auto add pages when num_row is not enough
        [x] Output filename with count
        [ ] Output big5 code list as well
    """
    file_size = os.stat(filename).st_size
    font_data_size = glyph_h * 2
    font_data_count = file_size / (font_data_size + 2 if has_big5_code else font_data_size)
    font_data_list = []
    big5_code_list = []
    with open(filename, 'rb') as f:
        if has_big5_code:
            while big5_code := f.read(2):
                font_data = f.read(font_data_size)
                font_data_list.append(font_data)
                big5_code_list.append(big5_code)
        else:
            while font_data := f.read(font_data_size):
                font_data_list.append(font_data)

    # draw font index table
    cell_width = 20
    cell_height = 20
    num_col = 40
    num_row = ceil(font_data_count / num_col)
    img_w = cell_width * num_col
    img_h = cell_height * num_row
    img = Image.new('RGB', (img_w, img_h), color='white')
    for glyph_idx, font_data in track(enumerate(font_data_list), total=font_data_count):
        for byte_idx, byte in enumerate(font_data):
            for k in range(7, -1, -1):
                bit = (byte >> k) & 1
                rel_x = 7-k+8*(byte_idx % 2)
                rel_y = byte_idx // 2
                abs_x = (glyph_idx % num_col) * cell_width + rel_x
                abs_y = (glyph_idx // num_col) * cell_width + rel_y
                color = (0, 0, 0) if bit == 1 else (255, 255, 255)
                img.putpixel((abs_x, abs_y), color)

    img.save('font_index_{}({}).png'.format(prefix, int(font_data_count)))

# TODO:
#   [ ] find out all the font files
#   [ ] list all the font which koei-code is higher than A9
#   [ ] OCR? https://gist.github.com/beremaran/dc41c96aa8e3aaa1c1951428314df554

# draw_table()


extract_font(SAN2_MSG16P, 14, 'SAN2_MSG16P', has_big5_code=True)
extract_font(SAN3_HAN16P, 14, 'SAN3_HAN16P')
extract_font(LEMPE_MSG16P, 14, 'LEMPE_MSG16P', has_big5_code=True)
extract_font(NOBU4_MSG16P, 14, 'NOBU4_MSG16P')
extract_font(SUI_MSG16P, 14, 'SUI_MSG16P', has_big5_code=True)
