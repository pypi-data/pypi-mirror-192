"""
Tests for the RIS class.
"""
from unittest import TestCase

from ris import RIS


class TestRIS(TestCase):
    """
    A test case for the RIS class.
    """

    def test_ris_decode_alpha(self):
        """
        Assert that alphabetic text can be decoded to RIS-codes.
        """
        self.assertEqual(RIS.decode("PT", encoding="alpha"), "🇵🇹")

    def test_ris_decode_html(self):
        """
        Assert that HTML can be decoded to RIS-codes.
        """
        self.assertEqual(
            RIS.decode("&#127467;&#127476;", encoding="html"), "🇫🇴")

    def test_ris_encode_alpha(self):
        """
        Assert that RIS-codes can be encoded to alphabetic text.
        """
        self.assertEqual(RIS("🇨🇦").encode(encoding="alpha"), "CA")

    def test_ris_encode_html(self):
        """
        Assert that RIS-codes can be encoded to HTML.
        """
        self.assertEqual(
            RIS("🇳🇱").encode(encoding="html"), "&#127475;&#127473;")

    def test_ris_decode_error(self):
        """
        Assert that invalid RIS-codes will result in an error.
        """
        with self.assertRaises(AssertionError):
            RIS.decode("123")
