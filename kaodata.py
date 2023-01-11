from PIL import Image

KAODATA = "/Users/tzengyuxio/DOSBox/SAN3/KAODATA.DAT"
PALETTE = ['#000000', '#10B251', '#F35100', '#F3E300', '#0041F3', '#00C3F3', '#F351D3', '#F3F3F3']  # 黑 綠 朱 黃 藍 青 洋紅 白


def convert_to_array(data_bytes):
    array = []
    it = iter(data_bytes)
    for b1 in it:
        b2, b3 = next(it), next(it)
        for i in range(7, -1, -1):
            n = ((b1 >> i) & 1) * 4 + ((b2 >> i) & 1) * 2 + ((b3 >> i) & 1)
            array.append(n)
    return array


colors = []
for c in PALETTE:
    rr, gg, bb = c[1:3], c[3:5], c[5:7]
    colors.append((int(rr, base=16), int(gg, base=16), int(bb, base=16)))

prefix = 'SAN3'

with open(KAODATA, 'rb') as f:
    i = 0
    while data_bytes := f.read(1920):
        i += 1
        img = Image.new('RGB', (64, 80))
        color_array = convert_to_array(data_bytes)
        for idx, dot in enumerate(color_array):
            x, y = idx % 64, idx // 64
            img.putpixel((x, y), colors[dot])
        filename = '{}/{}_{:04d}.png'.format(prefix, prefix, i)
        img.save(filename)
