from . import chart as chart
from _typeshed import Incomplete

class ChartArea(chart.Chart):
    subtype: Incomplete
    cross_between: str
    show_crosses: bool
    label_position_default: str
    label_positions: Incomplete
    def __init__(self, options: Incomplete | None = None) -> None: ...
