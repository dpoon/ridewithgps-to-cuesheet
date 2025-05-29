from . import xmlwriter as xmlwriter
from .chart_area import ChartArea as ChartArea
from .chart_bar import ChartBar as ChartBar
from .chart_column import ChartColumn as ChartColumn
from .chart_doughnut import ChartDoughnut as ChartDoughnut
from .chart_line import ChartLine as ChartLine
from .chart_pie import ChartPie as ChartPie
from .chart_radar import ChartRadar as ChartRadar
from .chart_scatter import ChartScatter as ChartScatter
from .chart_stock import ChartStock as ChartStock
from .chartsheet import Chartsheet as Chartsheet
from .exceptions import DuplicateWorksheetName as DuplicateWorksheetName, FileCreateError as FileCreateError, FileSizeError as FileSizeError, InvalidWorksheetName as InvalidWorksheetName
from .format import Format as Format
from .packager import Packager as Packager
from .sharedstrings import SharedStringTable as SharedStringTable
from .utility import xl_cell_to_rowcol as xl_cell_to_rowcol
from .worksheet import Worksheet as Worksheet
from _typeshed import Incomplete
from xlsxwriter.image import Image as Image

class Workbook(xmlwriter.XMLwriter):
    chartsheet_class = Chartsheet
    worksheet_class = Worksheet
    filename: Incomplete
    tmpdir: Incomplete
    date_1904: Incomplete
    strings_to_numbers: Incomplete
    strings_to_formulas: Incomplete
    strings_to_urls: Incomplete
    nan_inf_to_errors: Incomplete
    default_date_format: Incomplete
    constant_memory: Incomplete
    in_memory: Incomplete
    excel2003_style: Incomplete
    remove_timezone: Incomplete
    use_future_functions: Incomplete
    default_format_properties: Incomplete
    max_url_length: Incomplete
    allow_zip64: bool
    worksheet_meta: Incomplete
    selected: int
    fileclosed: int
    filehandle: Incomplete
    internal_fh: int
    sheet_name: str
    chart_name: str
    sheetname_count: int
    chartname_count: int
    worksheets_objs: Incomplete
    charts: Incomplete
    drawings: Incomplete
    sheetnames: Incomplete
    formats: Incomplete
    xf_formats: Incomplete
    xf_format_indices: Incomplete
    dxf_formats: Incomplete
    dxf_format_indices: Incomplete
    palette: Incomplete
    font_count: int
    num_formats: Incomplete
    defined_names: Incomplete
    named_ranges: Incomplete
    custom_colors: Incomplete
    doc_properties: Incomplete
    custom_properties: Incomplete
    createtime: Incomplete
    num_vml_files: int
    num_comment_files: int
    x_window: int
    y_window: int
    window_width: int
    window_height: int
    tab_ratio: int
    str_table: Incomplete
    vba_project: Incomplete
    vba_project_is_stream: bool
    vba_project_signature: Incomplete
    vba_project_signature_is_stream: bool
    vba_codename: Incomplete
    image_types: Incomplete
    images: Incomplete
    border_count: int
    fill_count: int
    drawing_count: int
    calc_mode: str
    calc_on_load: bool
    calc_id: int
    has_comments: bool
    read_only: int
    has_metadata: bool
    has_embedded_images: bool
    has_dynamic_functions: bool
    has_embedded_descriptions: bool
    embedded_images: Incomplete
    feature_property_bags: Incomplete
    default_url_format: Incomplete
    def __init__(self, filename: Incomplete | None = None, options: Incomplete | None = None) -> None: ...
    def __enter__(self): ...
    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: types.TracebackType | None) -> None: ...
    def add_worksheet(self, name: Incomplete | None = None, worksheet_class: Incomplete | None = None): ...
    def add_chartsheet(self, name: Incomplete | None = None, chartsheet_class: Incomplete | None = None): ...
    def add_format(self, properties: Incomplete | None = None): ...
    def add_chart(self, options): ...
    def add_vba_project(self, vba_project, is_stream: bool = False): ...
    def add_signed_vba_project(self, vba_project, signature, project_is_stream: bool = False, signature_is_stream: bool = False): ...
    def close(self) -> None: ...
    def set_size(self, width, height) -> None: ...
    def set_tab_ratio(self, tab_ratio: Incomplete | None = None) -> None: ...
    def set_properties(self, properties) -> None: ...
    def set_custom_property(self, name, value, property_type: Incomplete | None = None): ...
    def set_calc_mode(self, mode, calc_id: Incomplete | None = None) -> None: ...
    def define_name(self, name, formula): ...
    def worksheets(self): ...
    def get_worksheet_by_name(self, name): ...
    def get_default_url_format(self): ...
    def use_zip64(self) -> None: ...
    def set_vba_name(self, name: Incomplete | None = None) -> None: ...
    def read_only_recommended(self) -> None: ...

class WorksheetMeta:
    activesheet: int
    firstsheet: int
    def __init__(self) -> None: ...

class EmbeddedImages:
    images: Incomplete
    image_indexes: Incomplete
    def __init__(self) -> None: ...
    def get_image_index(self, image: Image): ...
    def has_images(self): ...
