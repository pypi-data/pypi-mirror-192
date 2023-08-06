# Copyright (C) 2021,2022,2023 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""String helper functions for handling zh related text."""

from typing import Any
from unicodedata import numeric

WORD_NUMERIC_MAP = {
    "圩": 50.0,
    "圓": 60.0,
    "進": 70.0,
    "枯": 80.0,
    "枠": 90.0,
}


def zh_numeric(word: str, default: Any = None) -> Any:
    """Custom wrapper for unicodedata.numeric.

    This supports additional numeral values not supported by the existing
    library.

    Args:
        word(str): The Chinese character.
        default(Any): If set, a default value is used instead of raising
        exception.

    Returns:
        float: The numeric value of the Chinese character.
    """
    try:
        return numeric(word)
    except TypeError as terror:
        raise TypeError(
            "zh_numeric() argument 1 must be a unicode character, not str"
        ) from terror
    except ValueError as verror:
        try:
            return WORD_NUMERIC_MAP[word]
        except KeyError as kerror:
            if default is None:
                raise verror from kerror

            return default


# Unicode integer in hexadecimal for these characters.
FULLWIDTH_EXCLAMATION_MARK = 0xFF01
EXCLAMATION_MARK = 0x21
TILDE = 0x7E

# Mapping table for halfwidth ASCII characters to its fullwidth equivalent.
#
# Fullwidth is a text character that occupies two alphanumeric characters
# in monospace font.
#
# See Halfwidth and Fullwidth Forms in Unicode (https://w.wiki/66Ps) and
# Unicode block (https://w.wiki/66Pt).
HALFWIDTH_FULLWIDTH_MAP = {}
for i, j in enumerate(range(EXCLAMATION_MARK, TILDE + 1)):
    HALFWIDTH_FULLWIDTH_MAP[j] = FULLWIDTH_EXCLAMATION_MARK + i


def zh_halfwidth_to_fullwidth(words: str) -> str:
    """Convert halfwidth to fullwidth text.

    Args:
        words(str): The string contains halfwidth characters.

    Returns:
        str: The string contains fullwidth characters.
    """
    return words.translate(HALFWIDTH_FULLWIDTH_MAP)


__all__ = [
    "zh_halfwidth_to_fullwidth",
    "zh_numeric",
]
