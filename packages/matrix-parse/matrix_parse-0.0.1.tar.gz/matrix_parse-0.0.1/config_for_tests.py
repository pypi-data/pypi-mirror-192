SOURCE_URL = "https://raw.githubusercontent.com/koury/pymx/main/source.txt"
WRONG_URL = "https://somewrongdomain.net/"
EXPECTED_FROM_SOURCE_URL = [
    160, 150, 140, 130,
    90, 50, 10, 20,
    30, 40, 80, 120,
    110, 100, 60, 70,
]
INPUT_MATRIX_2x2 = [[1, 2], [3, 4]]
UNPACKED_MATRIX_2x2 = [4, 3, 1, 2]

INPUT_MATRIX_3x3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
UNPACKED_MATRIX_3x3 = [9, 8, 7, 4, 1, 2, 3, 6, 5]

INPUT_MATRIX_5x5 = [
    [9, 10, 11, 12, 13],
    [8, 21, 22, 23, 14],
    [7, 20, 25, 24, 15],
    [6, 19, 18, 17, 16],
    [5, 4, 3, 2, 1]
]
UNPACKED_MATRIX_5x5 = [num for num in range(1, 26)]

ARRAY_WITH_4_elements = sum(INPUT_MATRIX_2x2, [])
ARRAY_WITH_9_elements = sum(INPUT_MATRIX_3x3, [])
ARRAY_WITH_25_elements = sum(INPUT_MATRIX_5x5, [])
