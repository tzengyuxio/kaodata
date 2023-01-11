from PIL import  Image, ImageDraw

KAODATA = "/Users/tzengyuxio/DOSBox/SAN3/KAODATA.DAT"

def convert_to_array(bytes):
    array = []
    it = iter(bytes)
    for x in it:
        y, z = next(it), next(it)
        for i in range(7, -1, -1):
            n = (x >> i) & 1 * 4 + (y >> i) & 1 * 2+ (z >> i) & 1
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
