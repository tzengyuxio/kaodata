#!/usr/bin/env python3
import zlib
import click
from PIL import Image
import os
import os.path
import math
from bitstream import BitStream
import io
from utils import grouper


@click.group()
def dekoei():
    """dekoei command"""
    pass


@click.group()
def san9():
    """三國志IX

    \b
    File List:
        G_FaceL.s9
        G_FaceS.s9
        G_FaceT.s9
        G_FacLPK.s9
        G_FacSPK.s9
        G_FacTPK.s9
        P_Face.s9
    """
    pass


@click.group()
def san10():
    """三國志X

    \b
    File List:
        Grp\GpkFace1.s10
        Grp\GpkFace2.s10
        Grp\GpkFaceL.s10
        Grp\GpkFaceS.s10
        Grp\GpkFaceT.s10
        Grp\GrpFaceL.s10 832
        Grp\GrpFaceS.s10 1451, 分左右面向
        Grp\GrpFaceT.s10 832
        P_Face.s9
    """
    pass


@click.group()
def san11():
    """三國志11

    \b
    File List:
        San11Face00.fce

    Example:

        dekoei.py san11 face -f San11Face00.fce --prefix "SAN11_WIN_F"
    """
    pass


@click.group()
def san12():
    """三國志12

    \b
    File List:
        <placeholder>

    Example:

        dekoei.py san12 face -f KAO/SAN12_KAO_W_L.S12  --index KAO/SAN12_KAODATA.S12 --tag SAN12LARGE --prefix "SAN12_WIN_FL"
        ./dekoei.py san12 face -f KAO/SAN12_ADD00_KAO_W_L.S12  --index KAO/SAN12_ADD00.dat --tag SAN12LARGE --prefix "SAN12_WIN_FL"
        ./dekoei.py san12 face -f KAO/SAN12_ADD20_KAO_W_L.S12  --index KAO/SAN12_ADD20.dat --tag SAN12LARGE --prefix "SAN12_WIN_FL"
        ./dekoei.py san12 face -f KAO/SAN12_ADD21_KAO_W_L.S12  --index KAO/SAN12_ADD21.dat --tag SAN12LARGE --prefix "SAN12_WIN_FL"
        ./dekoei.py san12 face -f KAO/SAN12_SP0_KAO_W_L.S12  --index KAO/SAN12_SP0.dat --tag SAN12LARGE --prefix "SAN12_WIN_FL"

        ./dekoei.py san12 face -f KAO/SAN12_KAO_F_M.S12  --index KAO/SAN12_KAODATA.S12 --tag SAN12SMALL --prefix "SAN12_WIN_FM"
        ./dekoei.py san12 face -f KAO/SAN12_ADD00_KAO_F_M.S12  --index KAO/SAN12_ADD00.dat --tag SAN12SMALLA00 --prefix "SAN12_WIN_FM"
        ./dekoei.py san12 face -f KAO/SAN12_ADD20_KAO_F_M.S12  --index KAO/SAN12_ADD20.dat --tag SAN12SMALLA20 --prefix "SAN12_WIN_FM"
        ./dekoei.py san12 face -f KAO/SAN12_ADD21_KAO_F_M.S12  --index KAO/SAN12_ADD21.dat --tag SAN12SMALLA21 --prefix "SAN12_WIN_FM"
        ./dekoei.py san12 face -f KAO/SAN12_SP0_KAO_F_M.S12  --index KAO/SAN12_SP0.dat --tag SAN12SMALLSP --prefix "SAN12_WIN_FM"
    """
    pass


@click.group()
def san13():
    """三國志13

    \b
    File List:
        <placeholder>

    Example:
    """
    pass


@click.group()
def san14():
    """三國志14

    \b
    File List:
        <placeholder>

    Example:
    """
    pass


def get_codes(data):
    codes = []
    stream = BitStream(data, bytes)
    c1, c2 = 0, 0
    cursor = 0
    pos_end = len(data)*8
    l = 0
    while True:
        bit = stream.read(bool)
        cursor += 1
        c1 = (c1 << 1) | bit
        l += 1
        if not bit:
            for i in range(l):
                c2 = (c2 << 1) | stream.read(bool)
                cursor += 1
            codes.append(c1+c2)
            c1, c2 = 0, 0
            l = 0
        if cursor >= pos_end:
            break
    return codes


def ls11_decode_data(data, dictionary, orig_size):
    original_bytes = bytearray(orig_size)
    pos = 0

    codes = get_codes(data)
    # print('[{}] {}'.format(i, codes))
    # print('{:03d}: [{}]: ({}, {}, {}) ({}, {})'.format(i, pos, *encode_infos[i], len(data), size_of_codes(codes)))
    offset = 0
    count_in_block = 0
    for code in codes:
        # if pos >= original_size:
        #     break
        if count_in_block >= orig_size:
            continue
        if offset > 0:
            length = 3 + code
            for _ in range(length):
                original_bytes[pos] = original_bytes[pos-offset]
                pos += 1
                count_in_block += 1
                if count_in_block >= orig_size:
                    break
            offset = 0
        elif code < 256:
            original_bytes[pos] = dictionary[code]
            pos += 1
            count_in_block += 1
        else:
            offset = code - 256
    return bytes(original_bytes)


def load_palette(filename, start_pos):
    with open(filename, 'rb') as f:
        _ = f.read(start_pos)
        data = f.read(1024)
        color_bytes = [data[i:i+4] for i in range(0, 1024, 4)]
        colors = [tuple([x[i] for i in range(4)]) for x in color_bytes]
        return colors


def load_palette_data(data: bytes, reverse: bool):
    color_bytes = [data[i:i+4] for i in range(0, 1024, 4)]
    if reverse:
        return [tuple(x[2::-1]+x[3:]) for x in color_bytes]  # [b, g, r, a] -> [r, g, b, a]
    return [tuple(x) for x in color_bytes]


def san9_load_face(filename, palette, face_w=64, face_h=80, count=9999, start_pos=0):
    data_size = face_w * face_h
    file_size = os.stat(filename).st_size
    count = min(count, file_size // data_size)

    face_images = []
    with open(filename, 'rb') as f:
        f.seek(start_pos)
        for _ in range(count):
            f.read(16)
            face_data = f.read(data_size)
            image = Image.new('RGB', (face_w, face_h), color=(55, 55, 55))
            for px_idx in range(data_size):
                x, y = px_idx % face_w, px_idx // face_w
                color_index = face_data[px_idx]
                image.putpixel((x, y), palette[color_index])
            face_images.append(image)
    return face_images


def san10_load_face(filename, count):
    face_images = []
    with open(filename, 'rb') as f:
        f.seek(12)
        group_count = int.from_bytes(f.read(2), 'little')
        print(group_count)
        f.read(6)
        dictionary = f.read(256)
        group_infos = []
        for _ in range(group_count):
            face_w = int.from_bytes(f.read(4), 'little')  # (S) 40000000; (T) 20000000
            face_h = int.from_bytes(f.read(4), 'little')  # (S) 50000000; (T) 28000000
            orig_size = int.from_bytes(f.read(4), 'little')  # 00090000
            pack_size = int.from_bytes(f.read(4), 'little')  # 00090000
            start_pos = int.from_bytes(f.read(4), 'little')  #
            f.read(4)  # 01030000 (?)
            group_infos.append((face_w, face_h, orig_size, pack_size, start_pos))

        count = min(group_count, count)
        for i in range(count):
            face_w, face_h, orig_size, pack_size, start_pos = group_infos[i]
            data_size = face_w * face_h
            f.seek(start_pos)
            pack_data = f.read(pack_size)
            face_data, palette_data = bytes(), bytes()
            if pack_size != orig_size:
                pack_data = ls11_decode_data(pack_data, dictionary, orig_size)
                print('[{}] RLE Decode: ({}, {}, {})'.format(i, orig_size, pack_size, len(pack_data)))
            face_data = pack_data[:data_size]
            palette_data = pack_data[data_size:]
            palette = load_palette_data(palette_data, True)
            image = Image.new('RGB', (face_w, face_h), color=(55, 55, 55))
            for px_idx in range(data_size):
                x, y = px_idx % face_w, px_idx // face_w
                color_index = face_data[px_idx]
                image.putpixel((x, y), palette[color_index])
            face_images.append(image)
    return face_images


def san11_load_face(data, face_w, face_h, bpp):
    image = Image.new('RGB', (face_w, face_h), color=(55, 55, 55))
    data_size = face_w * face_h
    if bpp == 8:
        face_data = data[:data_size]
        palette_data = data[data_size:]
        palette = load_palette_data(palette_data, False)
        for px_idx in range(data_size):
            x, y = px_idx % face_w, px_idx // face_w
            color_index = face_data[px_idx]
            image.putpixel((x, y), palette[color_index])
        return image
    if bpp == 24:
        for px_idx in range(data_size):
            x, y = px_idx % face_w, px_idx // face_w
            color = [data[px_idx*3+i] for i in range(3)]
            color.reverse()
            image.putpixel((x, y), tuple(color))
        return image
    else:  # bpp == 32
        for px_idx in range(data_size):
            x, y = px_idx % face_w, px_idx // face_w
            color = [data[px_idx*4+i] for i in range(4)]
            color = color[2::-1] + color[3:]
            image.putpixel((x, y), tuple(color))
        return image


def save_faces(face_images, face_w, face_h, prefix, out_dir, crop_size=None):
    is_save_index = False if face_w > 128 else True
    count = len(face_images)
    if type(face_images) == list:
        face_images = dict(zip(range(1, count+1), face_images))

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # save single
    print('saving single files, count={}'.format(count))
    for idx, img in face_images.items():
        out_filename = '{}/{}{:04d}.png'.format(out_dir, prefix, idx + 1)
        if crop_size is not None:
            img = img.crop(crop_size)
        img.save(out_filename)
        print("... save {}".format(out_filename))

    # save index
    if is_save_index:
        print('saving index file')
        img_w = face_w * 16
        img_h = face_h * math.ceil(count / 16)
        index_image = Image.new('RGB', (img_w, img_h), color=(55, 55, 55))
        out_filename = '{}/{}00-INDEX.png'.format(out_dir, prefix)
        for idx, img in enumerate(face_images.values()):
            pos_x = (idx % 16) * face_w
            pos_y = (idx // 16) * face_h
            if crop_size is not None:
                index_image.paste(img.crop(crop_size), (pos_x, pos_y))
            else:
                index_image.paste(img, (pos_x, pos_y))
        index_image.save(out_filename)


def san12_decode_group(f, start_pos: int, data_size: int, crop_w, crop_h, face_w, face_h, indexes=None):
    print(start_pos, data_size)
    f.seek(start_pos)
    group_header = f.read(4)  # "LINK"
    group_count = int.from_bytes(f.read(4), 'little')
    group_u1 = f.read(8)  # (face:2000) 20000000 d0070000, (item:179) 20000000 b3000000
    group_u2 = f.read(16)  # A03E0000 00000000 00000000 00000000
    block_infos = []
    for _ in range(group_count):
        block_start_pos = int.from_bytes(f.read(4), 'little')
        block_data_size = int.from_bytes(f.read(4), 'little')
        block_infos.append((block_start_pos, block_data_size))
    face_images = {}
    crop_size = crop_w * crop_h * 4
    for idx, block_info in enumerate(block_infos):
        block_start_pos, block_data_size = block_info
        f.seek(start_pos + block_start_pos)
        header = f.read(8)  # header, "GT1G0500" or "G1TG0050"
        endian = 'little' if header == b"GT1G0500" else 'big'
        block_size = int.from_bytes(f.read(4), endian)  # data size
        if block_size < 32 * 32:
            print('... [{}] skipped, no data'.format(idx))
            continue
        print('... [{}][{}] read, block_start_pos: {}, block_size: {}'.format(
            idx, header, block_start_pos, block_size))
        f.read(32)  # unknown
        px_data = f.read(crop_size)
        image = san11_load_face(px_data, crop_w, crop_h, 32)
        if indexes is None:
            face_images[idx] = image
        else:
            face_images[indexes[idx]] = image
    return face_images


def decode_raw(data, alpha=True, crop=None, out_dir='.', prefix='TEST_F'):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        os.makedirs(out_dir + '/gt1g')
        os.makedirs(out_dir + '/dds')
        os.makedirs(out_dir + '/alpha')
        os.makedirs(out_dir + '/rgb')

    f = io.BytesIO(data)
    cnt = int.from_bytes(f.read(4), 'little')
    block_infos = []
    for _ in range(cnt):
        start_pos = int.from_bytes(f.read(4), 'little')
        data_size = int.from_bytes(f.read(4), 'little')
        block_infos.append((start_pos, data_size))
    # cnt = 1  # breaker
    for i in range(cnt):
        start_pos, data_size = block_infos[i]
        f.seek(start_pos)
        block_data = f.read(data_size)
        # print(block_data[:3])
        if block_data[:3] == b'zp1':  # zp1
            # print('decode zp1')
            decode_zp1(block_data, alpha, crop, i, out_dir, prefix)
        else:
            print('unknown how to decode')


def decode_zp1(data, alpha=True, crop_size=None, idx=0, out_dir='.', prefix='TEST_F'):
    f = io.BytesIO(data)
    f.read(4)  # header 'zp1 '
    sz = int.from_bytes(f.read(4), 'little')
    f.read(4)  # unknown
    cnt = int.from_bytes(f.read(4), 'little')
    block_sizes = []
    for _ in range(cnt):
        block_sizes.append(int.from_bytes(f.read(4), 'little'))
    gt1g_file = bytearray()
    f.seek(2048)
    for i in range(cnt):
        bsz_intable = block_sizes[i]
        start_pos = f.tell()
        bsz_inblock = int.from_bytes(f.read(4), 'little')
        read_size = math.ceil(bsz_intable/128) * 128 - 4
        print('[{}] zlib block: start_pos: {}, size: {}'.format(i, start_pos, read_size))
        zipped = f.read(read_size)
        new_file = zlib.decompress(zipped)
        print('[{}-{}] new_file size: {} ({})'.format(idx, i, len(new_file), hex(len(new_file))))
        gt1g_file.extend(new_file)

        # ## to images
        # images = decode_gt1g(new_file)
        # if images is None:
        #     continue
        # elif len(images) == 1:
        #     out_filename = '{}/{}{:04d}.png'.format(out_dir, prefix, idx)
        #     img = images[0].crop(crop_size) if alpha else images[0].crop(crop_size).convert('RGB')
        #     img.save(out_filename)
        # else:
        #     for frame_idx, img in enumerate(images):
        #         out_filename = '{}/{}{:04d}_{:02d}.png'.format(out_dir, prefix, idx, frame_idx)
        #         aimg = img.crop(crop_size) if alpha else img.crop(crop_size).convert('RGB')
        #         aimg.save(out_filename)
        # ## to decompressed files
        # out_filename = '{}/TEST{}-{:04d}.dat'.format(out_dir, idx, i)
        # with open(out_filename, 'xb') as fout:
        #     fout.write(new_file)
    # TODOS
    # - save gt1g file for check
    # - save DDS files for check
    gt1g_out_filename = '{}/gt1g/{}{:04d}.gt1g'.format(out_dir, prefix, idx)
    with open(gt1g_out_filename, 'xb') as fout:
        fout.write(gt1g_file)
    images = decode_gt1g(gt1g_file)
    if images is None:
        print('decode gt1g error')
        return
    elif len(images) == 1:
        out_filename = '{}/{}{:04d}.png'.format(out_dir, prefix, idx)
        img = images[0].crop(crop_size) if alpha else images[0].crop(crop_size).convert('RGB')
        img.save(out_filename)
    else:
        for frame_idx, img in enumerate(images):
            out_filename = '{}/dds/{}{:04d}_{:02d}.dds'.format(out_dir, prefix, idx, frame_idx)
            img.save(out_filename)
            if frame_idx == 2:
                out_filename_alpha = '{}/alpha/{}{:04d}.png'.format(out_dir, prefix, idx, frame_idx)
                out_filename_rgb = '{}/rgb/{}{:04d}.png'.format(out_dir, prefix, idx, frame_idx)
                aimg = img.crop(crop_size)
                aimg.save(out_filename_alpha)
                aimg = aimg.convert('RGB')
                aimg.save(out_filename_rgb)


def decode_gt1g(data, idx=0):
    """
    return dds image
    """
    f = io.BytesIO(data)
    g1t_size = len(data)

    # g1t_header (28 or 32 bytes)
    header = f.read(4)  # header, "GT1G"
    endian = 'little' if header == b"GT1G" else 'big'
    version = f.read(4)  # version, "0600"
    total_size = int.from_bytes(f.read(4), endian)  # data size
    if total_size < 32 * 32:
        print('... [{}] skipped, no data'.format(idx))
        return
    header_size = int.from_bytes(f.read(4), endian)  # header size
    nb_textures = int.from_bytes(f.read(4), endian)
    platform = int.from_bytes(f.read(4), endian)  # platform
    extra_size = int.from_bytes(f.read(4), endian)
    print('... [{}][{}] read, block_size: {}, {}, {}, {}, {}'.format(
        idx, header, total_size, header_size, nb_textures, platform, extra_size))

    # offset table (4 * nb_textures)
    f.seek(header_size)
    offset_tables = []
    for i in range(nb_textures):
        offset_tables.append(int.from_bytes(f.read(4), 'little'))
    # print('offset_table', offset_tables)

    print('TYPE OFFSET     SIZE       NAME           DIMENSIONS MIPMAPS PROPS')
    images = []
    for i in range(nb_textures):
        f.seek(header_size+offset_tables[i])
        mm = int.from_bytes(f.read(1), 'little')  # z_mipmaps, mipmaps
        tex_mipmaps = (mm >> 4) & 0x0F
        tex_z_mipmaps = mm & 0x0F
        tex_type = f.read(1)  # DDS_FORMAT_DXT5 0x08
        dx_dy = int.from_bytes(f.read(1), 'little')
        tex_dx = (dx_dy >> 4) & 0x0F
        tex_dy = dx_dy & 0x0F
        flags = f.read(5)
        data_size = int.from_bytes(f.read(4), 'little')  # should only 0 or 0x0c or 0x10 or 0x14, extra flag size
        if data_size >= 0x0c:
            flag_depth = f.read(4)
            flag1 = f.read(4)  # number of frames
        texture_size = 0
        if i + 1 == nb_textures:  # last one
            texture_size = g1t_size - header_size
            texture_size -= data_size
            texture_size -= len(offset_tables) * 4
        else:
            texture_size = offset_tables[i+1] - offset_tables[i]
        dims = '{}x{}'.format(1 << tex_dx, 1 << tex_dy)
        texture_size -= 8  # sizeof g1t_tex_header
        print('{} {} {} {} {}'.format(tex_type,
                                      header_size+extra_size+offset_tables[i],
                                      texture_size,
                                      dims,
                                      tex_mipmaps
                                      ))
        # TYPE OFFSET     SIZE       NAME                   DIMENSIONS MIPMAPS PROPS
        # 0x08 0x00000024 0x00004000 test_new_file0\000.dds 128x128    1       -
        # expected SIZE: 16384, actual 16384 g1t_size: 16440, header_size: 32
        print()
        fout = io.BytesIO(b'')
        fout.write(b'DDS ')
        # write dds header
        dds_header_size = 124
        dds_header_flags = 0x00001007 | 0x00080000  # DDS_HEADER_FLAGS_TEXTURE | DDS_HEADER_FLAGS_LINEARSIZE;
        dds_header_height = 1 << tex_dy
        dds_header_width = 1 << tex_dx
        dds_header_pitch_or_linear_size = ((dds_header_width + 3) // 4) * \
            ((dds_header_height + 3) // 4) * 16  # 16: bpb, bytes per pixel block
        dds_header_depth = 0
        dds_header_mipmap_count = tex_mipmaps  # 0 in this case
        dds_header_reserved = 0  # all 0
        dds_header_caps = 4096  # 0x00001000  // DDSCAPS_TEXTURE
        if dds_header_mipmap_count != 0:
            dds_header_flags |= 0x00020000  # // DDSD_MIPMAPCOUNT
            dds_header_caps |= 262152  # DDS_SURFACE_FLAGS_MIPMAP 0x00400008  // DDSCAPS_COMPLEX | DDSCAPS_MIPMAP
        dds_header_caps2 = 0
        dds_header_caps3 = 0  # 0
        dds_header_caps4 = 0  # 0
        dds_header_reserved2 = 0  # 0
        fout.write(dds_header_size.to_bytes(4, 'little'))
        fout.write(dds_header_flags.to_bytes(4, 'little'))
        fout.write(dds_header_height.to_bytes(4, 'little'))
        fout.write(dds_header_width.to_bytes(4, 'little'))
        fout.write(dds_header_pitch_or_linear_size.to_bytes(4, 'little'))
        fout.write(dds_header_depth.to_bytes(4, 'little'))
        fout.write(dds_header_mipmap_count.to_bytes(4, 'little'))
        for i in range(11):
            fout.write(dds_header_reserved.to_bytes(4, 'little'))
        # ddspf
        ddspf_size = 32
        ddspf_flags = 4  # DDS_FOURCC 0x00000004  // DDPF_FOURCC
        ddspf_four_cc = b'DXT5'  # "DXT5"
        ddspf_rgb_bit_count = 0
        ddspf_r_bit_mask = 0
        ddspf_g_bit_mask = 0
        ddspf_b_bit_mask = 0
        ddspf_a_bit_mask = 0
        fout.write(ddspf_size.to_bytes(4, 'little'))
        fout.write(ddspf_flags.to_bytes(4, 'little'))
        fout.write(ddspf_four_cc)
        fout.write(ddspf_rgb_bit_count.to_bytes(4, 'little'))
        fout.write(ddspf_r_bit_mask.to_bytes(4, 'little'))
        fout.write(ddspf_g_bit_mask.to_bytes(4, 'little'))
        fout.write(ddspf_b_bit_mask.to_bytes(4, 'little'))
        fout.write(ddspf_a_bit_mask.to_bytes(4, 'little'))

        fout.write(dds_header_caps.to_bytes(4, 'little'))
        fout.write(dds_header_caps2.to_bytes(4, 'little'))
        fout.write(dds_header_caps3.to_bytes(4, 'little'))
        fout.write(dds_header_caps4.to_bytes(4, 'little'))
        fout.write(dds_header_reserved2.to_bytes(4, 'little'))

        # data
        f.seek(len(data) - texture_size)
        fout.write(f.read(texture_size))

        images.append(Image.open(fout))
    return images


@click.command(help="顏CG解析")
@click.option('-p', '--palette', 'palette_file', help="色盤", required=True)
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('-t', '--tag', 'tag', default='SAN9', help='')
@click.option('--prefix', 'prefix', help='')
@click.option('--image-size',
              type=click.Choice(['L', 'S', 'T'], case_sensitive=False),
              help='頭像尺寸 L 240x240,\n S:  64x 80,\n T: 32x40')
def san9_face(palette_file, face_file, tag, image_size, prefix):
    """三國志 IX 頭像解析"""
    image_size_spec = {"L": (240, 240), "S": (64, 80), "T": (32, 40)}
    face_w, face_h = image_size_spec[image_size]
    palette = load_palette(palette_file, start_pos=44)
    face_images = san9_load_face(face_file, palette, face_h=face_h, face_w=face_w, start_pos=4)
    save_faces(face_images, face_w, face_h, prefix, out_dir=tag)


@click.command()
def san9_person():
    pass


@click.command(help="顏CG解析")
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('-t', '--tag', 'tag', default='SAN10', help='')
@click.option('--count', 'count', default=9999, help='')
@click.option('--prefix', 'prefix', help='')
@click.option('--image-size',
              type=click.Choice(['L', 'S', 'T'], case_sensitive=False),
              help='頭像尺寸 L 240x240,\n S:  64x 80,\n T: 32x40')
def san10_face(face_file, tag, image_size, prefix, count):
    """三國志 X 頭像解析"""
    image_size_spec = {"L": (240, 240), "S": (64, 80), "T": (32, 40)}
    face_w, face_h = image_size_spec[image_size]
    face_images = san10_load_face(face_file, count)
    save_faces(face_images, face_w, face_h, prefix, tag)


@click.command(help="顏CG解析")
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('-t', '--tag', 'tag', default='SAN11', help='')
@click.option('--count', 'count', default=9999, help='')
@click.option('--prefix', 'prefix', help='')
def san11_face(face_file, tag, prefix, count):
    """三國志 X 頭像解析"""
    if not os.path.exists(tag):
        os.makedirs(tag)
        os.makedirs(tag+"/LARGE")
        os.makedirs(tag+"/SMALL1")
        os.makedirs(tag+"/SMALL2")

    with open(face_file, 'rb') as f:
        header = f.read(12)
        count1 = int.from_bytes(f.read(4), 'little')
        count2 = int.from_bytes(f.read(4), 'little')
        # print(count1, count2)
        f.read(count1 * 4)  # unknown
        block_infos = []
        for _ in range(count2):
            start_pos = int.from_bytes(f.read(4), 'little')
            data_size = int.from_bytes(f.read(4), 'little')
            block_infos.append((start_pos, data_size))
        small_images = []
        other_images = []
        large_count, small_count, other_count = 0, 0, 0
        counting = 0
        for idx, block_info in enumerate(block_infos):
            if counting >= count:
                break
            start_pos, data_size = block_info
            if data_size == 0:
                continue
            f.seek(start_pos)
            # pic_entry header, 24 bytes
            pe_sig = f.read(8)  # WFTX0010
            pe_size = int.from_bytes(f.read(4), 'little')
            pe_unknown1 = f.read(4)  # 0x01000000 (LARGE, SMALL all 1)
            face_w = int.from_bytes(f.read(2), 'little')
            face_h = int.from_bytes(f.read(2), 'little')
            bpp = int.from_bytes(f.read(1), 'little')  # 0x18 or 0x08
            pe_unknown2 = f.read(3)  # 0x000000 or 0x010000 (LARGE all 0, SMALL 大多 0, 8BPP or 有色盤者 1)
            pe_data = f.read(pe_size-24)

            # extract face image
            image = san11_load_face(pe_data, face_w, face_h, bpp)
            out_filename = ""
            if face_w == 240 and face_h == 240:
                large_count += 1
                out_filename = '{}/LARGE/{}L{:04d}.png'.format(tag, prefix, idx + 1)
            elif face_w == 64 and face_h == 80:
                small_count += 1
                small_images.append(image)
                out_filename = '{}/SMALL1/{}S{:04d}.png'.format(tag, prefix, idx + 1)
                if small_count % 2 == 0:
                    out_filename = '{}/SMALL2/{}S{:04d}.png'.format(tag, prefix, idx + 1)
            else:
                other_count += 1
                # other_images.append(image)
                # if pe_unknown2 != b'\x00\x00\x00':
                #     print('[{:04d}] {:>10s} {}, {}'.format(idx, hex(start_pos), data_size, pe_unknown2))
            # save single
            if out_filename != "":
                image.save(out_filename)
                print("... save {}".format(out_filename))
                counting += 1
        # save index
        print('saving index file')
        small_face_w = 64
        small_face_h = 80
        img_w = small_face_w * 16
        img_h = small_face_h * math.ceil(small_count / 2 / 16)
        index_image1 = Image.new('RGB', (img_w, img_h), color=(55, 55, 55))
        index_image2 = Image.new('RGB', (img_w, img_h), color=(55, 55, 55))
        out_filename1 = '{}/{}S00-INDEX1.png'.format(tag, prefix)
        out_filename2 = '{}/{}S00-INDEX2.png'.format(tag, prefix)
        for idx, img_pair in enumerate(grouper(small_images, 2, incomplete='ignore')):
            pos_x = (idx % 16) * small_face_w
            pos_y = (idx // 16) * small_face_h
            index_image1.paste(img_pair[0], (pos_x, pos_y))
            index_image2.paste(img_pair[1], (pos_x, pos_y))
        index_image1.save(out_filename1)
        index_image2.save(out_filename2)

        # final print
        print('LARGE:{}, SMALL:{}, OTHER:{}'.format(large_count, small_count, other_count))
        print('total counting: {}'.format(counting))


@click.command(help="顏CG解析")
@click.option('-f', '--face', 'face_file', help="頭像檔案", required=True)
@click.option('--index', 'index_file', help="索引檔案")
@click.option('-t', '--tag', 'tag', default='SAN12', help='')
@click.option('--count', 'count', default=9999, help='')
@click.option('--prefix', 'prefix', help='')
def san12_face(face_file, index_file, tag, prefix, count):
    if index_file is not None:
        face_w, face_h, canvas_w, canvas_h = 32, 32, 32, 32
        if "F_M" in face_file:
            face_w, face_h, canvas_w, canvas_h = 48, 60, 64, 64
        elif "W_S" in face_file:
            face_w, face_h, canvas_w, canvas_h = 90, 128, 128, 128
        elif "W_L" in face_file:
            face_w, face_h, canvas_w, canvas_h = 360, 512, 512, 512
        indexes = []
        with open(index_file, 'rb') as f:
            header = f.read(3)
            print('header: {}'.format(header))
            if header == b"S12":
                print("This is a S12 index file.")
                indexes = None
            else:
                f.seek(0)
                idx_count = int.from_bytes(f.read(4), 'little')
                while True:
                    raw = f.read(4)
                    if raw == b'':
                        break
                    indexes.append(int.from_bytes(raw, 'little'))
        with open(face_file, 'rb') as f:
            start_pos, data_size = 0, -1
            face_images = san12_decode_group(f, start_pos, data_size, canvas_w, canvas_h, face_w, face_h, indexes)
            save_faces(face_images, face_w, face_h, prefix, tag, crop_size=(0, 0, face_w, face_h))
        return
    with open(face_file, 'rb') as f:
        header = f.read(4)
        count = int.from_bytes(f.read(4), 'little')
        u = f.read(8)  # 01000000 00000000, unknown
        print(' '.join(['%02x' % b for b in u]))
        group_infos = []
        for _ in range(count):
            start_pos = int.from_bytes(f.read(4), 'little')
            data_size = int.from_bytes(f.read(4), 'little')
            group_infos.append((start_pos, data_size))
        for idx, group_info in enumerate(group_infos):
            start_pos, datasize = group_info
            f.seek(start_pos)
            group_header = f.read(4)
            group_count = int.from_bytes(f.read(4), 'little')
            group_u = f.read(8)  # (face:2000) 20000000 d0070000, (item:179) 20000000 b3000000
            group_u2 = f.read(16)  # A03E0000 00000000 00000000 00000000
            print('[{}{}] {:5d}: {}'.format(group_header, idx, group_count, ' '.join(['%02x' % b for b in group_u])))
            # groups
            # [0] FACE 64x64x32bpp, 2000 (48x60)
            # [1] FACE 32x32x32bpp, 2000
            # [2] BUST 512x512x32bpp, 2000 (360x512)
            # [3] BUST 128x128x32bpp, 2000 (90x128)
            # [4] ITEM, 179
            # [5] 'LZP2' --17bytes-> 'LINK'
        # start_pos, data_size = group_infos[0]
        # face_images = san12_decode_group(f, start_pos, data_size, 64, 64, 48, 60)
        # save_faces(face_images, 48, 60, prefix, tag, crop_size=(0, 0, 48, 60))
        start_pos, data_size = group_infos[2]
        face_images = san12_decode_group(f, start_pos, data_size, 512, 512, 360, 512)
        save_faces(face_images, 360, 512, prefix, tag, crop_size=(0, 0, 360, 512))


@click.command(help="顏CG解析")
@click.option('-d', '--data', 'data_file', help="資料檔案", required=True)
@click.option('-t', '--tag', 'tag', default='SAN13', help='')
@click.option('--count', 'count', default=9999, help='')
@click.option('--prefix', 'prefix', help='')
def san13_face(data_file, tag, prefix, count):
    data0 = data_file
    data1 = data_file.replace('0', '1')
    # print(data0, ':', data1)
    data_groups = []
    with open(data0, 'rb') as f:
        idx = 0
        while dd1 := f.read(8):
            start_pos = int.from_bytes(dd1, 'little')
            u1 = int.from_bytes(f.read(8), 'little')  # unzip size?
            size = int.from_bytes(f.read(8), 'little')
            u3 = int.from_bytes(f.read(8), 'little')  # zip or not
            # print('[{}] {}, {}'.format(idx, start_pos, size))
            data_groups.append((start_pos, u1, size, u3))
            idx += 1
    # [XSMALL]
    # group_idx = 20
    # crops = (0, 0, 72, 72)
    # alpha = False
    # [LARGE]
    # group_idx = 8
    # crops = (0, 0, 633, 900)
    # alpha = True
    # [XLARGE]
    group_idx = 13
    crops = None
    alpha = True

    start_pos, _, size, _ = data_groups[group_idx]
    img_infos = []
    with open(data1, 'rb') as f:
        f.seek(start_pos)
        data = f.read(size)
        decode_raw(data, alpha, crops,  out_dir=tag, prefix=prefix)
        # img_count = int.from_bytes(f.read(4), 'little')
        # print(start_pos, img_count)
        # for idx in range(img_count):
        #     img_sp = int.from_bytes(f.read(4), 'little')
        #     img_sz = int.from_bytes(f.read(4), 'little')
        #     img_infos.append((img_sp, img_sz))
        #     print(idx, img_sp, img_sz, start_pos+img_sp)


san9.add_command(san9_face, "face")
san9.add_command(san9_person, "person")
san10.add_command(san10_face, "face")
san11.add_command(san11_face, "face")
san12.add_command(san12_face, "face")
san13.add_command(san13_face, "face")
dekoei.add_command(san9)
dekoei.add_command(san10)
dekoei.add_command(san11)
dekoei.add_command(san12)
dekoei.add_command(san13)
dekoei.add_command(san14)


if __name__ == '__main__':
    dekoei()
