from . import xmlwriter as xmlwriter
from _typeshed import Incomplete
from xlsxwriter.image import Image as Image

class RichValue(xmlwriter.XMLwriter):
    embedded_images: Incomplete
    def __init__(self) -> None: ...
