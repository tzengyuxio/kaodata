import sys
from PIL import Image
import os.path
import math

endian = 'little'

color_tab = set()


def nobu5():
    args = sys.argv[1:]
    # sep = b'\x00\x00\x00\x00\x40\x00\x50\x00'
    sep = b'\x40\x00\x50\x00'
    lsep = len(sep)
    tt = dict()
    with open(args[0], 'rb') as f:
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


def main():
    args = sys.argv[1:]


if __name__ == '__main__':
    main()

    # nobu5()

# GT1G0500 2C400000 20000000 01000000 00000000 00000000 00000000 04000000 10016600 00102100 B0-1 (64)
# GT1G0500 2C400000 20000000 01000000 00000000 00000000 00000000 04000000 10016600 00102100 B0-2
# G1TG0050 00000030 00000020 00000001 00000001 00000000 00000000 00000004 01010000 00011200 FF405154 <- 48bytes
# GT1G0500 2C100000 20000000 01000000 00000000 00000000 00000000 04000000 10015500 00102100 B1-1 (32)
# GT1G0500 2C001000 20000000 01000000 00000000 00000000 00000000 04000000 10019900 00102100 B2-1 (512)
#          ^^x4
#          16428
#          block size
