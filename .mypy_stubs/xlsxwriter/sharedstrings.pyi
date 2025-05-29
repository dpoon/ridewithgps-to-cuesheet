from . import xmlwriter as xmlwriter
from _typeshed import Incomplete

class SharedStrings(xmlwriter.XMLwriter):
    string_table: Incomplete
    def __init__(self) -> None: ...

class SharedStringTable:
    count: int
    unique_count: int
    string_table: Incomplete
    string_array: Incomplete
    def __init__(self) -> None: ...
