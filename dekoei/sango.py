import click
from rich.console import Console
from utils import *
from san_person import *

console = Console()


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

    palette = load_palette_from_file(palette_file, 4)  # 4 bytes: 0x01000300
    face_w, face_h = 96, 120

    def stream() -> typing.Generator[bytes, None, None]:
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
            while data := f.read(96*120):
                yield data

    extract_images('', face_w, face_h, palette, out_dir, prefix, data_loader=stream)


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

    palette = load_palette_from_file(palette_file, 4)  # 4 bytes: 0x01000300
    face_w, face_h = 96, 120

    def stream() -> typing.Generator[bytes, None, None]:
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
            while data := f.read(96*120):
                yield data

    extract_images('', face_w, face_h, palette, out_dir, prefix, data_loader=stream)


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
    palette = load_palette_from_file(palette_file, 5720)  # 5720 = 4096 + 1612 + 12, 4096: BOFFSETS[4]

    face_w, face_h = 64, 80  # 小頭像
    offset = 24374192  # 9380 + 24364800 + 12 = 24,374,192
    if is_large:
        face_w, face_h = 160, 180  # 大頭像
        offset = 9380+12

    def stream() -> typing.Generator[bytes, None, None]:
        with open(face_file, 'rb') as f:
            count = 846
            f.seek(offset)
            for _ in range(count):
                yield f.read(face_w * face_h)

    extract_images('', face_w, face_h, palette, out_dir, prefix, data_loader=stream)


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
        P_Face.s9       武將CG色盤
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
    image_size_spec = {"L": (240, 240), "S": (64, 80), "T": (32, 40)}
    # face_filenames = {"L": "G_FaceL.s9", "S": "G_FaceS.s9", "T": "G_FaceT.s9"}
    pk_face_filenames = {"L": "G_FacLPK.s9", "S": "G_FacSPK.s9", "T": "G_FacTPK.s9"}

    if game_dir is not None:
        palette_file = os.path.join(game_dir, 'P_FACE.s9')
        face_file = os.path.join(game_dir, pk_face_filenames[image_size])

    palette = load_palette_from_file(palette_file, 44)
    face_w, face_h = image_size_spec[image_size]

    def stream() -> typing.Generator[bytes, None, None]:
        with open(face_file, 'rb') as f:
            data_size = face_w * face_h
            file_size = os.stat(face_file).st_size
            count = file_size // data_size

            f.seek(4)  # skip header
            for _ in range(count):
                f.read(16)  # skip info(block_size, ?, width, height)
                yield f.read(data_size)

    extract_images('', face_w, face_h, palette, out_dir, prefix, data_loader=stream)


@click.command()
def san9_person():
    pass


san9.add_command(san9_face, "face")
san9.add_command(san9_person, "person")
