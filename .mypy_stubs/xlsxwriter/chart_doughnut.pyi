from . import chart_pie as chart_pie

class ChartDoughnut(chart_pie.ChartPie):
    vary_data_color: int
    rotation: int
    hole_size: int
    def __init__(self) -> None: ...
    def set_hole_size(self, size) -> None: ...
