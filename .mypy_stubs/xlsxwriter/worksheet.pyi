from . import xmlwriter as xmlwriter
from .drawing import Drawing as Drawing, DrawingInfo as DrawingInfo, DrawingTypes as DrawingTypes
from .exceptions import DuplicateTableName as DuplicateTableName, OverlappingRange as OverlappingRange
from .format import Format as Format
from .shape import Shape as Shape
from .utility import quote_sheetname as quote_sheetname, xl_cell_to_rowcol as xl_cell_to_rowcol, xl_col_to_name as xl_col_to_name, xl_pixel_width as xl_pixel_width, xl_range as xl_range, xl_rowcol_to_cell as xl_rowcol_to_cell, xl_rowcol_to_cell_fast as xl_rowcol_to_cell_fast
from .xmlwriter import XMLwriter as XMLwriter
from _typeshed import Incomplete
from typing import NamedTuple
from xlsxwriter.comments import CommentType as CommentType
from xlsxwriter.image import Image as Image
from xlsxwriter.url import Url as Url, UrlTypes as UrlTypes
from xlsxwriter.vml import ButtonType as ButtonType

re_dynamic_function: Incomplete

def convert_cell_args(method): ...
def convert_range_args(method): ...
def convert_column_args(method): ...

class CellBlankTuple(NamedTuple):
    format: Incomplete

class CellErrorTuple(NamedTuple):
    error: Incomplete
    format: Incomplete
    value: Incomplete

class CellNumberTuple(NamedTuple):
    number: Incomplete
    format: Incomplete

class CellStringTuple(NamedTuple):
    string: Incomplete
    format: Incomplete

class CellBooleanTuple(NamedTuple):
    boolean: Incomplete
    format: Incomplete

class CellFormulaTuple(NamedTuple):
    formula: Incomplete
    format: Incomplete
    value: Incomplete

class CellDatetimeTuple(NamedTuple):
    number: Incomplete
    format: Incomplete

class CellRichStringTuple(NamedTuple):
    string: Incomplete
    format: Incomplete
    raw_string: Incomplete

class CellArrayFormulaTuple(NamedTuple):
    formula: Incomplete
    format: Incomplete
    value: Incomplete
    range: Incomplete
    atype: Incomplete

class Worksheet(xmlwriter.XMLwriter):
    name: Incomplete
    index: Incomplete
    str_table: Incomplete
    palette: Incomplete
    constant_memory: int
    tmpdir: Incomplete
    is_chartsheet: bool
    ext_sheets: Incomplete
    fileclosed: int
    excel_version: int
    excel2003_style: bool
    xls_rowmax: int
    xls_colmax: int
    xls_strmax: int
    dim_rowmin: Incomplete
    dim_rowmax: Incomplete
    dim_colmin: Incomplete
    dim_colmax: Incomplete
    col_info: Incomplete
    selections: Incomplete
    hidden: int
    active: int
    tab_color: int
    top_left_cell: str
    panes: Incomplete
    active_pane: int
    selected: int
    page_setup_changed: bool
    paper_size: int
    orientation: int
    print_options_changed: bool
    hcenter: bool
    vcenter: bool
    print_gridlines: bool
    screen_gridlines: bool
    print_headers: bool
    row_col_headers: bool
    header_footer_changed: bool
    header: str
    footer: str
    header_footer_aligns: bool
    header_footer_scales: bool
    header_images: Incomplete
    footer_images: Incomplete
    header_images_list: Incomplete
    margin_left: float
    margin_right: float
    margin_top: float
    margin_bottom: float
    margin_header: float
    margin_footer: float
    repeat_row_range: str
    repeat_col_range: str
    print_area_range: str
    page_order: int
    black_white: int
    draft_quality: int
    print_comments: int
    page_start: int
    fit_page: int
    fit_width: int
    fit_height: int
    hbreaks: Incomplete
    vbreaks: Incomplete
    protect_options: Incomplete
    protected_ranges: Incomplete
    num_protected_ranges: int
    set_cols: Incomplete
    set_rows: Incomplete
    zoom: int
    zoom_scale_normal: int
    print_scale: int
    is_right_to_left: bool
    show_zeros: int
    leading_zeros: int
    outline_row_level: int
    outline_col_level: int
    outline_style: int
    outline_below: int
    outline_right: int
    outline_on: int
    outline_changed: bool
    original_row_height: int
    default_row_height: int
    default_row_pixels: int
    default_col_width: float
    default_col_pixels: int
    default_date_pixels: int
    default_row_zeroed: int
    names: Incomplete
    write_match: Incomplete
    table: Incomplete
    merge: Incomplete
    merged_cells: Incomplete
    table_cells: Incomplete
    row_spans: Incomplete
    has_vml: bool
    has_header_vml: bool
    has_comments: bool
    comments: Incomplete
    comments_list: Incomplete
    comments_author: str
    comments_visible: bool
    vml_shape_id: int
    buttons_list: Incomplete
    vml_header_id: int
    autofilter_area: str
    autofilter_ref: Incomplete
    filter_range: Incomplete
    filter_on: int
    filter_cols: Incomplete
    filter_type: Incomplete
    filter_cells: Incomplete
    row_sizes: Incomplete
    col_size_changed: bool
    row_size_changed: bool
    last_shape_id: int
    rel_count: int
    hlink_count: int
    hlink_refs: Incomplete
    external_hyper_links: Incomplete
    external_drawing_links: Incomplete
    external_comment_links: Incomplete
    external_vml_links: Incomplete
    external_table_links: Incomplete
    external_background_links: Incomplete
    drawing_links: Incomplete
    vml_drawing_links: Incomplete
    charts: Incomplete
    images: Incomplete
    tables: Incomplete
    sparklines: Incomplete
    shapes: Incomplete
    shape_hash: Incomplete
    drawing: int
    drawing_rels: Incomplete
    drawing_rels_id: int
    vml_drawing_rels: Incomplete
    vml_drawing_rels_id: int
    background_image: Incomplete
    rstring: str
    previous_row: int
    validations: Incomplete
    cond_formats: Incomplete
    data_bars_2010: Incomplete
    use_data_bars_2010: bool
    dxf_priority: int
    page_view: int
    vba_codename: Incomplete
    date_1904: bool
    hyperlinks: Incomplete
    strings_to_numbers: bool
    strings_to_urls: bool
    nan_inf_to_errors: bool
    strings_to_formulas: bool
    default_date_format: Incomplete
    default_url_format: Incomplete
    default_checkbox_format: Incomplete
    workbook_add_format: Incomplete
    remove_timezone: bool
    max_url_length: int
    row_data_filename: Incomplete
    row_data_fh: Incomplete
    worksheet_meta: Incomplete
    vml_data_id: Incomplete
    row_data_fh_closed: bool
    vertical_dpi: int
    horizontal_dpi: int
    write_handlers: Incomplete
    ignored_errors: Incomplete
    has_dynamic_arrays: bool
    use_future_functions: bool
    ignore_write_string: bool
    embedded_images: Incomplete
    def __init__(self) -> None: ...
    @convert_cell_args
    def write(self, row, col, *args): ...
    @convert_cell_args
    def write_string(self, row, col, string, cell_format: Incomplete | None = None): ...
    @convert_cell_args
    def write_number(self, row, col, number, cell_format: Incomplete | None = None): ...
    @convert_cell_args
    def write_blank(self, row, col, blank, cell_format: Incomplete | None = None): ...
    @convert_cell_args
    def write_formula(self, row, col, formula, cell_format: Incomplete | None = None, value: int = 0): ...
    @convert_range_args
    def write_array_formula(self, first_row, first_col, last_row, last_col, formula, cell_format: Incomplete | None = None, value: int = 0): ...
    @convert_range_args
    def write_dynamic_array_formula(self, first_row, first_col, last_row, last_col, formula, cell_format: Incomplete | None = None, value: int = 0): ...
    @convert_cell_args
    def write_datetime(self, row, col, date, cell_format: Incomplete | None = None): ...
    @convert_cell_args
    def write_boolean(self, row, col, boolean, cell_format: Incomplete | None = None): ...
    @convert_cell_args
    def write_url(self, row, col, url, cell_format: Incomplete | None = None, string: Incomplete | None = None, tip: Incomplete | None = None): ...
    @convert_cell_args
    def write_rich_string(self, row, col, *args): ...
    def add_write_handler(self, user_type, user_function) -> None: ...
    @convert_cell_args
    def write_row(self, row, col, data, cell_format: Incomplete | None = None): ...
    @convert_cell_args
    def write_column(self, row, col, data, cell_format: Incomplete | None = None): ...
    @convert_cell_args
    def insert_image(self, row, col, source, options: Incomplete | None = None): ...
    @convert_cell_args
    def embed_image(self, row, col, source, options: Incomplete | None = None): ...
    @convert_cell_args
    def insert_textbox(self, row, col, text, options: Incomplete | None = None): ...
    @convert_cell_args
    def insert_chart(self, row, col, chart, options: Incomplete | None = None): ...
    @convert_cell_args
    def write_comment(self, row, col, comment, options: Incomplete | None = None): ...
    def show_comments(self) -> None: ...
    def set_background(self, source, is_byte_stream: bool = False): ...
    def set_comments_author(self, author) -> None: ...
    def get_name(self): ...
    def activate(self) -> None: ...
    def select(self) -> None: ...
    def hide(self) -> None: ...
    def very_hidden(self) -> None: ...
    def set_first_sheet(self) -> None: ...
    @convert_column_args
    def set_column(self, first_col, last_col, width: Incomplete | None = None, cell_format: Incomplete | None = None, options: Incomplete | None = None): ...
    @convert_column_args
    def set_column_pixels(self, first_col, last_col, width: Incomplete | None = None, cell_format: Incomplete | None = None, options: Incomplete | None = None): ...
    def autofit(self, max_width: int = 1790) -> None: ...
    def set_row(self, row, height: Incomplete | None = None, cell_format: Incomplete | None = None, options: Incomplete | None = None): ...
    def set_row_pixels(self, row, height: Incomplete | None = None, cell_format: Incomplete | None = None, options: Incomplete | None = None): ...
    def set_default_row(self, height: Incomplete | None = None, hide_unused_rows: bool = False) -> None: ...
    @convert_range_args
    def merge_range(self, first_row, first_col, last_row, last_col, data, cell_format: Incomplete | None = None): ...
    @convert_range_args
    def autofilter(self, first_row, first_col, last_row, last_col) -> None: ...
    def filter_column(self, col, criteria) -> None: ...
    def filter_column_list(self, col, filters) -> None: ...
    @convert_range_args
    def data_validation(self, first_row, first_col, last_row, last_col, options: Incomplete | None = None): ...
    @convert_range_args
    def conditional_format(self, first_row, first_col, last_row, last_col, options: Incomplete | None = None): ...
    @convert_range_args
    def add_table(self, first_row, first_col, last_row, last_col, options: Incomplete | None = None): ...
    @convert_cell_args
    def add_sparkline(self, row, col, options: Incomplete | None = None): ...
    @convert_range_args
    def set_selection(self, first_row, first_col, last_row, last_col) -> None: ...
    @convert_cell_args
    def set_top_left_cell(self, row: int = 0, col: int = 0) -> None: ...
    def outline_settings(self, visible: int = 1, symbols_below: int = 1, symbols_right: int = 1, auto_style: int = 0) -> None: ...
    @convert_cell_args
    def freeze_panes(self, row, col, top_row: Incomplete | None = None, left_col: Incomplete | None = None, pane_type: int = 0) -> None: ...
    @convert_cell_args
    def split_panes(self, x, y, top_row: Incomplete | None = None, left_col: Incomplete | None = None) -> None: ...
    def set_zoom(self, zoom: int = 100) -> None: ...
    def right_to_left(self) -> None: ...
    def hide_zero(self) -> None: ...
    def set_tab_color(self, color) -> None: ...
    def protect(self, password: str = '', options: Incomplete | None = None) -> None: ...
    def unprotect_range(self, cell_range, range_name: Incomplete | None = None, password: Incomplete | None = None): ...
    @convert_cell_args
    def insert_button(self, row, col, options: Incomplete | None = None): ...
    @convert_cell_args
    def insert_checkbox(self, row, col, boolean, cell_format: Incomplete | None = None): ...
    def set_landscape(self) -> None: ...
    def set_portrait(self) -> None: ...
    def set_page_view(self, view: int = 1) -> None: ...
    def set_pagebreak_view(self) -> None: ...
    def set_paper(self, paper_size) -> None: ...
    def center_horizontally(self) -> None: ...
    def center_vertically(self) -> None: ...
    def set_margins(self, left: float = 0.7, right: float = 0.7, top: float = 0.75, bottom: float = 0.75) -> None: ...
    def set_header(self, header: str = '', options: Incomplete | None = None, margin: Incomplete | None = None) -> None: ...
    def set_footer(self, footer: str = '', options: Incomplete | None = None, margin: Incomplete | None = None) -> None: ...
    def repeat_rows(self, first_row, last_row: Incomplete | None = None) -> None: ...
    @convert_column_args
    def repeat_columns(self, first_col, last_col: Incomplete | None = None) -> None: ...
    def hide_gridlines(self, option: int = 1) -> None: ...
    def print_row_col_headers(self) -> None: ...
    def hide_row_col_headers(self) -> None: ...
    @convert_range_args
    def print_area(self, first_row, first_col, last_row, last_col): ...
    def print_across(self) -> None: ...
    def fit_to_pages(self, width, height) -> None: ...
    def set_start_page(self, start_page) -> None: ...
    def set_print_scale(self, scale) -> None: ...
    def print_black_and_white(self) -> None: ...
    def set_h_pagebreaks(self, breaks) -> None: ...
    def set_v_pagebreaks(self, breaks) -> None: ...
    def set_vba_name(self, name: Incomplete | None = None) -> None: ...
    def ignore_errors(self, options: Incomplete | None = None): ...
