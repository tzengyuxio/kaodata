import os
import click

##############################################################################


@click.group()
def nobu3():
    """
    信長之野望II 戰國群雄傳

    "name": "信長之野望II 戰國群雄傳",
    "face_file": "KAODATA.DAT", # KAO_OE 僅有前 28 人
    "face_size": (64, 80),
    "face_count": 177, # 177 之後是大眾臉
    "double_height": True,
    "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55', '#5555FF', '#55FFFF', '#FF55FF', '#FFFFFF']
    """
    pass


@click.command(help='顏 CG 解析')
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='_output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def nobu3_face(face_file, out_dir, prefix):
    pass


@click.command(help='人物資料解析')
def nobu3_person():
    """
    人物資料解析
    """
    pass


nobu3.add_command(nobu3_face, 'face')
nobu3.add_command(nobu3_person, 'person')

##############################################################################


@click.group()
def nobu4():
    """
    信長之野望 武將風雲錄

    "name": "武將風雲錄",
    "face_file": "KAODATA.DAT",
    "face_size": (64, 80),
    "palette": ['#000000', '#00AA00', '#AA0000', '#FFFF00', '#0000AA', '#00AAAA', '#AA00AA', '#FFFFFF']
    """
    pass


@click.command(help='顏 CG 解析')
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='_output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def nobu4_face(face_file, out_dir, prefix):
    pass


@click.command(help='人物資料解析')
def nobu4_person():
    """
    人物資料解析
    """
    pass


nobu4.add_command(nobu4_face, 'face')
nobu4.add_command(nobu4_person, 'person')

##############################################################################


@click.group()
def nobu5():
    """
    信長之野望 霸王傳

    """
    pass


@click.command(help='顏 CG 解析')
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='_output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def nobu5_face(face_file, out_dir, prefix):
    pass


@click.command(help='人物資料解析')
def nobu5_person():
    """
    人物資料解析
    """
    pass


def nobu5_test(filename: str):
    # sep = b'\x00\x00\x00\x00\x40\x00\x50\x00'
    sep = b'\x40\x00\x50\x00'
    lsep = len(sep)
    tt = dict()
    with open(filename, 'rb') as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        f.seek(0)

        bs = f.read()
        i = 0
        old_pos = 0
        pos = bs.find(sep)
        while pos != -1:
            ss = pos+lsep-old_pos
            if ss in tt:
                tt[ss] += 1
            else:
                tt[ss] = 1
            f.seek(old_pos)
            nn = f.read(1)
            print('[{:04d}] {:8d}  {:8d} {:2d}(byte size)'.format(i, pos, ss, int.from_bytes(nn, 'big')))
            i += 1
            old_pos = pos + lsep
            pos = bs.find(sep, old_pos)
        print('[{:04d}] {:8d}  {:8d}'.format(i, pos, file_size-old_pos))

        # for k in sorted(tt.keys()):
        #     print("{:4d} : {:4d}".format(k, tt[k]))


nobu5.add_command(nobu5_face, 'face')
nobu5.add_command(nobu5_person, 'person')

# GT1G0500 2C400000 20000000 01000000 00000000 00000000 00000000 04000000 10016600 00102100 B0-1 (64)
# GT1G0500 2C400000 20000000 01000000 00000000 00000000 00000000 04000000 10016600 00102100 B0-2
# G1TG0050 00000030 00000020 00000001 00000001 00000000 00000000 00000004 01010000 00011200 FF405154 <- 48bytes
# GT1G0500 2C100000 20000000 01000000 00000000 00000000 00000000 04000000 10015500 00102100 B1-1 (32)
# GT1G0500 2C001000 20000000 01000000 00000000 00000000 00000000 04000000 10019900 00102100 B2-1 (512)
#          ^^x4
#          16428
#          block size

##############################################################################


@click.group()
def nobu6():
    """
    信長之野望 天翔記

    """
    pass


@click.command(help='顏 CG 解析')
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--out_dir', 'out_dir', default='_output', help='output directory')
@click.option('--prefix', 'prefix', default='', help='filename prefix of output files')
def nobu6_face(face_file, out_dir, prefix):
    pass


@click.command(help='人物資料解析')
def nobu6_person():
    """
    人物資料解析
    """
    pass


nobu6.add_command(nobu6_face, 'face')
nobu6.add_command(nobu6_person, 'person')
