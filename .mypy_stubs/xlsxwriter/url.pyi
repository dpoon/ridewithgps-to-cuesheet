from enum import Enum

class UrlTypes(Enum):
    UNKNOWN = 0
    URL = 1
    INTERNAL = 2
    EXTERNAL = 3

class Url:
    MAX_URL_LEN: int
    MAX_PARAMETER_LEN: int
    def __init__(self, link: str) -> None: ...
    @classmethod
    def from_options(cls, options: dict) -> Url | None: ...
    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, value: str): ...
    @property
    def tip(self) -> str: ...
    @tip.setter
    def tip(self, value: str): ...
