import re

from enum import Enum
from typing import TypedDict


class StartParams(TypedDict):
    context: list
    token: str


class EndParams(TypedDict):
    context: list
    token: str


class ProcessParams(TypedDict):
    context: list
    match: re.Match


class AtomMatchParams(TypedDict):
    context: list
    text: str


class NumberingType(Enum):
    DECIMAL = 1
    ALPHABETIC = 2
    ROMAN_NUMERALS = 3

    def __str__(self) -> str:
        return self.name


class Separator(Enum):
    PERIOD = 1
    CLOSING_PAREN = 2

    def __str__(self) -> str:
        return self.name


class Alignment(Enum):
    ALIGN_DEFAULT = 1
    ALIGN_CENTER = 2
    ALIGN_LEFT = 3
    ALIGN_RIGHT = 4

    def __str__(self) -> str:
        return self.name
