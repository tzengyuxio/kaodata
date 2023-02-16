import sys
from game_infos import GAME_INFOS

font_count = 0
font_codes = set()


def export_persons(tag, filename):
    game_info = GAME_INFOS[tag]["persons"]
    start_pos = game_info["start_pos"]
    person_count = game_info["data_count"]
    data_size = game_info["data_size"]

    with open(filename, 'rb') as f:
        data_array = [[] for _ in range(person_count)]
        num_blocks = len(start_pos)
        for i in range(num_blocks):
            f.seek(start_pos[i])
            for j in range(person_count):
                d = f.read(data_size[i])
                data_array[j].append(d)
                # print(i, j, len(d), len(data_array[j]))
                # print(data_array[j])

    for i in range(person_count):
        parse_lempe(data_array[i])


def unpack(b):
    ability = []
    t = ['D', 'C', 'B', 'A']
    for i in range(4):
        c = (b >> 2*i) & 0b00000011
        ability.append(t[c])
    return ability


def unpack_mask(b):
    masks = []
    b = b >> 2
    if b & 1:
        masks.append('幸運')
    else:
        masks.append('')
    b = b >> 1
    if b & 1:
        masks.append('魅力')
    else:
        masks.append('')
    b = b >> 1
    c = b & 3
    if c == 1:
        masks.append('勇氣')
    elif c == 2:
        masks.append('膽小')
    else:
        masks.append('')
    b = b >> 2
    c = b & 3
    if c == 1:
        masks.append('冷靜')
    elif c == 2:
        masks.append('單純')
    else:
        masks.append('')
    masks.reverse()
    return masks


def parse_lempe(data):
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
    # 00 1AE6DF00 411C0505 00525705 0000 # BCBA AACA 1111, 1769
    # 00 1B950500 491E0500 00303904 0000 # CCCB CCDD 0000, 1768
    # 00 1B5A0100 42170000 00000004 0000 # BBCC CDDD 0000, 1775
    # 00 1E610500 31140000 00000000 0000 # CDBC CCDD 0000, 1778
    # 00 1E515500 2D0E0000 00000000 0000 # CDCC CCCC -000, 1784
    # 0E 04AF6A00 64E96464 00646401 0000 # AABB BBBC 1111, 1819
    # ^^ ^ ^^^^   ^^  ^^     ^^^^
    # 國 城 能     忠  兵      訓士
    #             誠  力      練氣

    global font_count

    # [d1, d2]
    d1 = data[0]
    d2 = data[1]
    # name = str.rstrip(d1[:14].decode().replace('\x00', ''))
    # name = d1[:14].hex()
    name = to_unicode(d1[:14])
    for i in range(0, 14, 2):
        font_code = d1[i:i+2]
        if font_code != b'\x00\x00':
            font_count += 1
            font_codes.add(font_code.hex())
    nation = d2[0]
    city = d2[1]
    kao_id = d1[14]
    a1 = unpack(d2[2])  # 政治 經濟 補給 建設
    a2 = unpack(d2[3])  # 統帥 步兵 騎兵 砲兵
    masks = unpack_mask(d1[15])
    print('{:7s}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}'.format(
        name, nation, city, kao_id, *a1, *a2, *masks))

    print(font_count, len(font_codes))  # 861, 238


def count_big5(s):
    up = s[:2]
    dw = s[2:]
    a = int('0x'+up, 16) - int('0xa4', 16)
    bb = int('0x'+dw, 16)
    if bb > int('0xa1', 16):
        bb = bb - int('0xa1', 16) + 63
    else:
        bb = bb - int('0x40', 16)
    return (a * 157 + bb) + 1


def count_koei(s):
    up = s[:1]
    dw = s[1:]
    print(up, dw)
    a = int.from_bytes(up, 'big') - int('0x92', 16)
    bb = int.from_bytes(dw,'big')
    if bb > int('0x80', 16):
        bb = bb - int('0x80', 16) + 63
    else:
        bb = bb - int('0x40', 16)
    return (a * 188 + bb) + 1 - 95


def to_big5(n):
    y = n - 1
    a = y // 157
    b = y % 157
    print("[A&B]", a, b)
    up = int('0xa4', 16) + a
    dw = int('0x40', 16) + b if b < 64 else int('0xa1', 16) + (b-63)
    print("[U&D]", up, dw)
    c = (up * 256 + dw)
    d = c.to_bytes(2, 'big')
    print("[C&D]", c, d)
    return d.decode('big5')


def to_unicode(s):
    r = ''
    for i in range(0, 14, 2):
        font_code = s[i:i+2]
        if font_code == b'\x00\x00':
            continue
        font_no = count_koei(font_code)
        print('font_no', font_code, font_no)
        # r.append(to_big5(font_no))
        r += to_big5(font_no)
    return r


def main():
    args = sys.argv[1:]
    if len(args) == 2:
        export_persons(args[0], args[1])
    else:
        print("Usage: {} KEYWORD FILENAME".format(sys.argv[0]))

    # font test
    font_codes_list = list(font_codes)
    font_codes_list.sort()
    ftable = {}
    for x in font_codes_list:
        # print(x)
        dw = x[2:]
        if dw in ftable:
            ftable[dw] += 1
        else:
            ftable[dw] = 1
    for i in range(16):
        row = []
        for j in range(16):
            jj = hex(i*16 + j)
            if jj[2:] in ftable:
                row.append(ftable[jj[2:]])
            else:
                row.append(0)
        row2 = [x if x != 0 else ' ' for x in row]
        print('{:4s}: {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
            hex(i*16), *row2))
    # print(font_codes_list[0])
    # print(font_codes_list[-1])


if __name__ == '__main__':
    main()
