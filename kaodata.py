from PIL import  Image, ImageDraw

KAODATA = "/Users/tzengyuxio/DOSBox/SAN3/KAODATA.DAT"

def convert_to_array(bytes):
    array = []
    it = iter(bytes)
    for x in it:
        y, z = next(it), next(it)
        for i in range(8):
            offset = 7-i
            mask = 1 << offset
            n = ((x & mask) >> offset) * 4 + ((y & mask) >> offset) * 2+ ((z & mask) >> offset)
            array.append(n)
    return array


with open(KAODATA, 'rb') as f:
    bytes = f.read(1920)
    color_array = convert_to_array(bytes)

    for idx, dot in enumerate(color_array):
        if idx % 64 == 0:
            print()
        print(dot, end='')


    # img = Image.new('RGB', (64, 80), color='red')
    # img.save('pil_red.png')
    pass
