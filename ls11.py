from bitstream import BitStream
from rich.progress import track

LS11_ENDIAN = 'big'
LS11_MAGIC = [b'LS11', b'Ls12']


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
                try:
                    recover_data.append(recover_data[pos])
                except IndexError:
                    # TODO: review this exception handler
                    print(f"IndexError: {len(recover_data)=}, {pos=}, {delta=}")
                    recover_data.append(0)
            delta = 0
        elif code < 256:  # replace code with dictionary
            recover_data.append(dictionary[code])
        else:  # copy operation
            delta = code - 256
    return bytes(recover_data)


def ls11_decode_parts(data: bytes, print_only=False) -> list[bytes]:
    if data[:4] not in LS11_MAGIC:
        # TODO(yuxioz): wrong header, log chars here.
        return []

    dictionary = data[16:16+256]
    pos = 16+256
    infos = []
    while data[pos:pos+4] != b'\x00\x00\x00\x00':
        compressed_size = int.from_bytes(data[pos:pos+4], LS11_ENDIAN)
        uncompressed_size = int.from_bytes(data[pos+4:pos+8], LS11_ENDIAN)
        offset = int.from_bytes(data[pos+8:pos+12], LS11_ENDIAN)
        infos.append((compressed_size, uncompressed_size, offset))
        pos += 12

    if print_only:
        for info in infos:
            compressed_size, uncompressed_size, offset = info
            header = data[offset:offset+3]
            if header == b'NPK':
                print(info, 'NPK')
            else:
                print(info)
        return []

    decoded_data = []
    # for i in track(range(len(infos)), description="Decoding... "):
    # rich.errors.LiveError: Only one live display may be active at once
    for i in range(len(infos)):
        compressed_size, uncompressed_size, offset = infos[i]
        compressed_data = data[offset:offset+compressed_size]
        if compressed_size == uncompressed_size:
            decoded_data.append(compressed_data)
            continue
        codes = get_codes(compressed_data)
        recover_data = recover(codes, dictionary)
        decoded_data.append(recover_data[:uncompressed_size])

    return decoded_data


def ls11_decode(data: bytes, print_only=False) -> bytes:
    decoded_data = ls11_decode_parts(data, print_only)
    if len(decoded_data) == 0:
        return b''

    return b''.join(decoded_data)
