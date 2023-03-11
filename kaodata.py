import sys
from game_infos import GAME_INFOS
from utils import *


# 成吉思汗
KHAN_KAODATA = "/Users/tzengyuxio/DOSBox/KHAN/KAODATA.DAT"
KHAN_PALETTE = ['#302000', '#417120', '#D33030', '#D3B282', '#204182', '#418292', '#C38251',
                '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白


# 成吉思涵 (色盤未確定)
# export_kaodata('KHAN', KHAN_KAODATA, KHAN_PALETTE)

# ----------------------------------------------------------------------

# 大航海時代
# export_faces('KOUKAI2I', '/Users/tzengyuxio/DOSBox/DAIKOH2', all_in_one=True) # items
# export_faces('KOUKAI2M', '/Users/tzengyuxio/DOSBox/DAIKOH2', all_in_one=True) # montage
# data = b'\x3C\x93\xF8\x17\x13\xF8\x3B\x2F\x13\xF8\x16\xC3'
# print(get_codes(data))


# 航空霸業II (尚未找到)
# export_faces('AIR2', '/Users/tzengyuxio/DOSBox/AIR2', all_in_one=True)

# ls11_decode('KAODATA/ISHIN2_FACE.I2', 'KAODATA/ISHIN2_FACE.DEC')


def main():
    args = sys.argv[1:]


if __name__ == '__main__':
    main()
