from . import xmlwriter as xmlwriter
from _typeshed import Incomplete
from xlsxwriter.comments import CommentType as CommentType
from xlsxwriter.image import Image as Image

class ButtonType:
    row: Incomplete
    col: Incomplete
    width: Incomplete
    height: Incomplete
    macro: Incomplete
    caption: Incomplete
    description: Incomplete
    x_scale: int
    y_scale: int
    x_offset: int
    y_offset: int
    vertices: Incomplete
    def __init__(self, row: int, col: int, height: int, width: int, button_number: int, options: dict = None) -> None: ...

class Vml(xmlwriter.XMLwriter): ...
