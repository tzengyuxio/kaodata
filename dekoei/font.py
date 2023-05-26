import os
from PIL import Image
from utils import *
from rich.console import Console
from rich.table import Table
from math import ceil, floor
from rich.progress import track

cns11643_unicode_table = {}

HOME_DIR = os.path.expanduser('~')

#
SAN2_MSG16P = HOME_DIR + "/DOSBox/SAN2/MSG.16P"
SAN2_NAME16P = HOME_DIR + "/DOSBox/SAN2/NAME.16P"
SAN3_HAN16P = HOME_DIR + "/DOSBox/SAN3/HAN.16P"  # 37380 bytes, 1335 字, 每字 28 bytes
SAN3_NAME16P = HOME_DIR + "/DOSBox/SAN3/NAME.16P"

NOBU4_MSG16P = HOME_DIR + "/DOSBox/NOBU4/MSG.16P"

AIR2_MSG16P = HOME_DIR + "/DOSBox/AIR2/MSG.16P"
AIR2_ZIKU16P = HOME_DIR + "/DOSBox/AIR2/ZIKU.16P"
AIR2_INSTALL16P = HOME_DIR + "/DOSBox/AIR2/INSTALL.16P"
EUROPE_MSG16P = HOME_DIR + "/DOSBox/olzx/MSG.16P"
EUROPE_EMSG16P = HOME_DIR + "/DOSBox/olzx/EMSG.16P"
LEMPE_MSG16P = HOME_DIR + "/DOSBox/lempereur/MSG.16P"
ROYAL_MSG16P = HOME_DIR + "/DOSBox/gemfire/MSG.16P"
SUI_MSG16P = HOME_DIR + "/DOSBox/SUI/MSG.16P"


def big5_code(c):
    return c.encode('big5').hex().upper()


def view_big5_code():
    s = '即晨晝夜'  # '即晨晝夜晴雲多雨霧'
    for c in s:
        print(c, big5_code(c))


not_matched = []


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

    adjusted_codes = set()
    uncommon_codes = set()
    unique_lower_codes = set()
    for c in unique_codes:
        if ('9A30' < c and c < '9C74') or ('A657' < c and c < 'A889'):
            adjusted_codes.add(c)
        if c > 'AAAA':  # 非常用字, 要找出誤差大的修正方式
            uncommon_codes.add(c)
        unique_lower_codes.add(c[2:])
    print('unique_lower_codes len: {:4d}'.format(len(unique_lower_codes)))

    # for c in sorted(adjusted_codes):
    #     print(c)
    # print('------------------------------------------------------------------------------')
    # for c in sorted(uncommon_codes):
    #     print(c)
    print('adjusted_codes:{}'.format(len(adjusted_codes)))
    print('uncommon_codes:{}'.format(len(uncommon_codes)))

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
        [x] Auto add pages when num_row is not enough
        [x] Output filename with count
        [ ] Output big5 code list as well
        [x] Fix total number of rich progress bar
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
    num_row_max = 11
    num_row = ceil(font_data_count / num_col)
    if len(font_data_list) > 2000:
        num_row = num_row_max
    count_per_page = num_col * num_row
    pages = ceil(font_data_count / count_per_page)
    for page_idx in range(pages):
        img_w = cell_width * num_col
        img_h = cell_height * num_row
        img = Image.new('RGB', (img_w, img_h), color='white')
        font_data_list_page = font_data_list[page_idx*count_per_page:(page_idx+1)*count_per_page]
        total = len(font_data_list_page) % count_per_page if page_idx == pages-1 else count_per_page
        for glyph_idx, font_data in track(enumerate(font_data_list_page), total=total):
            for byte_idx, byte in enumerate(font_data):
                for k in range(7, -1, -1):
                    bit = (byte >> k) & 1
                    rel_x = 7-k+8*(byte_idx % 2)
                    rel_y = byte_idx // 2
                    abs_x = (glyph_idx % num_col) * cell_width + rel_x
                    abs_y = (glyph_idx // num_col) * cell_width + rel_y
                    color = (0, 0, 0) if bit == 1 else (255, 255, 255)
                    img.putpixel((abs_x, abs_y), color)

        page_postfix = '_{:02d}'.format(page_idx+1) if pages > 1 else ''
        font_index_filename = 'GLYPH_TABLE_{}({}){}.png'.format(prefix, int(font_data_count), page_postfix)
        img.save(font_index_filename)


def hex_to_unicode(hex_str):
    code_point = int(hex_str, 16)
    return chr(code_point)


def koei_tw_to_unicode(data: bytes) -> str:
    global cns11643_unicode_table
    if len(cns11643_unicode_table) == 0:
        cns11643_unicode_table = load_cns11643_unicode_table()
    cns_code = cns_from_order(order_of_koei_tw(data))
    return cns11643_unicode_table[cns_code]


# TODO:
#   [ ] find out all the font files
#   [x] list all the font which koei-code is higher than A9
#   [ ] OCR? https://gist.github.com/beremaran/dc41c96aa8e3aaa1c1951428314df554
#   [x] write function to convert koei-tw to big5 then to utf-8
#   [ ] check the font order in ziku.16p or name.16p
#       - and see if there is any pattern of the delta between koei-tw and big5
#       - and see if all game use the same font table


view_big5_code()
# draw_table()


# == Extract font from file ==
# extract_font(AIR2_MSG16P, 14, 'AIR2_MSG16P')
# extract_font(AIR2_ZIKU16P, 14, 'AIR2_ZIKU16P')
# extract_font(AIR2_INSTALL16P, 14, 'AIR2_INSTALL16P')
# extract_font(EUROPE_MSG16P, 14, 'EUROPE_MSG16P')
# extract_font(EUROPE_EMSG16P, 14, 'EUROPE_EMSG16P')
# extract_font(SAN2_MSG16P, 14, 'SAN2_MSG16P', has_big5_code=True)
# extract_font(SAN2_NAME16P, 14, 'SAN2_NAME16P')
# extract_font(SAN3_HAN16P, 14, 'SAN3_HAN16P')
# extract_font(SAN3_NAME16P, 14, 'SAN3_NAME16P')
# extract_font(LEMPE_MSG16P, 14, 'LEMPE_MSG16P', has_big5_code=True)
# extract_font(NOBU4_MSG16P, 14, 'NOBU4_MSG16P')
# extract_font(SUI_MSG16P, 14, 'SUI_MSG16P', has_big5_code=True)
# extract_font(ROYAL_MSG16P, 14, 'ROYAL_MSG16P')

print(koei_tw_to_unicode(b'\x92\xa0'))  # 一
print(koei_tw_to_unicode(b'\x92\xb4'))  # 三
print(koei_tw_to_unicode(b'\xa6\x57'))  # 遜
print(koei_tw_to_unicode(b'\xa6\x6d'))  # 銀
print(koei_tw_to_unicode(b'\xb3\xfd'))  # 俅
print(koei_tw_to_unicode(b'\xb0\xda'))  # 汜
print(koei_tw_to_unicode(b'\xc3\x6a'))  # 詡


def cns_order(c: bytes) -> int:
    print(c[0], c[1])
    return (c[0]-0x21) * 94 + (c[1] - 0x21)

# print(cns_order(b'\x21\x21'))  # 0
# print(cns_order(b'\x28\x71'))  # 俅 2-287E
# print(cns_order(b'\x22\x5b'))  # 汜 2-225B
