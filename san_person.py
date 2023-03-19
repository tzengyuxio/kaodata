from collections import namedtuple
from utils import H, to_unicode_name, kao2str

##############################################################################
# Common data
# - `~format` for struct unpack
# - `~PersonRaw`
# - `~Person`
# - `~table_title`
# - `~headers`

##############################################################################
# 三國志
#
# SINADATA.DAT:4326
#
# 43616F20 43616F00 00000000 23585D5E 64616403 03001027 07010A0A 0A000000
# 53756E20 4A69616E 00000000 22255560 621A6403 08008813 29020A0A 0A000000
# 4C697520 42656900 00000000 1D555F3F 63476403 0200F401 0E030A0A 0A000000
# N                          A B I P  C L L ?  F   S    C N S S  S ? ? ?
# a                          g o n o  h u o U  a   o    i a . .  .
# m                          e d t w  a c y 1  c   l    t t L A  A
# e                            y e e  r k a    e   d    y i o b  r
#                                l r  i   l        i      o y i  m
#                                l    s   t        e      n a l  s
#                                .    m   y        r        l i
#                                     a            s        t t
#                                                           y y
#

s1_format = '<12sbBBBBBBBHHBBBBBxxx'  # 32 bytes

S1PersonRaw = namedtuple(
    'S1PersonRaw', 'name age body intell power charisma luck loyalty unknown1 face soldiers city nation s_loyalty s_ability s_arms')


class S1Person(S1PersonRaw):
    id: int

    def __getitem__(self, key):
        if key == 'name':
            return to_unicode_name(self.name)
        if key == 'face':
            return kao2str(self.face, 255)
        if key == 'master':
            return '◎' if self.unknown1 & 0b10 else ''
        if key == 'naval':
            return '○' if self.unknown1 & 0b01 else ''
        if hasattr(self, key):
            return str(getattr(self, key))
        else:
            raise KeyError(key)


s1_table_title = '三國志 人物表'
s1_headers = [H('id', 'ID', 'id'), H('name', '姓名', 'name'), H('face', '顏', 'face'),
              H('age', '年齡', 'base'),
              H('body', '身體', 'base'),
              H('intell', '知力', 'base'),
              H('power', '武力', 'base'),
              H('charisma', '信服力', 'base'),
              H('luck', '運勢', 'base'),
              H('loyalty', '忠誠度', 'state'),
              H('city', '城市', 'state'),
              H('nation', '勢力', 'state'),
              H('master', '君主', 'state'),
              H('naval', '水軍', ''),
              H('soldiers', '兵士數', 'state'),
              H('s_loyalty', '兵忠誠', 'state'),
              H('s_ability', '兵武力', 'state'),
              H('s_arms', '兵武裝', 'state'),
              #   H('unknown1', '未知1', ''),
              ]

##############################################################################
# 三國志II
#

s2_format = '<12sbBBBBBBBHHBBBBBxxx'  # 32 bytes

S2PersonRaw = namedtuple(
    'S2PersonRaw', 'name age body intell power charisma luck loyalty unknown1 face soldiers city nation s_loyalty s_ability s_arms')


class S2Person(S2PersonRaw):
    id: int

    def __getitem__(self, key):
        if key == 'name':
            return to_unicode_name(self.name)
        if key == 'master':
            return '◎' if self.unknown1 & 0b10 else ''
        if key == 'naval':
            return '○' if self.unknown1 & 0b01 else ''
        if hasattr(self, key):
            return str(getattr(self, key))
        else:
            raise KeyError(key)


s2_table_title = '三國志 人物表'
s2_headers = [H('id', 'ID', 'id'), H('name', '姓名', 'name'), H('face', '顏', 'face'),
              H('age', '年齡', 'base'),
              H('body', '身體', 'base'),
              H('intell', '知力', 'base'),
              H('power', '武力', 'base'),
              H('charisma', '信服力', 'base'),
              H('luck', '運勢', 'base'),
              H('loyalty', '忠誠度', 'state'),
              H('city', '城市', 'state'),
              H('nation', '勢力', 'state'),
              H('master', '君主', 'state'),
              H('naval', '水軍', ''),
              H('soldiers', '兵士數', 'state'),
              H('s_loyalty', '兵忠誠', 'state'),
              H('s_ability', '兵武力', 'state'),
              H('s_arms', '兵武裝', 'state'),
              #   H('unknown1', '未知1', ''),
              ]

##############################################################################
# 三國志III
#
# 0x0000 顏 次席 士兵 寶物 MASK STATUS ABILITY 相性 義理 忠誠 城市 勢力 仕官 裡所屬士官 親族 訓練 士氣 無 生年 工作 餘月 無 姓名
# xx     H  H   H   H   H    BBBBB  BBBBBB   B   B   B   B   B   B    BB       B   B   B   xxx B   B   B   xxx 6s
#
# STATUS: 行動 疾病 壽命 埋伏 身份 (action disease lifespan undercover position)

s3_format = '<xxHHHHHBBBBBBBBBBBBBBBBBBBBBBxxxBBBxxx6s'  # 49 bytes

S3PersonRaw = namedtuple('S3PersonRaw', 'face next sldr items mask action disease lifespan undercover position army navy war intl pol chrm aishou giri loyalty city nation service in_nation in_service family discipline morale birth_year work left_month name')


class S3Person(S3PersonRaw):
    id: int

    def __getitem__(self, key):
        if key == 'name':
            return to_unicode_name(self.name)
        if key == 'face':
            return kao2str(self.face, 307, True)
        if key == 'ambition':
            return str((self.mask & 0b11000000) >> 6)
        if key == 'luck':
            return str((self.mask & 0b00110000) >> 4)
        if key == 'calmness':
            return str((self.mask & 0b00001100) >> 2)
        if key == 'bravery':
            return str((self.mask & 0b00000011) >> 0)
        if hasattr(self, key):
            return str(getattr(self, key))
        else:
            raise KeyError(key)


s3_table_title = '三國志III 人物表'
s3_headers = [H('id', 'ID', 'id'), H('name', '姓名', 'name'), H('face', '顏', 'face'),
              H('ambition', '野心', 'mask'),
              H('luck', '運氣', 'mask'),
              H('calmness', '冷靜', 'mask'),
              H('bravery', '勇猛', 'mask'),
              H('army', '陸指', 'base'),
              H('navy', '水指', 'base'),
              H('war', '武力', 'base'),
              H('intl', '智力', 'base'),
              H('pol', '政治', 'base'),
              H('chrm', '魅力', 'base'),
              H('aishou', '相性', 'mask'),
              H('giri', '義理', 'mask'),
              ]
