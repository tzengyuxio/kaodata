import sys
from PIL import Image
import numpy


def load_pallete(filename):
    palettes = []
    with open(filename, 'rb') as f:
        for _ in range(3):
            _ = f.read(4)
            data = f.read(1024)
            bytes_list = [data[i:i+4] for i in range(0, 1024, 4)]
            palette = [tuple([x[i] for i in range(4)]) for x in bytes_list]
            palettes.append(palette)
    # print('p0 vs p1: {}'.format(palettes[0] == palettes[1]))
    # print('p0 vs p2: {}'.format(palettes[0] == palettes[2]))
    # print(len(palettes))
    # print(len(palettes[0]))
    return palettes[0]


def export_face(filename, idx):
    img_data = None
    with open(filename, 'rb') as f:
        count = int.from_bytes(f.read(4), 'little')
        print('count: {}'.format(count))
        offset = 4 + 16 * count
        f.seek(4 + idx * 16)
        endian = 'little'
        pos = int.from_bytes(f.read(4), endian)
        size = int.from_bytes(f.read(4), endian)
        w = int.from_bytes(f.read(4), endian)
        h = int.from_bytes(f.read(4), endian)
        print('pos: {}; size: {}; dimension: ({}, {})'.format(pos, size, w, h))
        f.seek(offset + pos)
        img_data = f.read(size)

    pallete = load_pallete("/Users/yuxioz/PALETTE.S6")
    # for c in pallete:
    #     print(c)

    print('img_data len: {}, type: {}'.format(len(img_data), type(img_data)))
    image = Image.new('RGB', (w, h), color='magenta')
    for i in range(size):
        x, y = i % w, i // w
        color_index = img_data[i] #int.from_bytes(img_data[i], 'little')
        image.putpixel((x, y), pallete[color_index])
    out_filename = 'KAO_{:04d}.png'.format(idx+1)
    image.save(out_filename)


def main():
    args = sys.argv[1:]
    export_face("/Users/yuxioz/Desktop/KOEI 頭像色盤參考/KAO/KAODATA.S6", int(args[0], 10))


if __name__ == '__main__':
    main()
