GAME_INFOS = {
    "EUROPE": {
        "name": "歐陸戰線",
        "face_file": "FACE.DAT",
        "face_size": (64, 80),
        "palette": ['#000000', '#419241', '#B24120', '#F3C361', '#104192', '#6FAEAE', '#D371B2', '#F3F3F3']
    },
    "TK2": {
        "name": "提督之決斷II",
        "face_file": "KAO.TK2",
        "face_size": (48, 64),
        "palette": ['#000000', '#417100', '#D32000', '#E3A261', '#0030A2', '#7192B2', '#C36161', '#F3F3F3']
    },
    "KOHRYUKI": {
        "name": "項劉記",
        "face_file": "KAO.KR1",
        "face_size": (64, 80),
        "palette": ['#000000', '#418200', '#C34100', '#E3A251', '#0030A2', '#71A2B2', '#B27171', '#F3E3D3']
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
    "SAN1S": {
        "name": "三國志 STEAM",
        "face_file": "SAN1.EXE",
        "face_size": (48, 80),
        "face_count": 360,
        "start_pos": 1056963, # 1056960, # 241920,
        "double_height": True,
        # "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55']
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55', '#5555FF', '#55FFFF', '#FF55FF', '#FFFFFF']
    },
    "SAN1PC98": {
        "name": "三國志",
        "face_file": "PC98_SAN_B.FDI",
        "face_size": (48, 80),
        "face_count": 113, # 後面有 (48, 80)x158個 montage 資料(應為動畫)
        "start_pos": 15120+240,
        "double_height": True,
        "palette": ['#000000', '#00FF00', '#FF0000', '#FFFF00', '#0000FF', '#00FFFF', '#FF00FF', '#FFFFFF']
    },
    "SAN2PC98": {
        "name": "三國志II",
        "face_file": "PC98_SAN2_B.FDI",
        "face_size": (64, 80),
        "face_count": [95, 124], # 後面有 (64,80)x52個 montage 資料
        "start_pos": [189440, 371842+894], # 189120 (~121 後半正確) 365697
        "palette": ['#000000', '#00FF00', '#FF0000', '#FFFF00', '#0000FF', '#00FFFF', '#FF00FF', '#FFFFFF']
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
        "face_file": "KAO2.DEC",  # "KAO.LZW", 465890 bytes (KAO: first 210279 bytes, THEN: 864B x 128)
        "face_size": (64, 80),
        "face_count": 128,
        "palette": ['#000000', '#00A261', '#D34100', '#F3A261', '#0041D3', '#00A2F3', '#D361A2', '#F3E3D3']
    },
    "KOUKAI2M": {
        "name": "大航海時代II",
        "face_file": "KAO.LZW",  # "KAO.LZW", 465890 bytes (LS11: first 292514 bytes, MONTAGE: 173376)
        "face_size": (64, 80),
        "start_pos": 292514,
        "palette": ['#000000', '#00A261', '#D34100', '#F3A261', '#0041D3', '#00A2F3', '#D361A2', '#F3E3D3']
    },
    "KOUKAI2I": {
        "name": "大航海時代II 道具",
        "face_file": "KAO2.DEC",
        "face_size": (48, 48),
        "face_count": 128,
        "start_pos": 245760,
        "palette": ['#000000', '#00A261', '#D34100', '#F3A261', '#0041D3', '#00A2F3', '#D361A2', '#F3E3D3']
    },
    "SUIKODEN": {
        "name": "水滸傳",
        "face_file": "KAOIBM.DAT",
        "face_size": (64, 80),
        "double_height": True,
        "palette": ['#000000', '#55FF55', '#FF5555', '#FFFF55', '#5555FF', '#55FFFF', '#FF55FF', '#FFFFFF']
    },
    "AIR2": {
        "name": "航空霸業II",  # NOT READY
        # CITYFACE.GDT, MAKFACE.GDT, MAKER.GDT, MAN.GDT, STAFF1.GDT 均非 KAO
        "face_file": "MAN.GDT",
        "face_size": (64, 80),
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    },
    "LIBERTY": {
        "name": "獨立戰爭",  # NOT READY
        "face_file": "FACE.IDX",
        "face_size": (64, 80),
        "palette": ['#202010', '#206510', '#BA3000', '#EFAA8A', '#104575', '#658A9A', '#BA7545', '#EFDFCF']
    }
}
