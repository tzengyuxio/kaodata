GAME_INFOS = {
    "EUROPE": {
        "name": "歐陸戰線",
        "face_file": "FACE.DAT",
        "face_size": (64, 80),
        "palette": ['#000000', '#419241', '#B24120', '#F3C361', '#104192', '#6FAEAE', '#D371B2', '#F3F3F3']
    },
    "GENGHIS": {
        "name": "蒼狼與白鹿 成吉思汗",  # 蒼狼與白鹿 成吉思汗, 系列第二作
        "face_file": "KAO.DAT",  # 中英文版相同
        "face_size": (64, 80),
        "double_height": True,
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55', '#5555FF', '#55FFFF', '#FF55FF', '#FFFFFF']
    },
    "GENCHOH": {
        "name": "蒼狼與白鹿 元朝秘史",  # 蒼狼與白鹿 元朝秘史, 系列第三作
        "face_file": "",
        "face_size": (64, 80),
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55', '#5555FF', '#55FFFF', '#FF55FF', '#FFFFFF']  # 未校色
    },
    "ISHIN": {
        "name": "維新之嵐",
        "face_file": "",
        "face_size": (48, 80),
        "face_count": 105,
        "double_height": True,
        "start_pos": 582656,
        "palette": ['#000000', '#00FF00', '#FF0000', '#FFFF00', '#0000FF', '#00FFFF', '#FF00FF', '#FFFFFF']
    },
    "KOHRYUKI": {
        "name": "項劉記",
        "face_file": "KAO.KR1",
        "face_size": (64, 80),
        "palette": ['#000000', '#418200', '#C34100', '#E3A251', '#0030A2', '#71A2B2', '#B27171', '#F3E3D3']
    },
    "KOUKAI": {
        "name": "大航海時代",
        "face_file": "KAO.PUT",
        "face_size": (64, 80),
        "face_count": 34,
        "double_height": True,
        "start_pos": 47616,
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55', '#5555FF', '#55FFFF', '#FF55FF', '#FFFFFF']
    },
    "KOUKAI2": {
        "name": "大航海時代II",
        "face_file": "KAO2.LZW",  # "KAO.LZW", 465890 bytes (KAO: first 210279 bytes, THEN: 864B x 128)
        "face_size": (64, 80),
        "face_count": 128,
        "ls11_encoded": True,
        "palette": ['#000000', '#00A261', '#D34100', '#F3A261', '#0041D3', '#00A2F3', '#D361A2', '#F3E3D3']
    },
    "KOUKAI2M": {
        "name": "大航海時代II",
        "face_file": "KAO.LZW",  # "KAO.LZW", 465890 bytes (LS11: first 292514 bytes, MONTAGE: 173376)
        "face_size": (64, 80),
        "start_pos": 292514,
        "ls11_encoded": True,
        "palette": ['#000000', '#00A261', '#D34100', '#F3A261', '#0041D3', '#00A2F3', '#D361A2', '#F3E3D3']
    },
    "KOUKAI2I": {
        "name": "大航海時代II 道具",
        "face_file": "KAO2.LZW",
        "face_size": (48, 48),
        "face_count": 128,
        "start_pos": 245760,
        "ls11_encoded": True,
        "palette": ['#000000', '#00A261', '#D34100', '#F3A261', '#0041D3', '#00A2F3', '#D361A2', '#F3E3D3']
    },
    "LEMPE": {
        "name": "拿破崙",
        "face_file": "KAODATA.DAT",  # 中英文版相同
        "face_size": (64, 80),
        "double_height": True,
        "persons": {
            "start_pos": [8934, 13274],
            "data_size": [17, 15],
            "data_count": 255
        },
        "nations": ["France", "Holland", "Bavaria", "Denmark", "Turkey", "Italy", "Venice", "Naples", "Portugal", "Sweden", "Spain", "Prussia", "Russia", "Austria", "England", "Dublin"],
        "places": {
            "start_pos": 7404,
            "data_size": 34,
            "data_count": 45 # 1-46?
            },
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55', '#5555FF', '#55FFFF', '#FF55FF', '#FFFFFF']
    },
    "ROYAL": {
        "name": "魔法皇冠",
        "face_file": "KAODATA.DAT",
        "face_size": (64, 80),
        "double_height": True,
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55', '#5555FF', '#55FFFF', '#FF55FF', '#FFFFFF']
    },
    "ROYALPC98": {
        "name": "魔法皇冠",
        "face_file": "KAODATA.DAT",
        "face_size": (64, 80),
        "start_pos": 368640+46080,
        "face_count": 91,
        "palette": ['#000000', '#00BA65', '#FF5555', '#EFCF55', '#0065BA', '#459ADF', '#FF55FF', '#FFFFFF']
    },
    "SAN1": {
        "name": "三國志",
        "face_file": "SAN_B/PICDATA.DAT",
        "face_size": (48, 80),
        "face_count": 114,
        "double_height": True,
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55']
    },
    "SAN2": {
        "name": "三國志II",
        "face_file": "KAODATA.DAT",
        "face_size": (64, 80),
        "double_height": True,
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55', '#5555FF', '#55FFFF', '#FF55FF', '#FFFFFF']
    },
    "SAN3": {
        "name": "三國志III",
        "face_file": "KAODATA.DAT",
        "face_size": (64, 80),
        "palette": ['#000000', '#10B251', '#F35100', '#F3E300', '#0041F3', '#00C3F3', '#F351D3', '#F3F3F3']
    },
    "SAN4": {
        "name": "三國志IV",
        # KAODATA.S4 作用尚不明, File Size: 530,413 byte (340 人需要 652,800)
        "face_file": "KAODATAP.S4",
        "face_size": (64, 80),
        "palette": ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251', '#D3D3B2']
    },
    "SAN4P": {
        "name": "三國志IV 威力加強版",
        "face_file": "KAODATA2.S4",
        "face_size": (64, 80),
        "palette": ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251', '#D3D3B2']
        # color pallete (威力加強版編輯器)
        #   | 黑[0] | 深藍[4] | 朱紅[2] | 深皮[6] |
        #   | 綠[1] | 淺藍[5] | 淺皮[3] | 雪白[7] |
    },
    "SAN5": {
        "name": "三國志V",
        "face_file": "KAODATA.S5",  # KAODATA.S5, KAODATAP.S5: 1,503,360 = 783 * 1920, 兩檔案相同
        "face_size": (64, 80),
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    },
    "SAN5P": {
        "name": "三國志V 威力加強版",
        "face_file": "KAOEX.S5",
        "face_size": (64, 80),
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    },
    "SAN1PC98": {
        "name": "三國志",
        "face_file": "PC98_SAN_B.FDI",
        "face_size": (48, 80),
        "face_count": 113,  # 後面有 (48, 80)x158個 montage 資料(應為動畫)
        "start_pos": 15120+240,
        "double_height": True,
        "palette": ['#000000', '#00FF00', '#FF0000', '#FFFF00', '#0000FF', '#00FFFF', '#FF00FF', '#FFFFFF']
    },
    "SAN2PC98": {
        "name": "三國志II",
        "face_file": "PC98_SAN2_B.FDI",
        "face_size": (64, 80),
        "face_count": [95, 124],  # 後面有 (64,80)x52個 montage 資料
        "start_pos": [189440, 371842+894],  # 189120 (~121 後半正確) 365697
        "palette": ['#000000', '#00FF00', '#FF0000', '#FFFF00', '#0000FF', '#00FFFF', '#FF00FF', '#FFFFFF']
    },
    "SUIKODEN": {
        "name": "水滸傳",
        "face_file": "KAOIBM.DAT",
        "face_size": (64, 80),
        "double_height": True,
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55', '#5555FF', '#55FFFF', '#FF55FF', '#FFFFFF']
    },
    "SUI98": {
        "name": "水滸傳",
        "face_file": "KAOIBM.DAT",
        "face_size": (64, 80),
        "start_pos": 15360,
        "face_count": 260,
        "palette": ['#000000', '#00FF00', '#FF0000', '#FFFF00', '#0000FF', '#00FFFF', '#FF00FF', '#FFFFFF']
    },
    "TAIKOH": {
        "name": "太閣立志傳",
        "face_file": "KAO.PUT",
        "face_size": (64, 80),
        "palette": ['#000000', '#41C341', '#F35100', '#F3D300', '#2061A2', '#00C3F3', '#F361B2', '#F3F3F3']
    },
    "TK2": {
        "name": "提督之決斷II",
        "face_file": "KAO.TK2",
        "face_size": (48, 64),
        "palette": ['#000000', '#417100', '#D32000', '#E3A261', '#0030A2', '#7192B2', '#C36161', '#F3F3F3']
    },
    "WINNING": {
        "name": "光榮賽馬",
        "face_file": "",
        "face_size": (64, 80),
        "palette": ['#000000', '#20D320', '#F30000', '#F3D300', '#0061C3', '#00B2F3', '#F351F3', '#F3F3F3']
    },
    "AIR2": {
        "name": "航空霸業II",  # NOT READY
        # CITYFACE.GDT, MAKFACE.GDT, MAKER.GDT, MAN.GDT, STAFF1.GDT 均非 KAO
        "face_file": "MAN.GDT",
        "face_size": (64, 80),
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    },
    "ISHIN2": {
        "name": "維新之嵐2",  # NOT READY
        "face_file": "ISHIN2.I2",
        "face_size": (64, 80),
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    },
    "LIBERTY": {
        "name": "獨立戰爭",  # NOT READY
        "face_file": "FACE.IDX",
        "face_size": (64, 80),
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    },
    "NOBU1": {
        "name": "",
        "face_file": "",
        "face_size": (48, 80),
        # "face_count": 114,
        "double_height": True,
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55']
    },
    "NOBU2": {
        "name": "",
        "face_file": "",
        "face_size": (64, 80),
        # "face_count": 114, #177 之後是大眾臉
        "double_height": True,
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    },
    "NOBU4": {
        "name": "",
        "face_file": "",
        "face_size": (64, 80),
        # "face_count": 114, #177 之後是大眾臉
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    },
    "TEST": {
        "name": "測試用",
        "face_file": "KAODATA.DAT",
        "face_size": (64, 80),
        # "start_pos": 2,
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    },
    "TEST2": {
        "name": "測試用",
        "face_file": "KAODATA.DAT",
        "face_size": (48, 80),
        "double_height": True,
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    },
    "TEST3": {
        "name": "測試用",
        "face_file": "KAODATA.DAT",
        "face_size": (64, 80),
        "ls11_encoded": True,
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    }
}
