import click
from rich.console import Console
from utils import *
from san_person import *

console = Console()


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
@click.option('-s', '--scenario', 'scenario', help="劇本", default=0)
def san1_person(file, scenario):
    """
    人物資料解析

    SINADATA.DAT
    """
    def person_loader(file, scenario=0):
        offsets = [4326, 16816, 29306, 41796, 54286]
        read_count, read_size = 255, struct.calcsize(s1_format)
        person_data = []
        with open(file, 'rb') as f:
            f.seek(offsets[scenario])
            for _ in range(read_count):
                person_data.append(f.read(read_size))
        return person_data
    person_data = person_loader(file, scenario)

    persons = load_person(person_data, s1_format, S1Person)
    print_table(s1_table_title, s1_headers, persons)


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
@click.option('-t', '--taiki-file', 'taiki_file', help="待機檔案", required=True)
def san2_person(file, taiki_file):
    """
    人物資料解析

    dekoei.py san2 person -f ~/dosbox/SAN2/SCENARIO.DAT -t ~/DOSBox/san2/TAIKI.DAT
    """

    def person_loader(file, taiki_file):
        offsets = [0x0, 0x33af, 0x675e, 0x9b0d, 0xcebc, 0x1026b]  # size=0x33af per scenario
        read_count, read_size = 215, struct.calcsize(s2_format)  # count=215
        tf_read_count, tf_read_size = 420, struct.calcsize(s2_format_taiki)  # count=420
        person_data = []
        kaos = set()  # 用來過濾重複
        with open(file, 'rb') as f, open(taiki_file, 'rb') as tf:
            for offset in offsets:
                f.seek(offset+0x16)
                for _ in range(read_count):
                    pd = f.read(read_size)
                    if pd[26:28] in kaos:  # [26:28]
                        continue
                    if pd[28:32] == b'\x00\x00\x00\x00':
                        break
                    person_data.append(b''.join([b'\xFF\xFF\xFF', pd]))
                    kaos.add(pd[26:28])
            tf.seek(0x6)
            for _ in range(tf_read_count):
                pd = tf.read(tf_read_size)
                if pd[29:31] in kaos:  # [29:31]
                    continue
                if pd[31:35] == b'\x00\x00\x00\x00':
                    break
                person_data.append(pd)
                kaos.add(pd[29:31])
        return person_data
    person_data = person_loader(file, taiki_file)

    persons = load_person(person_data, s2_format_taiki, S2Person)
    # print_csv(s2_headers, persons)
    print_table(s2_table_title, s2_headers, persons)


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

    def person_loader(file):
        read_count, read_size = 600, struct.calcsize(s3_format)
        person_data = []
        with open(file, 'rb') as f:
            for _ in range(read_count):
                pd = f.read(read_size)
                if pd[43:] == b'\x00\x00\x00\x00\x00\x00':
                    continue
                person_data.append(pd)
        return person_data
    person_data = person_loader(file)

    persons = load_person(person_data, s3_format, S3Person)
    print_table(s3_table_title, s3_headers, persons)


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
@click.option('-f', '--face', 'face_file', help="頭像檔案")
@click.option('-p', '--palette', 'palette_file', default='Palette.S6', help="色盤檔案")
@click.option('--out_dir', 'out_dir', default='_output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def san6_face(game_dir, face_file, palette_file, out_dir, prefix):
    """
    ./dekoei.py san6 face -d /Volumes/common/San6WPK/
    """
    if game_dir is not None:
        palette_file = os.path.join(game_dir, 'Palette.S6')
        face_file = os.path.join(game_dir, 'Kaodata.s6')

    palette: list
    with open(palette_file, 'rb') as f:
        f.read(4)  # 0x00030001
        raw_data = f.read(1024)
        palette = list(grouper(raw_data, 4))

    face_w, face_h = 96, 120

    def loader() -> bytes:
        with open(face_file, 'rb') as f:
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

##############################################################################


@click.group()
def san7():
    """三國志VII"""
    pass


@click.command(help='顏 CG 解析')
@click.option('-d', '--dir', 'game_dir', help="遊戲目錄")
@click.option('-f', '--face', 'face_file', help="頭像檔案")
@click.option('-p', '--palette', 'palette_file', default='P_Kao.s7', help="色盤檔案")
@click.option('--out_dir', 'out_dir', default='_output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def san7_face(game_dir, face_file, palette_file, out_dir, prefix):
    """
    P_Kao.s7    Palette file
    Kaodata.s7  KAO file

    ./dekoei.py san7 face -d /Volumes/common/San7WPK/
    """
    if game_dir is not None:
        palette_file = os.path.join(game_dir, 'P_Kao.s7')
        face_file = os.path.join(game_dir, 'Kaodata.s7')

    palette: list
    with open(palette_file, 'rb') as f:
        f.read(4)  # 0x00030001
        raw_data = f.read(1024)
        palette = list(grouper(raw_data, 4))

    face_w, face_h = 96, 120

    def loader() -> bytes:
        with open(face_file, 'rb') as f:
            """
            KAODATA.S7

            CNT             4       bytes  # 0xA602 = 678
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


san7.add_command(san7_face, 'face')

##############################################################################


@click.group()
def san8():
    """三國志VIII"""
    pass


@click.command(help='顏 CG 解析')
@click.option('-d', '--dir', 'game_dir', help="遊戲目錄")
@click.option('-f', '--face', 'face_file', help="頭像檔案")
@click.option('-p', '--palette', 'palette_file', default='P_Kao.s7', help="色盤檔案")
@click.option('-s', '--size', 'size', default='small', help="頭像大小 (small, large)")
@click.option('--out_dir', 'out_dir', default='_output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def san8_face(game_dir, face_file, palette_file, size, out_dir, prefix):
    """
    P_MAIN.S8       Palette file
    g_maindy.s8     Kao file

    ./dekoei.py san8 face -d /Volumes/common/San8WPK/
    """
    is_large = True if size.lower() == 'large' else False

    if game_dir is not None:
        palette_file = os.path.join(game_dir, 'P_MAIN.S8')
        face_file = os.path.join(game_dir, 'g_maindy.s8')

    palette: list
    with open(palette_file, 'rb') as f:
        """
        P_MAIN.S8

        MAGIC WORD      8       bytes  # 0x4B4F4549 = 'KOEI'
        OFFSET          8       bytes  # 0x4C06 = 1612
        SIZE            8       bytes  # size of BOFFSETS (block offsets), 0x3406 = 1588
        BOFFSETS        4x397   bytes  # 397 = SIZE / 4
        UNKNOWN        12       bytes  # 0xFFFFFFFF 0x00000000 0x00000000

        BLOCK N      1024       bytes  # offset = OFFSET + BOFFSETS[N] + 12
                                       # size = BOFFSETS[N+1] - BOFFSETS[N]

        KAO PALETTE = BLOCK 4 (0-base)
        """
        f.seek(5720)  # 4096(BOFFSETS[4]) + 1612 + 12
        raw_data = f.read(1024)
        palette = list(grouper(raw_data, 4))

    face_w, face_h = 64, 80  # 小頭像
    offset = 24374192  # 9380 + 24364800 + 12 = 24,374,192
    if is_large:
        face_w, face_h = 160, 180  # 大頭像
        offset = 9380+12

    def loader() -> bytes:
        with open(face_file, 'rb') as f:
            count = 846
            f.seek(offset)
            return f.read(face_w * face_h * count)

    extract_images('', face_w, face_h, palette, out_dir, prefix, data_loader=loader)


san8.add_command(san8_face, 'face')

##############################################################################


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


@click.command(help="顏CG解析")
@click.option('-d', '--dir', 'game_dir', help="遊戲目錄")
@click.option('-p', '--palette', 'palette_file', help="色盤", required=True)
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='_output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
@click.option('--image-size',
              type=click.Choice(['L', 'S', 'T'], case_sensitive=False),
              help='頭像尺寸 L 240x240,\n S:  64x 80,\n T: 32x40')
def san9_face(game_dir, palette_file, face_file, image_size, out_dir, prefix):
    """三國志 IX 頭像解析

    dekoei.py san9 face -p KAO/SAN9_P_Face.s9 -f KAO/SAN9_G_FaceL.s9  -t SAN9L   --image-size=L --prefix "SAN9_WIN_FL"
    dekoei.py san9 face -p KAO/SAN9_P_Face.s9 -f KAO/SAN9_G_FacLPK.s9 -t SAN9PKL --image-size=L --prefix "SAN9PK_WIN_FL"
    dekoei.py san9 face -p KAO/SAN9_P_Face.s9 -f KAO/SAN9_G_FaceS.s9  -t SAN9S   --image-size=S --prefix "SAN9_WIN_FS"
    dekoei.py san9 face -p KAO/SAN9_P_Face.s9 -f KAO/SAN9_G_FacSPK.s9 -t SAN9PKS --image-size=S --prefix "SAN9PK_WIN_FS"
    dekoei.py san9 face -p KAO/SAN9_P_Face.s9 -f KAO/SAN9_G_FaceT.s9  -t SAN9T   --image-size=T --prefix "SAN9_WIN_FT"
    dekoei.py san9 face -p KAO/SAN9_P_Face.s9 -f KAO/SAN9_G_FacTPK.s9 -t SAN9PKT --image-size=T --prefix "SAN9PK_WIN_FT"

    ./dekoei.py san9 face -p /Volumes/common/San9WPK/P_Face.s9 -f /Volumes/common/San9WPK/G_FaceS.s9 --image-size=S
    ./dekoei.py san9 face -p /Volumes/common/San9WPK/P_Face.s9 -f /Volumes/common/San9WPK/G_FaceL.s9 --image-size=L
    """
    palette: list
    with open(palette_file, 'rb') as f:
        f.seek(44)
        raw_data = f.read(1024)
        palette = list(grouper(raw_data, 4))

    image_size_spec = {"L": (240, 240), "S": (64, 80), "T": (32, 40)}
    face_w, face_h = image_size_spec[image_size]

    # TODO(yuxioz):
    #   - [ ] loader 應該改用 iterator/generator 方式重寫過，不要一次回傳一大塊 bytes
    #   - [ ] 改使用 game_dir, 指定色盤與頭像檔太繁瑣
    #   - [ ] 將 6,7,8,9 的 load palette 抽出
    def loader() -> bytes:
        with open(face_file, 'rb') as f:
            data_size = face_w * face_h
            file_size = os.stat(face_file).st_size
            count = file_size // data_size

            f.seek(4)  # skip header
            face_data = bytearray()
            for _ in range(count):
                f.read(16)  # skip info(block_size, ?, width, height)
                face_data.extend(f.read(data_size))
            return bytes(face_data)

    extract_images('', face_w, face_h, palette, out_dir, prefix, data_loader=loader)


@click.command()
def san9_person():
    pass


san9.add_command(san9_face, "face")
san9.add_command(san9_person, "person")
