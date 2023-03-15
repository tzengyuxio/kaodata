from utils import *

cns11643_unicode_table = {}

# hanzi: (big5, koei-tw)
ctable = {
    "三": ("A454", "92B4"),  # LEMPE
    "卡": ("A564", "93A5"),  # LEMPE
    "世": ("A540", "9381"),  # LEMPE
    "四": ("A57C", "93BD"),  # LEMPE
    "治": ("AA76", "97D8"),  # LEMPE
    "洛": ("ACA5", "99A7"),  # LEMPE
    "娜": ("AE52", "9AF3"),  # LEMPE
    "拿": ("AEB3", "9B71"),  # LEMPE
    "破": ("AF7D", "9C31"),  # LEMPE
    "崙": ("B15B", "9DA0"),  # LEMPE
    "喬": ("B3EC", "9FD1"),  # LEMPE
    "琳": ("B559", "A0DE"),  # LEMPE, SAN3
    "維": ("BAFB", "A5C3"),  # LEMPE
    "多": ("A668", "948A"),  # LEMPE
    "亞": ("A8C8", "968A"),  # LEMPE
    "袁": ("B04B", "9CAF"),  # SAN3
    "紹": ("B2D0", "9ED4"),  # SAN3
    "曹": ("B1E4", "9E39"),  # SAN3
    "操": ("BEDE", "A8E6"),  # SAN3
    "術": ("B34E", "9F4A"),  # SAN3
    "劉": ("BC42", "A6AB"),  # SAN3
    "表": ("AAED", "986C"),  # SAN3
    "備": ("B3C6", "9FAB"),  # SAN3
    "孫": ("AE5D", "9B30"),  # SAN3
    "公": ("A4BD", "92FB"),  # SAN3
    "王": ("A4FD", "937A"),  # SAN3
    "馬": ("B0A8", "9CEA"),  # SAN3
    "孔": ("A4D5", "934C"),  # SAN3
    "華": ("B5D8", "A17A"),  # SAN3
    "太": ("A4D3", "934A"),  # SAN3
    "尚": ("A97C", "96FD"),  # SAN3
    "黃": ("B6C0", "A236"),  # SAN3
    "良": ("A87D", "9656"),  # SAN3
    "陶": ("B3B3", "9F98"),  # SAN3
    "伊": ("A5EC", "9444"),  # nobu4
    "達": ("B946", "A444"),  # nobu4
    "宗": ("A976", "96F7"),  # nobu4
    "中": ("A4A4", "92E2"),  # nobu4
    "野": ("B3A5", "9F8A"),  # nobu4
    "張": ("B169", "9DAE"),  # SAN3
    "飛": ("ADB8", "9A9A"),  # SAN3
    "周": ("A950", "96D1"),  # SAN3
    "倉": ("ADDC", "9ABE"),  # SAN3
    "胡": ("AD4A", "9A43"),  # SAN3, 車兒 966B 96A2
    "宮": ("AE63", "9B36"),  # SAN3, 陳 9F94
    "島": ("AE71", "9B4B"),  # nobu4, 津 999E
    "義": ("B871", "A399"),  # nobu4
    "時": ("AEC9", "9B8C"),  # nobu4
    "泰": ("AEF5", "9BB8"),  # SAN3
    "班": ("AF5A", "9BDC"),  # SAN3, 吳 9562
    "祖": ("AFAA", "9C43"),  # SAN3, 黃 A236
    "純": ("AFC2", "9C61"),  # SAN3
    "蔣": ("BDB1", "A7D9"),  # SAN3, 琬 BEA0
    "蔡": ("BDB2", "A7DA"),  # SAN3, 瑁 A346
    "蒙": ("BB58", "A5DF"),  # SAN3, 呂 9564
    "褚": ("BB75", "A5FC"),  # SAN3, 許褚 9F58
    "遜": ("BBB9", "A657"),  # SAN3, 陸 9F95
    "審": ("BC66", "A6CF"),  # SAN3, 配 9CD8
    "德": ("BC77", "A6E0"),  # SAN3, 龐 ACB1
    "樂": ("BCD6", "A756"),  # SAN3, 進 A1CF
    # "群": ("B873", "9A95"),  # SAN3, 陳 9F94
    "會": ("B77C", "A2C3"),  # SAN3, 鍾 AB95
    "當": ("B7ED", "A34B"),  # SAN3, 韓 ABA6
    "雲": ("B6B3", "A1F7"),  # SAN3
    "賈": ("B8EB", "A3F1"),  # SAN3, 詡 C36A
    "宋": ("A7BA", "959B"),  # SUI
    "江": ("A6BF", "94BF"),  # SUI
    "魯": ("BE7C", "A8A6"),  # SUI
    "智": ("B4BC", "A082"),  # SUI
    "深": ("B260", "9E86"),  # SUI
    "高": ("B0AA", "9CEC"),  # SUI
    "俅": ("CDDE", "B3FD"),  # SUI
    "美": ("ACFC", "9A30"),  # nobu4 宇佐美 A674 A6F5 ACFC, 949694F59A30
    "納": ("AFC7", "9C66"),  # nobu4 新納 忠元 B773 AFC7 A9BE A4B8, A2BA9C66
    "荀": ("AFFB", "9CA0"),  # SAN3, 荀彧 _, 9CA0B6FC
    "彧": ("D17B", "B6FC"),  # SAN3, 荀彧 _, 9CA0B6FC
    "髦": ("BBEC", "A696"),  # SAN3, 髦
    "尹": ("A4A8", "92E6"),  # SAN3, 尹賞 _, 92E6A841
    "賞": ("BDE0", "A841"),  # SAN3, 尹賞 _, 92E6A841
    "耿": ("AFD5", "9C75"),  # SAN3, 耿武 _, 9C7597BC
    "武": ("AA5A", "97BC"),  # SAN3, 耿武 _, 9C7597BC
    "震": ("BE5F", "A889"),  # SAN3
    "鄭": ("BE47", "A86D"),  # SAN3, 鄭度 _, A86D98F8
    "度": ("ABD7", "98F8"),  # SAN3, 鄭度 _, A86D98F8
    "潘": ("BCEF", "A775"),  # SAN3, 潘濬 _, A775AAAA
    "濬": ("C0E0", "AAAA"),  # SAN3, 潘濬 _, A775AAAA
    "郭": ("B3A2", "9F87"),  # SAN3, 郭汜 _, 9F87B0DA
    "汜": ("C9FA", "B0DA"),  # SAN3, 郭汜 _, 9F87B0DA
    "張": ("B169", "9DAE"),  # SAN3, 張繡(縤) _, 9DAECC66
    "縤": ("EADE", "CC66"),  # SAN3, 張繡(縤) _, 9DAECC66
    "步": ("A842", "95E2"),  # SAN3, 步騭 _, 95E2D4F0
    "騭": ("F563", "D4F0"),  # SAN3, 步騭 _, 95E2D4F0
    "申": ("A5D3", "93F2"),  # SAN3, 申耽 _, 93F29C74
    "耽": ("AFD4", "9C74"),  # SAN3, 申耽 _, 93F29C74
    "雷": ("B970", "A474"),  # SAN3, 雷銅 _, A474A66E
    "銅": ("BBC9", "A66E"),  # SAN3, 雷銅 _, A474A66E
    "鄧": ("BE48", "A86E"),  # SAN3, 鄧賢 _, A86EA846
    "賢": ("BDE5", "A846"),  # SAN3, 鄧賢 _, A86EA846
    "嚴": ("C459", "AD85"),  # SAN3, 嚴輿 _, AD85AB82
    "輿": ("C1D6", "AB82"),  # SAN3, 嚴輿 _, AD85AB82
    "程": ("B57B", "A132"),  # SAN3, 程銀 _, A132A66D
    "銀": ("BBC8", "A66D"),  # SAN3, 程銀 _, A132A66D
    "卓": ("A8F4", "96B6"),  # SAN3, 卓膺 _, 96B6AAFD
    "膺": ("C174", "AAFD"),  # SAN3, 卓膺 _, 96B6AAFD
    "魏": ("C351", "AC9C"),  # SAN3, 魏續 _, AC9CADFC
    "續": ("C4F2", "ADFC"),  # SAN3, 魏續 _, AC9CADFC
    "觀": ("C65B", "AF37"),  # SAN3, 孫觀 _, 9B30AF37
    "夏": ("AE4C", "9AED"),  # SAN3, 夏侯楙 _, 9AED9AB6C177
    "候": ("ADD4", "9AB6"),  # SAN3, 夏侯楙(候) _, 9AED9AB6C177
    "楙": ("DDD5", "C177"),  # SAN3, 夏侯楙 _, 9AED9AB6C177
    "謝": ("C1C2", "AB69"),  # SAN3, 謝旌 _, AB699E31
    "旌": ("B1DC", "9E31"),  # SAN3, 謝旌 _, AB699E31
    "薛": ("C1A7", "AB47"),  # SAN3, 薛悌 _, AB479B6B
    "悌": ("AEAD", "9B6B"),  # SAN3, 薛悌 _, AB479B6B
    "禮": ("C2A7", "ABF0"),  # SAN3, 薛禮 _, AB47ABF0
    "田": ("A5D0", "93EF"),  # SAN3, 田豐 _, 93EFAC58
    "豐": ("C2D7", "AC58"),  # SAN3, 田豐 _, 93EFAC58
    "瓚": ("C5D0", "AEBB"),  # SAN3
    "翊": ("D6F6", "BBBA"),  # SAN3
    "詡": ("E048", "C36A")  # SAN3
    # "春": ("AC4B", "9999"),  #
    # "秋": ("ACEE", "9999"),  #
    # "冬": ("A556", "9999"),  #
    # "莉": ("B2FA", "9549")  # 漢字部分不確定
    # 徐庶 (KOEI)9B579DAB
    # "徐": ("A8A4", "9650"),  # AI
    # 鄒靖 (KOEI)A44FA478
    # "鄒": ("A8A4", "9650"),  # AI
    # 趙雲 (KOEI)A64DA1F7
}


def test_to_indexes():
    # test of to_2bpp_indexes
    data = bytes(b'\x42\x04\x53\x0A')
    expected = [0, 2, 0, 0, 0, 1, 2, 0, 0, 2, 0, 2, 1, 0, 3, 2]
    assert to_2bpp_indexes(data) == expected

    # test of to_3bpp_indexes
    data = bytes(b'\x00\xFF\xAA\x57\x02\x00')
    expected = [3, 2, 3, 2, 3, 2, 3, 2, 0, 4, 0, 4, 0, 4, 6, 4]
    assert to_3bpp_indexes(data) == expected


def test_to_2bpp_indexes():
    # Test 1: Test if the function returns a list of integers for a given input
    assert isinstance(to_2bpp_indexes(b'\x00\x01\x02\x03'), list)
    assert all(isinstance(i, int) for i in to_2bpp_indexes(b'\x00\x01\x02\x03'))

    # Test 2: Test if the function returns an empty list for an empty input
    assert to_2bpp_indexes(b'') == []

    # Test 3: Test if the function correctly handles incomplete bytes in the input data
    assert to_2bpp_indexes(b'\x01\x02\x03') == [0, 0, 0, 0, 0, 0, 1, 2]
    assert to_2bpp_indexes(b'\x01\x02\x03\x04\x05') == [0, 0, 0, 0, 0, 0, 1, 2,
                                                        0, 0, 0, 0, 0, 1, 2, 2]

    # Test 4: Test if the function correctly converts the input data into 2bpp indexes
    assert to_2bpp_indexes(b'\x00\x00\x00\x00') == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert to_2bpp_indexes(b'\xFF\xFF\xFF\xFF') == [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    assert to_2bpp_indexes(b'\xAA\x55\xAA\x55') == [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]


def test_order_of_big5():
    # Test 1: Test if the function returns an integer for a given input
    assert isinstance(order_of_big5(0x0001), int)

    # Test 2: Test normal input
    assert order_of_big5(0xA440) == 0    # A440 一 0
    assert order_of_big5(0xB0A1) == 1947  # B0A1 陛 1947
    assert order_of_big5(0xB0AF) == 1961  # B0AF 偺
    assert order_of_big5(0xB1D7) == 2158  # B1D7 斜

    # Test 3: Test edge cases
    assert order_of_big5(0xA140) == -1


def test_ctable():
    # list relation and verify
    # 列出關係與驗證
    global cns11643_unicode_table
    if len(cns11643_unicode_table) == 0:
        cns11643_unicode_table = load_cns11643_unicode_table()

    for k in sorted(ctable.keys(), key=lambda x: order_of_koei_tw(ctable[x][0])):
        v = ctable[k]
        order = order_of_koei_tw(int(v[1], 16))
        cns_code = cns_from_order(order)
        assert cns11643_unicode_table[cns_code] == k
