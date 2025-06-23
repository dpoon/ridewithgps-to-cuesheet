from . import xmlwriter as xmlwriter
from _typeshed import Incomplete

class Styles(xmlwriter.XMLwriter):
    xf_formats: Incomplete
    palette: Incomplete
    font_count: int
    num_formats: Incomplete
    border_count: int
    fill_count: int
    custom_colors: Incomplete
    dxf_formats: Incomplete
    has_hyperlink: bool
    hyperlink_font_id: int
    has_comments: bool
    def __init__(self) -> None: ...
