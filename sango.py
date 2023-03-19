import click
from collections import namedtuple
from struct import unpack
from rich.console import Console
from rich.table import Table
from utils import *


@click.group()
def san1():
    """三國志（初代）

    SAN_B/PICDATA.DAT

    dekoei.py san1 face -f kao/三國志b.fdi
    dekoei.py san1 face -f kao/SAN1_DOS_PICDATA.DAT
    """
    pass


@click.command(help='顏 CG 解析')
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='_output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def san1_face(face_file, out_dir, prefix):
    palette = color_codes_to_palette(['#000000', '#55FF55', '#FF5555', '#FFFF55'])
    face_w, face_h = 48, 80
    num_part = 114
    loader = None

    # PC98 floppy image as face_file
    if '.fdi' in face_file.lower():
        """PC98_SAN_B.FDI"""
        palette = color_codes_to_palette(
            ['#000000', '#00FF00', '#FF0000', '#FFFF00', '#0000FF', '#00FFFF', '#FF00FF', '#FFFFFF']
        )
        num_part = 113
        offset_infos = [(15360, num_part*1440)]  # (offset, face_count * part_size)
        loader = create_floppy_image_loader(face_file, offset_infos)

    extract_images(face_file, face_w, face_h, palette, out_dir, prefix, num_part=num_part, hh=True, data_loader=loader)


@click.command(help='人物資料解析')
@click.option('-f', '--file', 'file', help="劇本檔案", required=True)
def san1_person(file):
    """
    人物資料解析

    SINADATA.DAT
    """
    # variables: PersonRaw, Person, headers, table_title, converter, loader

    PersonRaw = namedtuple(
        'PersonRaw', 'name,age,body,intell,power,charisma,luck,loyalty,naval,face,soldiers,nation,s_loyalty,s_ability,s_arms')
    Person = namedtuple('Person', 'id, name, face, body, intell, power, charisma, luck')

    def convert_person_raw_to_person(idx, pr):
        return Person(
            id=str(idx),
            name=to_unicode_name(pr.name),
            face=str(pr.face),
            body=str(pr.body),
            intell=str(pr.intell),
            power=str(pr.power),
            charisma=str(pr.charisma),
            luck=str(pr.luck)
        )

    # headers = [H('id', 'ID', 'id'), H('name', '姓名', 'name'), H('face', '顏', 'face'),
    #            H('status', 'Status', 'state'), H('position', 'Position', 'state'), H('loyalty', 'Loyalty', 'state'),
    #            H('age', 'Age', 'base'), H('body', 'Body', 'base'), H('intell', 'Intell.', 'base'), H('power', 'Power', 'base'), H(
    #                'charisma', 'Charisma', 'base'), H('luck', 'Luck', 'base'), H('exp', 'Exper.', 'base'),
    #            H('soldier', 'Soldiers', 'soldier'), H('sloyalty', '-Loyalty', 'soldier'), H('sability', '-Ability', 'soldier'), H('sarms', '-Arms', 'soldier'), H('naval', 'Naval', 'soldier')]
    headers = [H('id', 'ID', 'id'), H('name', '姓名', 'name'), H('face', '顏', 'face'),
               H('body', 'Body', 'base'), H('intell', 'Intell.', 'base'), H('power', 'Power', 'base'), H(
                   'charisma', 'Charisma', 'base'), H('luck', 'Luck', 'base')]
    console = Console()
    table = Table(title="Sangokushi Person Data")
    for h in headers:
        args = column_arguments(h)
        table.add_column(h.text, justify=args['justify'], style=args['style'])
    # 32 bytes, name, age, body, int, pow, charisma, luck, loyalty, position(1: employed?, 3: master), face, soldier, nation, sold.(loyalty, ability, arms)
    fmt = '<12sBBBBBBBBHHxBBBBxxx'

    def person_loader(file):
        person_data = []
        with open(file, 'rb') as f:
            f.seek(4326)
            for _ in range(255):
                person_data.append(f.read(32))
        return person_data

    person_data = person_loader(file)

    persons = []
    for idx, pd in enumerate(person_data):
        pr = PersonRaw._make(unpack(fmt, pd))
        p = convert_person_raw_to_person(idx, pr)
        persons.append(p)

    for p in persons:
        table.add_row(*[getattr(p, h.name) for h in headers])

    console.print(table)


san1.add_command(san1_face, 'face')
san1.add_command(san1_person, 'person')

##############################################################################


@click.group()
def san2():
    """三國志II

    KAODATA.DAT

    dekoei.py san2 face -f kao/SAN2_DOS_KAODATA.DAT
    dekoei.py san2 face -f kao/SAN2_PC98_三國志2_b.fdi
    """
    pass


@click.command(help='顏 CG 解析')
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='_output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def san2_face(face_file, out_dir, prefix):
    palette = color_codes_to_palette(
        ['#000000', '#55FF55', '#FF5555', '#FFFF55', '#5555FF', '#55FFFF', '#FF55FF', '#FFFFFF']
    )
    face_w, face_h = 64, 80
    hh = True
    loader = None

    # PC98 floppy image as face_file
    if '.fdi' in face_file.lower():
        """PC98_SAN2_B.FDI"""
        palette = color_codes_to_palette(
            ['#000000', '#00FF00', '#FF0000', '#FFFF00', '#0000FF', '#00FFFF', '#FF00FF', '#FFFFFF']
        )
        hh = False
        # NOTE: 在第二組 offset_info 之後還有 52 個 face 大小的 montage 資料
        offset_infos = [(189440, 95*1920), (372736, 124*1920)]  # (offset, face_count * part_size)
        loader = create_floppy_image_loader(face_file, offset_infos)

    extract_images(face_file, face_w, face_h, palette, out_dir, prefix, hh=hh, data_loader=loader)


@click.command(help='人物資料解析')
@click.option('-f', '--file', 'file', help="劇本檔案", required=True)
def san2_person(file):
    """
    人物資料解析

    <filename>
    """

    # 定義 PersonRaw 資料結構
    # 定義 Person 資料結構
    # func of PersonRaw -> Person
    #
    # 定義 headers
    # new table and add columns with header
    # 定義 'stack unpack fmt' for PersonRaw
    #
    # 宣告 persons
    # with open file:
    #     read data (maybe need to join with parts)
    #     pr = PersonRaw._make(unpack(fmt, data))
    #     p = convert(pr)
    #     persons.append(p)
    #
    # for p in persons:
    #     add row to table, or
    #     output as csv
    # print summary of persons


san2.add_command(san2_face, 'face')
san2.add_command(san2_person, 'person')

##############################################################################


@click.group()
def san3():
    """三國志III

    NBDATA.DAT      新武將
    SANGOKU3.SAV    存檔

    dekoei.py san3 face -f kao/SAN3_KAODATA.DAT --out_dir SAN3_DOS --prefix "SAN3_DOS_F"
    dekoei.py san3 face -f kao/SAN3_FACES.BMP --out_dir SAN3_WIN --prefix "SAN3_WIN_F"
    """
    pass


@click.command(help='顏 CG 解析')
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='_output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def san3_face(face_file, out_dir, prefix):
    """
    KAODATA.DAT (DOS)
    FACES.BMP (WIN, STEAM), 專用顏307, 大眾臉311
    """
    if 'faces.bmp' in face_file.lower():
        facebmp = Image.open(face_file)
        skips = [307, 308, 309, 310, 311, 623]
        w, h, num_col = 64, 80, 12
        num_faces = (facebmp.width // 64) * (facebmp.height // 80)
        face_images = dict()
        for i in range(num_faces):
            if i in skips:
                continue
            face = facebmp.crop((i % num_col * w, i // num_col * h, (i % num_col + 1) * w, (i // num_col + 1) * h))
            face_images[str(i)] = face
        output_images(face_images, out_dir, prefix)
        # output_images(list(face_images.values())[:307], out_dir, prefix+'_A')  # 專用顏
        # output_images(list(face_images.values())[307:], out_dir, prefix+'_B')  # 大眾臉
        return

    # for KAODATA.DAT (DOS)
    palette = color_codes_to_palette(
        ['#000000', '#10B251', '#F35100', '#F3E300', '#0041F3', '#00C3F3', '#F351D3', '#F3F3F3']
    )
    face_w, face_h = 64, 80

    extract_images(face_file, face_w, face_h, palette, out_dir, prefix)


@click.command(help='人物資料解析')
@click.option('-f', '--file', 'file', help="劇本檔案", required=True)
def san3_person(file):
    """
    人物資料解析

    SNDATA1B.CIM
    """
    headers = [H('id', 'ID', 'id'), H('name', '姓名', 'name'), H('face', '顏', 'face'),
               H('army', '陸指', 'base'), H('navy', '水指', 'base'), H('war', '武力', 'base'), H(
                   'intl', '智力', 'base'), H('pol', '政治', 'base'), H('charm', '魅力', 'base'),
               H('aisho', '相性', 'mask'), H('justice', '義理', 'mask')]
    console = Console()
    table = Table(title="Sangokushi III Person Data")
    for h in headers:
        args = column_arguments(h)
        table.add_column(h.text, justify=args['justify'], style=args['style'])

    Person = namedtuple('Person', 'face, next, soldier, items, mask, \
                        action, sick, lifespan, undercover, role, \
                        army, navy, war, intl, pol, chrm,\
                        aisho, justice, royalty, city, faction, service, \
                        in_faction, in_service, family, train, morale, birth, job, month, \
                        name')

    def kao2str(face):
        if face <= 307:
            return '[red]'+str(face)
        else:
            # convert face from number to hex string
            return hex(face)[2:].upper()

    # 0x0000 顏 次席 士兵 寶物 MASK STATUS ABILITY 相性 義理 忠誠 城市 勢力 仕官 裡所屬士官 親族 訓練 士氣 無 生年 工作 餘月 無 姓名
    # xx     H  H   H   H   H    BBBBB  BBBBBB   B   B   B   B   B   B    BB       B   B   B   xxx B   B   B   xxx 6s
    fmt = '<xxHHHHHBBBBBBBBBBBBBBBBBBBBBBxxxBBBxxx6s'
    with open(file, 'rb') as f:
        for i in range(600):
            data = f.read(49)
            p = Person._make(unpack(fmt, data))
            if p.name == b'\x00\x00\x00\x00\x00\x00':
                continue
            name = to_unicode_name(p.name)
            table.add_row(str(i), name, kao2str(p.face), str(p.army), str(p.navy), str(
                p.war), str(p.intl), str(p.pol), str(p.chrm), str(p.aisho), str(p.justice))
    console.print(table)


san3.add_command(san3_face, 'face')
san3.add_command(san3_person, 'person')

##############################################################################


@click.group()
def san4():
    """三國志IV"""
    pass


@click.command(help='顏 CG 解析')
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='_output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def san4_face(face_file, out_dir, prefix):
    """
    KAODATA.S4 (DOS, Steam) 530,413 byte (不明)
    KAODATA2.S4 (DOS)       三國志3:150, 水滸:170, TOTAL:320
    KAODATA2.S4 (Steam)     三國志3:150, 水滸:170, 信長:117, TOTAL:437
    KAODATAP.S4 (DOS)       三國志4:340, 水滸:117, 大眾:244, TOTAL:701
    KAODATAP.S4 (Steam)     三國志4:340, 水滸:117, 大眾:244, 信長:117, TOTAL:818

    # color pallete (威力加強版編輯器)
    #   | 黑[0] | 深藍[4] | 朱紅[2] | 深皮[6] |
    #   | 綠[1] | 淺藍[5] | 淺皮[3] | 雪白[7] |

    dekoei.py san4 face -f /Volumes/common/San4WPK/KAODATA2.S4 --prefix SAN4_WIN_F
    dekoei.py san4 face -f /Volumes/common/San4WPK/KAODATAP.S4 --prefix SAN4_WIN_F
    """
    palette = color_codes_to_palette(
        ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251', '#D3D3B2']
    )
    face_w, face_h = 64, 80

    extract_images(face_file, face_w, face_h, palette, out_dir, prefix)


san4.add_command(san4_face, 'face')

##############################################################################


@click.group()
def san5():
    """三國志V"""
    pass


@click.command(help='顏 CG 解析')
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='_output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def san5_face(face_file, out_dir, prefix):
    """
    KAODATA.S5 (DOS)    專用與大眾臉: 783
    KAODATAP.S5 (DOS)   同上，兩檔案大小相同 1,503,360 byte
    KAOEX.S5 (DOS)      三４:160, 項劉:30, 信長:60, 英傑:100, 水滸:32, TOTAL:382
    Steam 版三檔案與上述同

    dekoei.py san5 face -f /Volumes/common/San5WPK/KAODATA.S5 --prefix SAN5_WIN_F
    dekoei.py san5 face -f /Volumes/common/San5WPK/KAOEX.S5  --prefix SAN5_WIN_F
    """
    palette = color_codes_to_palette(
        ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    )
    face_w, face_h = 64, 80

    extract_images(face_file, face_w, face_h, palette, out_dir, prefix)


san5.add_command(san5_face, 'face')

##############################################################################


@click.group()
def san6():
    """三國志VI"""
    pass


@click.command(help='顏 CG 解析')
@click.option('-d', '--dir', 'game_dir', help="遊戲目錄")
@click.option('-p', '--palette', 'palette_file', default='Palette.S6', help="色盤檔案")
@click.option('--out_dir', 'out_dir', default='_output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def san6_face(game_dir, palette_file, out_dir, prefix):
    palette: list
    with open(palette_file, 'rb') as f:
        f.read(4)  # 0x00030001
        raw_data = f.read(1024)
        palette = list(grouper(raw_data, 4))

    face_w, face_h = 96, 120

    def loader() -> bytes:
        with open('KAO/SAN6_KAODATA.S6', 'rb') as f:
            """
            KAODATA.S6

            CNT             4       bytes
            OFFSET INFO     16*CNT  bytes
                POS             4   bytes
                SZ              4   bytes
                W               4   bytes
                H               4   bytes
            IMAGES          ...
            """
            count = int.from_bytes(f.read(4), LITTLE_ENDIAN)
            offset = 4 + 16 * count  # 4: header size; 16: info size(pos, len, w, h)
            f.seek(offset)
            return f.read()

    extract_images('', face_w, face_h, palette, out_dir, prefix, data_loader=loader)


san6.add_command(san6_face, 'face')
