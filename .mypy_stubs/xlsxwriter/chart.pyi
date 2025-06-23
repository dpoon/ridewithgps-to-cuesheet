from . import xmlwriter as xmlwriter
from .shape import Shape as Shape
from .utility import quote_sheetname as quote_sheetname, xl_range_formula as xl_range_formula, xl_rowcol_to_cell as xl_rowcol_to_cell
from _typeshed import Incomplete

class Chart(xmlwriter.XMLwriter):
    subtype: Incomplete
    sheet_type: int
    orientation: int
    series: Incomplete
    embedded: int
    id: int
    series_index: int
    style_id: int
    axis_ids: Incomplete
    axis2_ids: Incomplete
    cat_has_num_fmt: bool
    requires_category: bool
    legend: Incomplete
    cat_axis_position: str
    val_axis_position: str
    formula_ids: Incomplete
    formula_data: Incomplete
    horiz_cat_axis: int
    horiz_val_axis: int
    protection: int
    chartarea: Incomplete
    plotarea: Incomplete
    x_axis: Incomplete
    y_axis: Incomplete
    y2_axis: Incomplete
    x2_axis: Incomplete
    chart_name: str
    show_blanks: str
    show_na_as_empty: bool
    show_hidden: bool
    show_crosses: bool
    width: int
    height: int
    x_scale: int
    y_scale: int
    x_offset: int
    y_offset: int
    table: Incomplete
    cross_between: str
    default_marker: Incomplete
    series_gap_1: Incomplete
    series_gap_2: Incomplete
    series_overlap_1: Incomplete
    series_overlap_2: Incomplete
    drop_lines: Incomplete
    hi_low_lines: Incomplete
    up_down_bars: Incomplete
    smooth_allowed: bool
    title_font: Incomplete
    title_name: Incomplete
    title_formula: Incomplete
    title_data_id: Incomplete
    title_layout: Incomplete
    title_overlay: Incomplete
    title_none: bool
    date_category: bool
    date_1904: bool
    remove_timezone: bool
    label_positions: Incomplete
    label_position_default: str
    already_inserted: bool
    combined: Incomplete
    is_secondary: bool
    warn_sheetname: bool
    fill: Incomplete
    def __init__(self) -> None: ...
    def add_series(self, options: Incomplete | None = None) -> None: ...
    def set_x_axis(self, options) -> None: ...
    def set_y_axis(self, options) -> None: ...
    def set_x2_axis(self, options) -> None: ...
    def set_y2_axis(self, options) -> None: ...
    def set_title(self, options: Incomplete | None = None) -> None: ...
    def set_legend(self, options) -> None: ...
    def set_plotarea(self, options) -> None: ...
    def set_chartarea(self, options) -> None: ...
    def set_style(self, style_id) -> None: ...
    def show_blanks_as(self, option) -> None: ...
    def show_na_as_empty_cell(self) -> None: ...
    def show_hidden_data(self) -> None: ...
    def set_size(self, options: Incomplete | None = None) -> None: ...
    def set_table(self, options: Incomplete | None = None) -> None: ...
    def set_up_down_bars(self, options: Incomplete | None = None) -> None: ...
    def set_drop_lines(self, options: Incomplete | None = None) -> None: ...
    def set_high_low_lines(self, options: Incomplete | None = None) -> None: ...
    def combine(self, chart: Incomplete | None = None) -> None: ...
