from . import chart as chart
from _typeshed import Incomplete

class ChartScatter(chart.Chart):
    subtype: Incomplete
    cross_between: str
    horiz_val_axis: int
    val_axis_position: str
    smooth_allowed: bool
    requires_category: bool
    label_position_default: str
    label_positions: Incomplete
    def __init__(self, options: Incomplete | None = None) -> None: ...
    def combine(self, chart: Incomplete | None = None) -> None: ...
