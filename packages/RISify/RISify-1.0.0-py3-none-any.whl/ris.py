"""
Definition of the RIS module.
"""

import re

from markupsafe import Markup


class RIS:
    """
    Wraps a RIS-string and provides several functions for encoding and decoding
    from and to plain alphabetic text and HTML.
    """

    _ORD_A = ord("A")
    _ORD_A_RIS = ord("🇦")
    _ORD_Z_RIS = ord("🇿")

    def __init__(self, code: str):
        assert self.is_valid(code), f"specified ris-code \"{code}\" is invalid"
        self._code = code

    def __str__(self):
        return self._code

    def __eq__(self, other):
        if isinstance(other, RIS):
            return str(self) == str(other)
        if not isinstance(other, str):
            raise NotImplementedError
        if self.is_valid(other):
            return str(self) == other
        if other.isalpha():
            return str(self) == str(RIS.decode(other))
        return str(self) == str(RIS.decode(other, encoding="html"))

    def __ne__(self, other):
        return not other == self

    def encode(self, encoding: str = "alpha"):
        """
        Encode the current RIS-code. Currently, supports encoding to
        alphabetic text and HTML-encoding.
        """
        if encoding == "html":
            return Markup("".join([
                f"&#{ord(c)};" for c in self._code
            ]))

        if encoding == "alpha":
            return "".join([
                chr(self._ORD_A + (ord(c) - self._ORD_A_RIS))
                for c in self._code.upper()
            ])

        raise NotImplementedError(f"specified encoding \"{encoding}\" unknown")

    @classmethod
    def decode(cls, code, encoding="alpha"):
        """
        Decode the specified code into a RIS-code.
        """
        if encoding == "html":
            ris = ""
            pattern = re.compile(r"&#(\d{6});")
            for match in pattern.finditer(code):
                ris = ris + chr(int(match[1]))
            return cls(ris)

        if encoding == "alpha":
            return cls("".join([
                chr(cls._ORD_A_RIS + (ord(c) - cls._ORD_A)) for c in code
            ]))

        raise NotImplementedError(f"specified encoding \"{encoding}\" unknown")

    @staticmethod
    def is_valid(code: str) -> bool:
        """
        Indicate whether the specified string is a valid RIS-code.
        """
        return all(RIS._ORD_A_RIS <= ord(c) <= RIS._ORD_Z_RIS for c in code)
