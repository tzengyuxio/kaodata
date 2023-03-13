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


def test_to_2bpp_indexes():
    # Test 1: Test if the function returns a list of integers for a given input
    assert isinstance(to_2bpp_indexes(b'\x00\x01\x02\x03'), list)
    assert all(isinstance(i, int) for i in to_2bpp_indexes(b'\x00\x01\x02\x03'))

    # Test 2: Test if the function returns an empty list for an empty input
    assert to_2bpp_indexes(b'') == []

    # Test 3: Test if the function correctly handles incomplete bytes in the input data
    assert to_2bpp_indexes(b'\x01\x02\x03') == [0, 0, 0, 0, 0, 0, 1, 2]
    assert to_2bpp_indexes(b'\x01\x02\x03\x04\x05') == [0, 0, 0, 0, 0, 0, 1, 2,
                                                        0, 0, 0, 0, 0, 1, 2, 2]

    # Test 4: Test if the function correctly converts the input data into 2bpp indexes
    assert to_2bpp_indexes(b'\x00\x00\x00\x00') == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert to_2bpp_indexes(b'\xFF\xFF\xFF\xFF') == [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    assert to_2bpp_indexes(b'\xAA\x55\xAA\x55') == [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]


def test_count_in_big5_v2():
    # Test 1: Test if the function returns an integer for a given input
    assert isinstance(count_in_big5_v2('0001'), int)

    # Test 2: Test normal input
    assert count_in_big5_v2('A440') == 1    # A440 一 1
    assert count_in_big5_v2('B0A1') == 1948 # B0A1 陛 1948
    assert count_in_big5_v2('B0AF') == 1962 # B0AF 偺
    assert count_in_big5_v2('B1D7') == 2159 # B1D7 斜

    # Test 3: Test edge cases
    assert count_in_big5_v2('A140') == 1
