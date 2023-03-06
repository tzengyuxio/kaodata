from utils import *


def test_to_indexes():
    # test of to_2bpp_indexes
    data = bytes(b'\x42\x04\x53\x0A')
    expected = [0, 2, 0, 0, 0, 1, 2, 0, 0, 2, 0, 2, 1, 0, 3, 2]
    assert to_2bpp_indexes(data) == expected

    # test of to_3bpp_indexes
    data = bytes(b'\x00\xFF\xAA\x57\x02\x00')
    expected = [3, 2, 3, 2, 3, 2, 3, 2, 0, 4, 0, 4, 0, 4, 6, 4]
    assert to_3bpp_indexes(data) == expected
