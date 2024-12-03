import re

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
