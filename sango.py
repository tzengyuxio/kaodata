import click
from utils import *


@click.group()
def san1():
    """三國志（初代）"""
    pass


@click.command(help='顏 CG 解析')
def san1_face():
    pass


san1.add_command(san1_face, 'face')

##############################################################################


@click.group()
def san2():
    """三國志II"""
    pass


@click.command(help='顏 CG 解析')
def san2_face():
    pass


san2.add_command(san2_face, 'face')

##############################################################################


@click.group()
def san3():
    """三國志III"""
    pass


@click.command(help='顏 CG 解析')
def san3_face():
    pass


san3.add_command(san3_face, 'face')

##############################################################################


@click.group()
def san6():
    """三國志VI"""
    pass


@click.command(help='顏 CG 解析')
@click.option('-d', '--dir', 'game_dir', help="遊戲目錄")
@click.option('-p', '--palette', 'palette_file', default='Palette.S6', help="色盤檔案")
@click.option('--out_dir', 'out_dir', default='output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def san6_face(game_dir, palette_file, out_dir, prefix):
    palette: list
    with open(palette_file, 'rb') as f:
        f.read(4)  # 0x00030001
        raw_data = f.read(1024)
        palette = list(grouper(raw_data, 4))

    face_w, face_h = 96, 120
    one_face_data_size = face_w*face_h

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

    extract_images('', face_w, face_h, palette, out_dir, prefix, one_face_data_size, data_loader=loader)


san6.add_command(san6_face, 'face')
