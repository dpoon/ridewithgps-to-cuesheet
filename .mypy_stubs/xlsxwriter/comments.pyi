from . import xmlwriter as xmlwriter
from .utility import xl_cell_to_rowcol as xl_cell_to_rowcol, xl_rowcol_to_cell as xl_rowcol_to_cell
from _typeshed import Incomplete

class CommentType:
    row: int
    col: int
    text: str
    author: str | None
    color: str
    start_row: int
    start_col: int
    is_visible: bool | None
    width: float
    height: float
    x_scale: float
    y_scale: float
    x_offset: int
    y_offset: int
    font_size: float
    font_name: str
    font_family: int
    vertices: list[int | float]
    def __init__(self, row: int, col: int, text: str, options: dict[str, str | int | float] | None = None) -> None: ...
    def set_offsets(self, row: int, col: int): ...

class Comments(xmlwriter.XMLwriter):
    author_ids: Incomplete
    def __init__(self) -> None: ...
