import os
from PIL import Image
#
SAN2_MSG16P = "/Users/tzengyuxio/DOSBox/SAN2/MSG.16P"
SAN2_NAME16P = "/Users/tzengyuxio/DOSBox/SAN2/NAME.16P"

# 307張
SAN3_HAN16P = "/Users/tzengyuxio/DOSBox/SAN3/HAN.16P"  # 1335 字
SAN3_NAME16P = "/Users/tzengyuxio/DOSBox/SAN3/NAME.16P"


def export_font(tag, filename, font_h=14, pre=True):
    font_size = font_h * 2
    block_w = 20
    block_h = 28
    with open(filename, 'rb') as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()
        # num_font = (file_size-4) // font_size if head else file_size // font_size
        num_font = file_size // font_size
        img_w = block_w * 40
        img_h = block_h * ((num_font // 40) + 1)
        # print('head        : {}'.format(head))
        print('file size   : {}'.format(file_size))
        print('num of fonts: {}'.format(num_font))
        print('image size  : {}x{} ({}x{})'.format(img_w, img_h, 40, ((num_font // 40) + 1)))

        i = 0
        img = Image.new('RGB', (img_w, img_h), color='white')
        f.seek(0)
        if pre:
            c = f.read(2)  # 這個是 big5
            print('{}: ({}, {})'.format(c.hex(), i // 40, i % 40))
        while data_bytes := f.read(font_size):
            for idx, byte in enumerate(data_bytes):
                for k in range(7, -1, -1):
                    x = 7 - k + 8 * (idx % 2)
                    y = idx // 2
                    bit = (byte >> k) & 1
                    abs_x = (i % 40) * block_w + x
                    abs_y = (i // 40) * block_h + y
                    if bit:
                        img.putpixel((abs_x, abs_y), (0, 0, 0))
                    else:
                        img.putpixel((abs_x, abs_y), (255, 255, 255))
            i += 1
            if pre:
                c = f.read(2)
                print('{}: ({}, {})'.format(c.hex(), i // 40, i % 40))
    img_filename = '{}_{}.png'.format(tag, os.path.basename(filename).replace('.', ''))
    img.save(img_filename)
    print('...save {}'.format(img_filename))
    print()

# 三國志2
# export_font('SAN2', SAN2_MSG16P, pre=True)
# export_font('SAN2', SAN2_NAME16P)

# 三國志3
# export_font('SAN3', SAN3_HAN16P, font_h=14)
# export_font('SAN3', SAN3_NAME16P, font_h=14)


def count_big5(s):
    up = s[:2]
    dw = s[2:]
    a = int('0x'+up, 16) - int('0xa4', 16)
    bb = int('0x'+dw, 16)
    if bb > int('0xa1', 16):
        bb = bb - int('0xa1', 16) + 63
    else:
        bb = bb - int('0x40', 16)
    return  (a * 157 + bb) + 1

def count_koei(s):
    up = s[:2]
    dw = s[2:]
    a = int('0x'+up, 16) - int('0x92', 16)
    bb = int('0x'+dw, 16)
    if bb > int('0x80', 16):
        bb = bb - int('0x80', 16) + 63
    else:
        bb = bb - int('0x40', 16)
    return  (a * 188 + bb) + 1 - 95




# export_font('LEMPE', 'FONT/LEMPE_MSG.16P', pre=True)

print(count_big5('a454')) # 三 21
print(count_big5('a540')) # 世 158
print(count_big5('a57c')) # 四 218
print(count_big5('aca5')) # 洛 1324
print(count_big5('aeb3')) #    1652 (+3)
print(count_big5('af7d')) #    1789 (+18)
print(count_big5('b15b')) #    2069
print()
print(count_koei('92b4')) # 三 21
print(count_koei('9381')) # 世 158
print(count_koei('93bd')) # 四 218
print(count_koei('99a7')) # 洛 1324
print(count_koei('9b71')) # 拿 1647
print(count_koei('9c31')) # 破 1771
print(count_koei('9da0')) # 崙 2069
