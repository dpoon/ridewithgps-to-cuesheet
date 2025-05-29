from . import xmlwriter as xmlwriter

class Metadata(xmlwriter.XMLwriter):
    has_dynamic_functions: bool
    has_embedded_images: bool
    num_embedded_images: int
    def __init__(self) -> None: ...
