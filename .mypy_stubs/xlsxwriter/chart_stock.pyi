from . import chart as chart
from _typeshed import Incomplete

class ChartStock(chart.Chart):
    show_crosses: bool
    hi_low_lines: Incomplete
    date_category: bool
    label_position_default: str
    label_positions: Incomplete
    def __init__(self) -> None: ...
