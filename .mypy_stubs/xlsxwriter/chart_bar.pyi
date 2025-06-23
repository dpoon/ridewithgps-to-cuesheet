from . import chart as chart
from _typeshed import Incomplete

class ChartBar(chart.Chart):
    subtype: Incomplete
    cat_axis_position: str
    val_axis_position: str
    horiz_val_axis: int
    horiz_cat_axis: int
    show_crosses: bool
    label_position_default: str
    label_positions: Incomplete
    def __init__(self, options: Incomplete | None = None) -> None: ...
    combined: Incomplete
    def combine(self, chart: Incomplete | None = None) -> None: ...
