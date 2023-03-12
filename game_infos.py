GAME_INFOS = {
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
    "TAIKOH": {
        "name": "太閣立志傳",
        "face_file": "KAO.PUT",
        "face_size": (64, 80),
        "palette": ['#000000', '#41C341', '#F35100', '#F3D300', '#2061A2', '#00C3F3', '#F361B2', '#F3F3F3']
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
    "NOBU1": {
        "name": "",
        "face_file": "",
        "face_size": (48, 80),
        # "face_count": 114,
        "double_height": True,
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55']
    },
    "NOBU3": {
        "name": "信長之野望II 戰國群雄傳",
        "face_file": "KAODATA.DAT", # KAO_OE 僅有前 28 人
        "face_size": (64, 80),
        "face_count": 177, # 177 之後是大眾臉
        "double_height": True,
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55', '#5555FF', '#55FFFF', '#FF55FF', '#FFFFFF']
    },
    "NOBU4": {
        "name": "武將風雲錄",
        "face_file": "KAODATA.DAT",
        "face_size": (64, 80),
        "palette": ['#000000', '#00AA00', '#AA0000', '#FFFF00', '#0000AA', '#00AAAA', '#AA00AA', '#FFFFFF']
    },
    "TEST": {
        "name": "測試用",
        "face_file": "KAODATA.DAT",
        # "face_size": (208, 80),
        "face_size": (64, 80),
        # "start_pos": 1920,
        # "face_size": (128, 160),
        # "face_size": (72, 32),
        # "face_size": (80, 160),
        # "start_pos": 2,
        # "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF', '#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
        "double_height": True,
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
