import asyncio
import unittest
from parameterized import parameterized

from config_for_tests import (
    SOURCE_URL,
    EXPECTED_FROM_SOURCE_URL,
    WRONG_URL,
    INPUT_MATRIX_2x2,
    UNPACKED_MATRIX_2x2,
    INPUT_MATRIX_3x3,
    UNPACKED_MATRIX_3x3,
    INPUT_MATRIX_5x5,
    UNPACKED_MATRIX_5x5,
    ARRAY_WITH_4_elements,
    ARRAY_WITH_9_elements,
    ARRAY_WITH_25_elements
)
from matrix_parse import matrix_parse, unpack_matrix, create_matrix


class TestParseMatrix(unittest.TestCase):

    def test_with_correct_url(self):
        self.assertEqual(
            asyncio.run(matrix_parse(SOURCE_URL)), EXPECTED_FROM_SOURCE_URL
        )

    @parameterized.expand([
        ("test_with_404_response", SOURCE_URL + "make it wrong"),
        ("test_with_incorrect_url", WRONG_URL),
    ])
    def test_different_urls(self, _, url):
        self.assertIsNone(asyncio.run(matrix_parse(url)))


class TestUnpackMatrix(unittest.TestCase):

    @parameterized.expand([
        ("test_with_empty_matrix", [[]], []),
        ("test_with_matrix_2x2", INPUT_MATRIX_2x2, UNPACKED_MATRIX_2x2),
        ("test_with_matrix_3x3", INPUT_MATRIX_3x3, UNPACKED_MATRIX_3x3),
        ("test_with_matrix_5x5", INPUT_MATRIX_5x5, UNPACKED_MATRIX_5x5),
    ])
    def test_with_different_matrix(self, _, input_matrix, unpacked_matrix):
        self.assertEqual(
            unpack_matrix(input_matrix), unpacked_matrix
        )


class TestCreateMatrix(unittest.TestCase):

    @parameterized.expand([
        ("test_with_empty_matrix", [], [[]]),
        ("test_with_matrix_2x2", ARRAY_WITH_4_elements, INPUT_MATRIX_2x2),
        ("test_with_matrix_3x3", ARRAY_WITH_9_elements, INPUT_MATRIX_3x3),
        ("test_with_matrix_5x5", ARRAY_WITH_25_elements, INPUT_MATRIX_5x5),
    ])
    def test_with_different_arrays(self, _, array, matrix):
        self.assertEqual(
            create_matrix(array), matrix
        )
