from .app import App as App
from .comments import Comments as Comments
from .contenttypes import ContentTypes as ContentTypes
from .core import Core as Core
from .custom import Custom as Custom
from .exceptions import EmptyChartSeries as EmptyChartSeries
from .feature_property_bag import FeaturePropertyBag as FeaturePropertyBag
from .metadata import Metadata as Metadata
from .relationships import Relationships as Relationships
from .rich_value import RichValue as RichValue
from .rich_value_rel import RichValueRel as RichValueRel
from .rich_value_structure import RichValueStructure as RichValueStructure
from .rich_value_types import RichValueTypes as RichValueTypes
from .sharedstrings import SharedStrings as SharedStrings
from .styles import Styles as Styles
from .table import Table as Table
from .theme import Theme as Theme
from .vml import Vml as Vml
from _typeshed import Incomplete

class Packager:
    tmpdir: str
    in_memory: bool
    workbook: Incomplete
    worksheet_count: int
    chartsheet_count: int
    chart_count: int
    drawing_count: int
    table_count: int
    num_vml_files: int
    num_comment_files: int
    named_ranges: Incomplete
    filenames: Incomplete
    def __init__(self) -> None: ...
