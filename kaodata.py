import os.path

from PIL import Image

# 307張
SAN3_KAODATA = "/Users/tzengyuxio/DOSBox/SAN3/KAODATA.DAT"
SAN3_PALETTE = ['#000000', '#10B251', '#F35100', '#F3E300', '#0041F3', '#00C3F3', '#F351D3',
                '#F3F3F3']  # 黑 綠 朱 黃 藍 青 洋紅 白

# 530,413 byte (340 人需要 652,800)
SAN4_KAODATA = "/Users/tzengyuxio/DOSBox/SAN4/KAODATA.S4"
SAN4_PALETTE = ['#302000', '#204182', '#B24120', '#C38251', '#417120', '#418292', '#D3B282',
                '#D3D3B2']  # 黑 綠 朱 黃 藍 青 洋紅 白

# KAODATA2.S4: 320張, 水滸傳
SAN4_KAODATA2 = "/Users/tzengyuxio/DOSBox/SAN4/KAODATA2.S4"
SAN4_PALETTE2 = ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251',
                 '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白

# KAODATAP.S4: 701張, 1,346,621 byte
SAN4_KAODATAP = "/Users/tzengyuxio/DOSBox/SAN4/KAODATAP.S4"
SAN4_PALETTEP = ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251',
                 '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白

# KAODATA.S5, KAODATAP.S5: 1,503,360 = 783 * 1920, 兩檔案相同
SAN5_KAODATA = "/Users/tzengyuxio/DOSBox/SAN5/KAODATA.S5"
SAN5_PALETTE = ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251',
                '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白

# KAOEX.S5: 733,440 = 382 * 1920
SAN5_KAODATAEX = "/Users/tzengyuxio/DOSBox/SAN5/KAOEX.S5"
SAN5_PALETTEEX = ['#302000', '#417120', '#B24120', '#D3B282', '#204182', '#418292', '#C38251',
                  '#D3D3B2']  # 黑 綠 紅 粉 藍 青 橙 白


def convert_to_array(data_bytes):
    array = []
    it = iter(data_bytes)
    for b1 in it:
        b2, b3 = next(it), next(it)
        for i in range(7, -1, -1):
            n = ((b1 >> i) & 1) * 4 + ((b2 >> i) & 1) * 2 + ((b3 >> i) & 1)
            array.append(n)
    return array


def export_kaodata(tag, filename, palette, skip=0):
    color_table = []
    for c in palette:
        rr, gg, bb = c[1:3], c[3:5], c[5:7]
        color_table.append((int(rr, base=16), int(gg, base=16), int(bb, base=16)))

    if not os.path.exists(tag):
        os.makedirs(tag)

    with open(filename, 'rb') as f:
        i = 0
        while data_bytes := f.read(1920):
            i += 1
            img = Image.new('RGB', (64, 80))
            color_codes = convert_to_array(data_bytes)
            for idx, color_code in enumerate(color_codes):
                x, y = idx % 64, idx // 64
                img.putpixel((x, y), color_table[color_code])
            img_filename = '{}/{}_{:04d}.png'.format(tag, tag, i)
            img.save(img_filename)
            print('...save {}'.format(img_filename))
    print('{} images of face saved in [{}]'.format(i, tag))


# 三國志3
# export_kaodata('SAN3', SAN3_KAODATA, SAN3_PALETTE)

# 三國志4
# export_kaodata('SAN4', SAN4_KAODATA, SAN4_PALETTE)
# export_kaodata('SAN4_2', SAN4_KAODATA2, SAN4_PALETTE2)
# export_kaodata('SAN4_P', SAN4_KAODATAP, SAN4_PALETTEP)

# 三國志5
export_kaodata('SAN5', SAN5_KAODATA, SAN5_PALETTE)
export_kaodata('SAN5_EX', SAN5_KAODATAEX, SAN5_PALETTEEX)
