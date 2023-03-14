import os
from PIL import Image
from utils import grouper, order_of_big5, order_of_koei_tw
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

NOBU4_MSG16P = HOME_DIR + "/DOSBox/NOBU4/MSG.16P"

AIR2_MSG16P = HOME_DIR + "/DOSBox/AIR2/MSG.16P"
AIR2_ZIKU16P = HOME_DIR + "/DOSBox/AIR2/ZIKU.16P"
AIR2_INSTALL16P = HOME_DIR + "/DOSBox/AIR2/INSTALL.16P"
EUROPE_MSG16P = HOME_DIR + "/DOSBox/olzx/MSG.16P"
EUROPE_EMSG16P = HOME_DIR + "/DOSBox/olzx/EMSG.16P"
LEMPE_MSG16P = HOME_DIR + "/DOSBox/lempereur/MSG.16P"
ROYAL_MSG16P = HOME_DIR + "/DOSBox/gemfire/MSG.16P"
SUI_MSG16P = HOME_DIR + "/DOSBox/SUI/MSG.16P"


# 三國志2
# export_font('SAN2', SAN2_NAME16P)

# 三國志3
# export_font('SAN3', SAN3_NAME16P, font_h=14)


def count_big5(s):
    # convert hex string to int
    n = int('0x'+s, 16)
    return order_of_big5(n)


def count_koei(s):
    # convert hex string to int
    n = int('0x'+s, 16)
    return order_of_koei_tw(n)


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
    "美": ("ACFC", "9A30"),  # nobu4 宇佐美 A674 A6F5 ACFC, 949694F59A30
    "納": ("AFC7", "9C66"),  # nobu4 新納 忠元 B773 AFC7 A9BE A4B8, A2BA9C66
    "荀": ("AFFB", "9CA0"),  # SAN3, 荀彧 _, 9CA0B6FC
    "彧": ("D17B", "B6FC"),  # SAN3, 荀彧 _, 9CA0B6FC
    "髦": ("BBEC", "A696"),  # SAN3, 髦
    "尹": ("A4A8", "92E6"),  # SAN3, 尹賞 _, 92E6A841
    "賞": ("BDE0", "A841"),  # SAN3, 尹賞 _, 92E6A841
    "耿": ("AFD5", "9C75"),  # SAN3, 耿武 _, 9C7597BC
    "武": ("AA5A", "97BC"),  # SAN3, 耿武 _, 9C7597BC
    "震": ("BE5F", "A889"),  # SAN3
    "鄭": ("BE47", "A86D"),  # SAN3, 鄭度 _, A86D98F8
    "度": ("ABD7", "98F8"),  # SAN3, 鄭度 _, A86D98F8
    "潘": ("BCEF", "A775"),  # SAN3, 潘濬 _, A775AAAA
    "濬": ("C0E0", "AAAA"),  # SAN3, 潘濬 _, A775AAAA
    "郭": ("B3A2", "9F87"),  # SAN3, 郭汜 _, 9F87B0DA
    "汜": ("C9FA", "B0DA"),  # SAN3, 郭汜 _, 9F87B0DA
    "張": ("B169", "9DAE"),  # SAN3, 張繡(縤) _, 9DAECC66
    "縤": ("EADE", "CC66"),  # SAN3, 張繡(縤) _, 9DAECC66
    "步": ("A842", "95E2"),  # SAN3, 步騭 _, 95E2D4F0
    "騭": ("F563", "D4F0"),  # SAN3, 步騭 _, 95E2D4F0
    "申": ("A5D3", "93F2"),  # SAN3, 申耽 _, 93F29C74
    "耽": ("AFD4", "9C74"),  # SAN3, 申耽 _, 93F29C74
    "雷": ("B970", "A474"),  # SAN3, 雷銅 _, A474A66E
    "銅": ("BBC9", "A66E"),  # SAN3, 雷銅 _, A474A66E
    "鄧": ("BE48", "A86E"),  # SAN3, 鄧賢 _, A86EA846
    "賢": ("BDE5", "A846"),  # SAN3, 鄧賢 _, A86EA846
    "嚴": ("C459", "AD85"),  # SAN3, 嚴輿 _, AD85AB82
    "輿": ("C1D6", "AB82"),  # SAN3, 嚴輿 _, AD85AB82
    "程": ("B57B", "A132"),  # SAN3, 程銀 _, A132A66D
    "銀": ("BBC8", "A66D"),  # SAN3, 程銀 _, A132A66D
    "卓": ("A8F4", "96B6"),  # SAN3, 卓膺 _, 96B6AAFD
    "膺": ("C174", "AAFD"),  # SAN3, 卓膺 _, 96B6AAFD
    "魏": ("C351", "AC9C"),  # SAN3, 魏續 _, AC9CADFC
    "續": ("C4F2", "ADFC"),  # SAN3, 魏續 _, AC9CADFC
    "觀": ("C65B", "AF37"),  # SAN3, 孫觀 _, 9B30AF37
    "夏": ("AE4C", "9AED"),  # SAN3, 夏侯楙 _, 9AED9AB6C177
    "候": ("ADD4", "9AB6"),  # SAN3, 夏侯楙(候) _, 9AED9AB6C177
    "楙": ("DDD5", "C177"),  # SAN3, 夏侯楙 _, 9AED9AB6C177
    "謝": ("C1C2", "AB69"),  # SAN3, 謝旌 _, AB699E31
    "旌": ("B1DC", "9E31"),  # SAN3, 謝旌 _, AB699E31
    "薛": ("C1A7", "AB47"),  # SAN3, 薛悌 _, AB479B6B
    "悌": ("AEAD", "9B6B"),  # SAN3, 薛悌 _, AB479B6B
    "禮": ("C2A7", "ABF0"),  # SAN3, 薛禮 _, AB47ABF0
    "田": ("A5D0", "93EF"),  # SAN3, 田豐 _, 93EFAC58
    "豐": ("C2D7", "AC58"),  # SAN3, 田豐 _, 93EFAC58
    "瓚": ("C5D0", "AEBB"),  # SAN3
    "翊": ("D6F6", "BBBA"),  # SAN3
    "詡": ("E048", "C36A")  # SAN3
    # "春": ("AC4B", "9999"),  #
    # "秋": ("ACEE", "9999"),  #
    # "冬": ("A556", "9999"),  #
    # "莉": ("B2FA", "9549")  # 漢字部分不確定
    # 徐庶 (KOEI)9B579DAB
    # "徐": ("A8A4", "9650"),  # AI
    # 鄒靖 (KOEI)A44FA478
    # "鄒": ("A8A4", "9650"),  # AI
    # 趙雲 (KOEI)A64DA1F7
}


def view_big5_code():
    s = '輿謝旌薛悌禮田豐'  # '即晨晝夜晴雲多雨霧'
    for c in s:
        print(c, big5_code(c))


not_matched = []


def list_relation_and_verify():
    # 列出關係與驗證
    for k in sorted(ctable.keys(), key=lambda x: count_big5(ctable[x][0])):
        v = ctable[k]
        matched = ' ' if count_big5(v[0]) == count_koei(v[1]) else 'x'
        if matched == 'x':
            not_matched.append(v[1])
        delta = count_big5(v[0]) - count_koei(v[1])
        delta_str = ' ' if delta == 0 else ('+'+str(delta) if delta > 0 else str(delta))
        print("{} [{}] {:04d} {:04d}, {} {}".format(k, matched, count_big5(v[0]), count_koei(v[1]), v, delta_str))


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

    for c in sorted(adjusted_codes):
        print(c)
    print('------------------------------------------------------------------------------')
    for c in sorted(uncommon_codes):
        print(c)
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


# view_big5_code()
list_relation_and_verify()
# draw_table()


# == Extract font from file ==
# extract_font(AIR2_MSG16P, 14, 'AIR2_MSG16P')
# extract_font(AIR2_ZIKU16P, 14, 'AIR2_ZIKU16P')
# extract_font(AIR2_INSTALL16P, 14, 'AIR2_INSTALL16P')
# extract_font(EUROPE_MSG16P, 14, 'EUROPE_MSG16P')
# extract_font(EUROPE_EMSG16P, 14, 'EUROPE_EMSG16P')
# extract_font(SAN2_MSG16P, 14, 'SAN2_MSG16P', has_big5_code=True)
# extract_font(SAN3_HAN16P, 14, 'SAN3_HAN16P')
# extract_font(LEMPE_MSG16P, 14, 'LEMPE_MSG16P', has_big5_code=True)
# extract_font(NOBU4_MSG16P, 14, 'NOBU4_MSG16P')
# extract_font(SUI_MSG16P, 14, 'SUI_MSG16P', has_big5_code=True)
# extract_font(ROYAL_MSG16P, 14, 'ROYAL_MSG16P')
