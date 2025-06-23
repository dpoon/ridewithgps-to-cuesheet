from . import chart as chart
from _typeshed import Incomplete

class ChartPie(chart.Chart):
    vary_data_color: int
    rotation: int
    label_position_default: str
    label_positions: Incomplete
    def __init__(self) -> None: ...
    def set_rotation(self, rotation) -> None: ...
