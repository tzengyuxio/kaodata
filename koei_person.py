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
# 拿破崙
#
# NPDATA.CIM:8934
#
# 4E61706F 6C656F6E 00000000 0000005F 06  # BCBA AACA 1111
# 4E61706F 6C656F6E 00000000 0000005F 06  # start[22204]
# 4E61706F 6C656F6E 00000000 0000005F 06  # start[35474]
# 4E61706F 6C656F6E 00000000 0000005F 06  # start[48744]
# 4E61706F 6C656F6E 00000000 0000005F 06  # start[62014]
#  N a p o  l e o n
#
# 4A6F7365 70680000 00000000 00000103 06  # CCCB CCDD 0000, 2nd, Joseph
# 4C756369 656E0000 00000000 00000203 06  # BBCC CDDD 0000, 3rd, Lucien
# 42657274 68696572 00000000 00000842 06  # CCAB ACDC 1000, 9th, Berthier
# 57697474 67656E73 7465696E 00007201 06  # CDBC BBCB 0000, Wittgenstein
# 47656F72 67652049 49490000 00003A82 06  # George III
# 47656F72 67652049 56000000 00003B82 00  # George IV
# 56696374 6F726961 00000000 00003C5E 00  # Victoria
# 4B757475 736F7600 00000000 00006346 06  # Kutusov (single eye?)
# 42617272 61730000 00000000 00000B20 06  # Barras
# 4C656665 62767265 00000000 00000C12 06  # Lefebvre -o--
# 41756765 72656175 00000000 00000D81 06  # Augereau x---
# ^^^^^^^^ ^^^^^^^^ ^^^^^^^^     ^^
# 名字                            序號
#
# NPDATA.CIM:8934
#
# 00 1AE6DF00 411C0505 00525705 0000 # BCBA AACA 1111, 1769
# 00 1B950500 491E0500 00303904 0000 # CCCB CCDD 0000, 1768
# 00 1B5A0100 42170000 00000004 0000 # BBCC CDDD 0000, 1775
# 00 1E610500 31140000 00000000 0000 # CDBC CCDD 0000, 1778
# 00 1E515500 2D0E0000 00000000 0000 # CDCC CCCC -000, 1784
# 0E 04AF6A00 64E96464 00646401 0000 # AABB BBBC 1111, 1819
# ^^ ^ ^^^^   ^^  ^^     ^^^^
# 國 城 能     忠  兵      訓士
#             誠  力      練氣

lempe_format = '<14sBBxBBBBxBxBxxBBxxx'  # 32 bytes

LEMPEPersonRaw = namedtuple(
    'LEMPEPersonRaw', 'name face masks nation city ability1 ability2 loyalty soldiers discipline morale')


class LEMPEPerson(LEMPEPersonRaw):
    id: int
    lookups = {0: 'D', 1: 'C', 2: 'B', 3: 'A'}

    def __getitem__(self, key):
        if key == 'name':
            return to_unicode_name(self.name)
        if key == 'face':
            return kao2str(self.face, 255)
        if key == 'pol':  # politics
            v = (self.ability1 & 0b11000000) >> 6
            return self.lookups[v]
        if key == 'eco':  # economics
            v = (self.ability1 & 0b00110000) >> 4
            return self.lookups[v]
        if key == 'sup':  # support
            v = (self.ability1 & 0b00001100) >> 2
            return self.lookups[v]
        if key == 'bld':  # building
            v = (self.ability1 & 0b00000011)
            return self.lookups[v]
        if key == 'cmd':
            v = (self.ability2 & 0b11000000) >> 6
            return self.lookups[v]
        if key == 'inf':  # infantry
            v = (self.ability2 & 0b00110000) >> 4
            return self.lookups[v]
        if key == 'cav':  # cavalry
            v = (self.ability2 & 0b00001100) >> 2
            return self.lookups[v]
        if key == 'arty':  # artillery
            v = (self.ability2 & 0b00000011)
            return self.lookups[v]
        if key == 'calm':
            v = (self.masks & 0b11000000)
            return '冷靜' if v == 0b01000000 else '單純' if v == 0b10000000 else ''
        if key == 'brv':
            v = (self.masks & 0b00110000)
            return '勇氣' if v == 0b00010000 else '膽小' if v == 0b00100000 else ''
        if key == 'chrm':
            v = (self.masks & 0b00001000)
            return '魅力' if v else ''
        if key == 'luck':
            v = (self.masks & 0b00000100)
            return '幸運' if v else ''
        if hasattr(self, key):
            return str(getattr(self, key))
        else:
            raise KeyError(key)


lempe_table_title = '拿破崙 人物表'  # "L'Empereur Person Data Table"
lempe_headers = [H('id', 'ID', 'id'), H('name', '姓名', 'name'), H('face', '顏', 'face'),
                 H('pol', '政治', 'base'),
                 H('eco', '經濟', 'base'),
                 H('sup', '補給', 'base'),
                 H('bld', '建設', 'base'),
                 H('cmd', '統帥', 'base'),
                 H('inf', '步兵', 'base'),
                 H('cav', '騎兵', 'base'),
                 H('arty', '砲兵', 'base'),
                 H('calm', '冷靜', 'mask'),
                 H('brv', '勇敢', 'mask'),
                 H('chrm', '魅力', 'mask'),
                 H('luck', '幸運', 'mask'),
                 H('city', '城市', 'state'),
                 H('nation', '國籍', 'state'),
                 ]
