from . import worksheet as worksheet
from .drawing import Drawing as Drawing
from _typeshed import Incomplete

class Chartsheet(worksheet.Worksheet):
    is_chartsheet: bool
    drawing: Incomplete
    chart: Incomplete
    charts: Incomplete
    zoom_scale_normal: int
    orientation: int
    protection: bool
    def __init__(self) -> None: ...
    def set_chart(self, chart): ...
    def protect(self, password: str = '', options: Incomplete | None = None) -> None: ...
