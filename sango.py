import click
from utils import *


@click.group()
def san1():
    """三國志（初代）

    SAN_B/PICDATA.DAT

    ./dekoei.py san1 face -f kao/三國志b.fdi
    ./dekoei.py san1 face -f kao/SAN1_DOS_PICDATA.DAT
    """
    pass


@click.command(help='顏 CG 解析')
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='output', help='output directory')
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

        def pc98_loader() -> bytes:
            raw_data = bytearray()
            offset_infos = [(15360, 113*1440)]  # (offset, face_count * part_size)
            with open(face_file, 'rb') as f:
                for info in offset_infos:
                    f.seek(info[0])
                    raw_data.extend(f.read(info[1]))
            return bytes(raw_data)
        loader = pc98_loader

    extract_images(face_file, face_w, face_h, palette, out_dir, prefix, num_part=num_part, hh=True, data_loader=loader)


san1.add_command(san1_face, 'face')

##############################################################################


@click.group()
def san2():
    """三國志II

    KAODATA.DAT

    ./dekoei.py san2 face -f kao/SAN2_DOS_KAODATA.DAT
    ./dekoei.py san2 face -f kao/SAN2_PC98_三國志2_b.fdi
    """
    pass


@click.command(help='顏 CG 解析')
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='output', help='output directory')
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

        def pc98_loader() -> bytes:
            raw_data = bytearray()
            # NOTE: 在第二組 offset_info 之後還有 52 個 face 大小的 montage 資料
            offset_infos = [(189440, 95*1920), (372736, 124*1920)]  # (offset, face_count * part_size)
            with open(face_file, 'rb') as f:
                for info in offset_infos:
                    f.seek(info[0])
                    raw_data.extend(f.read(info[1]))
            return bytes(raw_data)
        loader = pc98_loader

    extract_images(face_file, face_w, face_h, palette, out_dir, prefix, hh=hh, data_loader=loader)


san2.add_command(san2_face, 'face')

##############################################################################


@click.group()
def san3():
    """三國志III

    ./dekoei.py san3 face -f kao/SAN3_KAODATA.DAT --out_dir SAN3_DOS --prefix "SAN3_DOS_F"
    ./dekoei.py san3 face -f kao/SAN3_FACES.BMP --out_dir SAN3_WIN --prefix "SAN3_WIN_F"
    """
    pass


@click.command(help='顏 CG 解析')
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='output', help='output directory')
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


san3.add_command(san3_face, 'face')

##############################################################################


@click.group()
def san4():
    """三國志IV"""
    pass


@click.command(help='顏 CG 解析')
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def san4_face(face_file, out_dir, prefix):
    """

    # color pallete (威力加強版編輯器)
    #   | 黑[0] | 深藍[4] | 朱紅[2] | 深皮[6] |
    #   | 綠[1] | 淺藍[5] | 淺皮[3] | 雪白[7] |
    """
    pass


san4.add_command(san4_face, 'face')

##############################################################################


@click.group()
def san5():
    """三國志V"""
    pass


@click.command(help='顏 CG 解析')
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def san5_face(face_file, out_dir, prefix):
    pass


san5.add_command(san5_face, 'face')

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
