from functools import reduce
from utils import *
from bitstream import BitStream


def get_codes(data: bytes) -> list[int]:
    """將壓縮資料轉換為字典索引值 list"""
    codes = []
    stream = BitStream(data, bytes)
    mask_len, pos, pos_end = 0, 0, len(data)*8
    while True:
        bit = stream.read(bool)
        mask_len += 1
        pos += 1
        if not bit:
            mask = (1 << mask_len) - 2
            factor = 0
            for _ in range(mask_len):
                factor = (factor << 1) | stream.read(bool)
            codes.append(mask+factor)
            pos += mask_len
            mask_len = 0
        if pos >= pos_end:
            break
    return codes


def recover(codes: list[int], dictionary: bytes) -> bytes:
    """從字典索引值與字典還原原始數據"""
    recover_data = bytearray()
    delta = 0
    for code in codes:
        if delta > 0:
            nc = 3 + code  # number of copy
            for _ in range(nc):
                pos = len(recover_data) - delta
                recover_data.append(recover_data[pos])
            delta = 0
        elif code < 256:  # replace code with dictionary
            recover_data.append(dictionary[code])
        else:  # copy operation
            delta = code - 256
    return bytes(recover_data)


def ls11_decode(data: bytes) -> bytes:
    if data[:4] not in [b'LS11', b'LS10', b'LS12']:
        # TODO(yuxioz): wrong header, log chars here.
        return bytes()

    dictionary = data[16:16+256]
    pos = 16+256
    infos = []
    while data[pos:pos+4] != b'\x00\x00\x00\x00':
        compressed_size = int.from_bytes(data[pos:pos+4], BIG_ENDIAN)
        uncompressed_size = int.from_bytes(data[pos+4:pos+8], BIG_ENDIAN)
        offset = int.from_bytes(data[pos+8:pos+12], BIG_ENDIAN)
        infos.append((compressed_size, uncompressed_size, offset))
        pos += 12

    decoded_data = bytearray()
    for i in range(len(infos)):
        compressed_size, uncompressed_size, offset = infos[i]
        compressed_data = data[offset:offset+compressed_size]
        codes = get_codes(compressed_data)
        recover_data = recover(codes, dictionary)
        decoded_data.extend(recover_data[:uncompressed_size])

    return bytes(decoded_data)
