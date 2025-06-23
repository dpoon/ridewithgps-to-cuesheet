from . import xmlwriter as xmlwriter
from .shape import Shape as Shape
from _typeshed import Incomplete
from enum import Enum
from xlsxwriter.url import Url as Url

class DrawingTypes(Enum):
    NONE = 0
    CHART = 1
    IMAGE = 2
    SHAPE = 3

class DrawingInfo:
    def __init__(self) -> None: ...

class Drawing(xmlwriter.XMLwriter):
    drawings: Incomplete
    embedded: int
    orientation: int
    def __init__(self) -> None: ...
